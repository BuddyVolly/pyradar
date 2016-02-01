#pyradar

PyRadar fork GIT repository.
Filters are NUMBA-powered; So, new requirement is NUMBA

|          Filter              |      No NUMBA       |      NUMBA          |
|------------------------------|---------------------|---------------------|
| Frost on 256x256 patch       |      9.72s          |       0.51s         |
| Kuan on 256x256 patch        |      5.38s          |       0.05s         |
| Lee on 256x256 patch         |      5.47s          |       0.05s         |
| LeeEnchanced on 256x256 patch|      5.46s          |       0.12s         |



## Installing GDAL for Python3

To not get numpy messed by obsolete version from repo, you can just install gdal

    apt-get download python3-gdal
    dpkg --force-all -i <name of the .deb files you downloaded>

## Contact Information

Mail the authors!
  *  Herranz, Matías <matiasherranz@gmail.com>
  *  Tita, Joaquín <joaquintita@gmail.com>

Or the colaborator!
  *  Cabral, Juan B. <jbc.develop@gmail.com>

Or the guy, who rewritten filters using NUMBA!
  *  Nanopony <sddeath@gmail.com>


### The docs are in readthedocs.org

http://pyradar-tools.readthedocs.org

### This is an example of what you can achieve with PyRadar:

Isodata clasification algorithm

<img align="CENTER"
     src="https://raw.github.com/PyRadar/pyradar/master/stuff/imgs/isodata.gif"
     alt="isodata"/>

Video in better quality: http://www.youtube.com/watch?v=4meidkmJWP0
