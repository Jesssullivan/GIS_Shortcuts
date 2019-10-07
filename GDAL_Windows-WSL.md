# Using Ubuntu GDAL on Windows w/ WSL   

[LINK: get the WSL shell from Microsoft](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

```
# In the WSL shell:

sudo apt-get install python3.6-dev -y
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install libgdal-dev -y
sudo apt-get install gdal-bin -y

# See here for more notes including Python bindings:
# https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
```
