# Catalog Server

#### This repo is part of Lab 1: Bazar.com: A Multi-tier Online Book Store

Note: This server runs on port 8000

To run it please do the following:

1- Make sure you have vagrant and virtualbox installed

2- Within the repo directory run these commands in your terminal:
* vagrant up
* vagrant ssh
* cd /vagrant
* python3 -m venv ~/venv
* source ~/venv/bin/activate
* pip install --upgrade pip
* pip install -r requirements.txt
* export FLASK_APP=server
* python -u -m flask run --host=0.0.0.0