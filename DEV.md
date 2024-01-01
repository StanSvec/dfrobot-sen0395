# DEV notes
## Copy project to raspberry
`rsync -avz -e ssh --exclude '.git' --exclude '.idea' /home/stans/Projects/iot/dfrobot-sen0395/ pi@raspberrypi.local:/home/pi/dfrobot-sen0395`

## Install on raspberry in editable mode
`flit install --user --symlink`
