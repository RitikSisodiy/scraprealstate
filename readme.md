I - Introduction:

The intention of this documentation is to give the reader a step-by-step guide to scrap data from ““

II - Scope:

Through this documentation, it shows how to setup our Scrapy spider ,how to install it on your machine, And 

start scraping

III - Assumptions:

The user must have some experience with Python and the command line

A command-line-interface to interact with your computer

A text editor to work with plain text files

Version 3.7 of the Python programming language

The pip package manager for Python

 

VII - The libraries & installations:

Before running the headless scripts, we need to be sure to have on our server:

64 bits server

$ lscpu | head -n 2
Architecture:                    x86_64
CPU op-mode(s):                  32-bit, 64-bit



Python 3

$ python3 -V
Python 3.8.2



pip3

$ pip3 -V
pip 20.1.1 from /home/roiarthurb/.local/lib/python3.8/site-packages/pip (python 3.8)



STEP 1. Create a virtual Environment and activation , Run the following Command on terminal

pip install virtualenv  // to install the virtualenv package

virtualenv <name of environment> // this command create a Virtual Environment 

source <name of environment>/bin/activate  // for linux

<name of environment>\Scripts\activate // for windows

STEP 2. Now we install the the dependencies of Project, for this run the following command

pip install -r requirements.txt  // make sure you are in the base directory of the project

VIII - Scraping The Data:

Now first we configure the MySQL database to store the data

for that have to create a new database in MySQL and add the configuration of that database in .env  file located in base directory

Make changes in  .env  file

DB_NAME="<name of database>"
DB_USER="<username>"
DB_PASSWORD="<password>"
DB_HOST="<HOST of database>"  # 'localhost'
DB_PORT=<PORT of database> # 3360

Now run the following command to start scraping

scrapy crawl netvendeur

If for some reason script terminated and you want to resume the scraping from the termination point run the following command

 scraping run "scrapy crawl netvendeur -s JOBDIR=crawls/netvendeur-1 