"""
Flask web app server
Written by Jess Sullivan
"""
from flask import Flask, redirect, flash, render_template, send_from_directory, request
from datetime import datetime
import subprocess
import os
import secrets
import time
import threading
import zipfile
from shutil import move

# global:
verbose = True  # verbose logging?
usrfile = 'usrfile'  # files should already be unique, each is in hashed dir
usr_id = ''  # placeholder for usr hex value

# paths:
rootpath = os.path.abspath(os.curdir)
inpath = os.path.join(rootpath, 'uploads')
outpath = os.path.join(rootpath, 'downloads')
templates = os.path.join(rootpath, 'templates')
rel_templates = os.path.relpath('templates')
r_apps = os.path.join(rootpath, 'shiny_apps')
rel_r_apps = os.path.relpath(r_apps)

# url:
hostname = '127.0.0.1'
hostport = 5000

# define Flask app:
app = Flask(__name__, template_folder=rel_templates, static_url_path=inpath)

# app modifications- using pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# recycle directories:
live_app_list = {}
start_time = time.time()
collection_int = 60  # max. lifetime of each app thread


# verbose logging?
def v(message):
    if verbose:
        print(message)


# check upload path before continuing:
if not os.path.exists(inpath):
    v(str('creating upload path ... '))
    os.mkdir(inpath)


def uploader(usrpath):  # see Flask docs
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            f = request.files['file']
            f.save(os.path.join(usrpath, usrfile))


def force_dir_rm(path):  # used by garbage daemon
    # checking and removing user dirs from OS-
    # assuming child threads may occasionally misbehave,
    # best to avoid guessing the state of child threads here in Python
    subprocess.Popen(str('rm -rf ' + path),
                     shell=True,
                     executable='/bin/bash')


def garbageloop():
    while True:
        time.sleep(collection_int)
        for usr in os.listdir(inpath):
            if not usr in live_app_list.keys():
                live_app_list[usr] = time.time()
            if time.time() - live_app_list[usr] > 10:
                try:
                    v('removing expired usr directories...')
                    force_dir_rm(os.path.join(inpath, usr))
                    live_app_list.pop(usr)
                except:
                    v(str('Error while removing expired usr directory:  \n' + usr))


# start garbageloop as daemon- operating as a child to Flask server:
init_loop = threading.Thread(target=garbageloop, daemon=True)
init_loop.start()


def isworking(proc):
    cmd = str('ps -q ' + str(proc) + ' -o state --no-headers')

    check = subprocess.Popen(cmd,
                             shell=True,
                             executable='/bin/bash',
                             encoding='utf8',
                             stdout=subprocess.PIPE)

    if check.stdout.read()[0] != 'S':
        return False
    else:
        return True


def newclient():
    return secrets.token_hex(15)


def r_thread(usr_dir, infile, outfile, choice, opt1=None, opt2=None, opt3=None, opt4=None):
    logfile = os.path.join(usr_dir, 'logs.txt')

    subprocess.Popen(str('touch ' + logfile),
                     shell=True,
                     executable='/bin/bash',
                     encoding='utf8')

    cmd = str('Rscript ' + os.path.join(r_apps, choice) +
              ' ' + infile +
              ' ' + outfile +
              ' >> ' + logfile)

    for opt in [opt1, opt2, opt3, opt4]:
        if opt is not None:
            cmd += str(' ' + opt)

    v(str('running command:  \n' + cmd))

    proc = subprocess.Popen(cmd,
                            shell=True,
                            executable='/bin/bash',
                            encoding='utf8')
    return proc.pid


class R_appThread(object):

    def __init__(self, outname, appchoice, templatepage, title,
                 opt1=None, opt2=None, opt3=None, opt4=None):

        self.templatepage = templatepage
        self.appchoice = appchoice
        self.outname = outname
        self.title = title
        self.opt1 = opt1
        self.opt2 = opt2
        self.opt3 = opt3
        self.opt4 = opt4

    def main(self):

        usr_id = newclient()
        usr_dir = os.path.join(inpath, usr_id)

        if not os.path.exists(usr_dir):
            os.mkdir(usr_dir)

        uploader(usr_dir)

        # while at url, run script after upload:
        if len(os.listdir(usr_dir)) > 0:
            """
            # assuming worker file takes at least two arguments- for example in R:
            args <- commandArgs(trailingOnly = TRUE)
            input <- args[1]  # file path from Flask
            output <- args[2]  # output directory
            """
            r_thread(usr_dir=usr_dir,
                     infile=os.path.join(usr_dir, usrfile),
                     outfile=os.path.join(usr_dir, self.outname),
                     choice=self.appchoice,
                     opt1=self.opt1,
                     opt2=self.opt2,
                     opt3=self.opt3,
                     opt4=self.opt4)

            # template is returned immediately, regardless of upload:
        return render_template(self.templatepage,
                               page=self.title,
                               tokenID=usr_id,
                               outname=self.outname)


def archiver(dl_filepath, usr_path):
    archive = zipfile.ZipFile(dl_filepath, "w", zipfile.ZIP_DEFLATED)
    for f in os.listdir(usr_path):
        archive.write(os.path.join(usr_path, f), arcname=f)
    archive.close()


@app.route('/')
def home():
    return render_template('home.jade', page='Home', tokenID='index')


@app.route('/download', methods=['GET', 'POST'])
def download():
    req = request.form.get('name')
    usr_path = os.path.join(inpath, req)
    print(usr_path)
    dl_filename = str('output_' + datetime.today().strftime('%Y-%m-%d') + '.zip')
    dl_filepath = os.path.join(usr_path, dl_filename)
    print(dl_filepath)
    archiver(dl_filepath, usr_path)
    response = send_from_directory(os.path.join(inpath, req), filename=dl_filename)
    response.headers["Content-Disposition"] = str('attachment; filename=' + dl_filename)
    return response


@app.route('/centkml', methods=['GET', 'POST'])
def centkml():
    cent = R_appThread(appchoice=os.path.join(r_apps, 'centkml.R'),
                       templatepage='generic.jade',
                       outname='output.kml',
                       title='KML Centroid Generator')
    return cent.main()


@app.route('/kmlcsv', methods=['GET', 'POST'])
def kmlcsv():
    kmlcsv = R_appThread(appchoice=os.path.join(r_apps, 'kml2csv.R'),
                         templatepage='generic.jade',
                         outname='output.csv',
                         title='KML --> CSV Converter')
    return kmlcsv.main()


@app.route('/kmlshp', methods=['GET', 'POST'])
def kmlshp():
    kmlshp = R_appThread(appchoice=os.path.join(r_apps, 'kml2shp.R'),
                         templatepage='generic.jade',
                         outname='shp.zip',
                         opt1='tmp.shp',
                         title='KML --> SHP Converter')
    return kmlshp.main()


@app.route('/demstl', methods=['GET', 'POST'])
def demstl():
    demstl = R_appThread(appchoice=os.path.join(r_apps, 'dem2stl.R'),
                         templatepage='generic.jade',
                         outname='output.stl',
                         title='DEM --> STL Converter')
    return demstl.main()
