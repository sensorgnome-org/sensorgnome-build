#!/bin/sh -e

# Install nodejs sensorgnome server dependencies using NPM.
on_chroot << EOF
npm install pm2 express socket.io connect errorhandler body-parser method-override multer
EOF
