# BeatNΞxus

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django?color=blue&logo=python)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/Original%20Author-sicktrick--237-brightgreen)](https://github.com/sicktrick-237)

BeatNexus is a python based web application which lets you save tracklists from 1001 Tracklists and MixesDB, directly to your YouTube or Spotify playlists.

Note: For Access (client secret), please follow the steps below.

## New Additions

* Now you can save your favourite Tracklists on Spotify.
* Also, you are now able to save your MixesDB tracklists to YouTube and Spotify.

## Packages

All the required packages are found on PyPI

[![PyPI](https://img.shields.io/pypi/v/apiclient?label=apiclient&logo=google)](https://pypi.org/project/apiclient/)
[![PyPI](https://img.shields.io/pypi/v/google-auth-httplib2?color=9cf&label=google-auth-httplib2)](https://pypi.org/project/google-auth-httplib2/)
[![PyPI](https://img.shields.io/pypi/v/Beautifulsoup?color=yellow&label=Beautifulsoup)](https://pypi.org/project/beautifulsoup4/)
[![PyPI](https://img.shields.io/pypi/v/selenium?label=selenium&logoColor=blue)](https://pypi.org/project/selenium/)
[![PyPI](https://img.shields.io/pypi/v/tqdm?label=tqdm&logoColor=blue)](https://pypi.org/project/tqdm/)

## Links

* All the Packages used in this project are included in Anaconda Distribution. You can download it <a href="https://www.anaconda.com/distribution/">here</a>.
* List of Radio Shows, Festival Mixes and Guestmix can be found on <a href="https://www.mixesdb.com/db/index.php/Main_Page">MixesDB</a> & <a href="https://www.1001tracklists.com">1001Tracklists</a>

## Installation
Install above packages with pip. Example.
```
$ pip install apiclient
```

## Usage

### Command Line Interface

* Install the dependencies and change the running directory to project directory.
    ```
    $ cd tracklist-manager 
    $ python PlaylistGenerator.py
    ```
* Enter your favourite 1001 or MixesDB Tracklist URL. Take this for <a href="https://www.1001tracklists.com/tracklist/g5tm74k/dada-life-podcast-december-2019-12-18.html">Example</a>
    ```
    Enter 1001Tracklist or MixesDB URL :
    ```

### Demo
![BeatNexus](demo/demo.gif)


### Jupyter Notebook

Open PlaylistGenerator.ipynb in Jupyter and Run.

Follow the instructions as per required inputs.
