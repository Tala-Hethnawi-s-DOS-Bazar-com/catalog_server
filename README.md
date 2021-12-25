# Catalog Server

#### This repo is part of Bazar.com: A Multi-tier Online Book Store

To run it please do the following:

1- Make sure you have docker installed

2 - Make sure you have your network set up (docker network create --subnet=172.18.0.0/16 bazar)
3- Within the repo directory run these commands in your terminal:
* docker build --tag catalog-server .
* docker run --net bazar --ip 172.18.0.20 catalog-server
* docker run --net bazar --ip 172.18.0.21 catalog-server
