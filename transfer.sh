#!/bin/bash

./ffmpeg -i $1/$1.mp4 -c:v libx264 -b:v 3M -threads 5 -preset superfast $1/f_$1.mp4