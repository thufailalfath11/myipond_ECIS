#!/bin/bash
cd /home/ECIS/myipond_ECIS/
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
if [ $LOCAL != $REMOTE ]; then
  git pull
  npm install      # atau pip install -r requirements.txt jika pakai Python
  sudo systemctl restart myipond-vite   # restart service kalau perlu
  sudo systemctl restart dekripsi       # backend juga auto restart
fi
