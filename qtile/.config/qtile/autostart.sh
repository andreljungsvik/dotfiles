#!/bin/sh
xrandr --output DP-2 --primary --mode 2560x1440 --rate 240.00 --output DP-0 --mode 1920x1080 --rate 144.00 --right-of DP-2

xinput --set-prop 'pointer:''Keychron Keychron Ultra-Link 8K' 'libinput Accel Profile Enabled' 0, 1

picom &

xset -dpms
xset s off
xset s noblank

eval "$(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)"
export SSH_AUTH_SOCK

#(sleep 2 && setxkbmap -layout us -option compose:ralt) &
