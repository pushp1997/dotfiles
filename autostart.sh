#!/bin/bash

picom &  # Start compositor
feh --bg-scale /home/pushp/Pictures/wallpaper.jpg &  # Set wallpaper
nm-applet &  # Network  manager frontend
udiskie -t &  # Automount external disks