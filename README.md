# Manga to epub3

This python script download a manga from the web and saved it to the epub3 format.
Currently the epub will generated with a minimum of metadata.
Mangapanda.com is currently the only webpage wich is suported.

### Usage:

    usage: main.py [-h] [-s] [-c CHAPTER] url folder

    Save a manga from mangapanda.com to a epub3 file

    positional arguments:
      url                   The absolute or relative url to the manga.
      folder                Path to th folder where the epub(s) will stored.

    optional arguments:
      -h, --help            show this help message and exit
      -s, --single          The manga will stored in a single epub instant of a
                            separate epub for each chapter.
      -c CHAPTER, --chapter CHAPTER
                            Save only a specific chapter with the chapter number
                            CHAPTER.
