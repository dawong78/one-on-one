#!/bin/sh

mkdir ~/.npm-packages
npm config set prefix ~/.npm-packages
npm install -g @angular/cli
