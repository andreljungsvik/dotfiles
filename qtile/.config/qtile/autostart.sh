#!/bin/sh
xrandr --output DP-2 --primary --mode 2560x1440 --rate 240.00 --output DP-0 --mode 1920x1080 --rate 120.00 --right-of DP-2

mouse_name="Endgame Gear Endgame Gear OP1 8k Gaming Mouse"

xinput --set-prop "$mouse_name" "libinput Accel Profile Enabled" 0 1
xinput --set-prop "$mouse_name" "libinput Accel Speed" -0.5

picom &

xset -dpms
xset s off
xset s noblank

eval "$(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)"
export SSH_AUTH_SOCK

redshift -c /home/user/.config/redshift.conf &

