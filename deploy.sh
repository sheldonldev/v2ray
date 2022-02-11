#!/bin/sh

if [ -f .env ]
then
  export $(grep -v '^#' .env | xargs)
fi

export ENDTYPE=$1

export IP=${SERVER_ADDRESS}
export PORT=${PORT}
export UUID=${UUID}

echo "Asia/Shanghai" > /etc/timezone

apt update
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3 -y
apt install unzip -y

./v2ray.sh "${TARGETPLATFORM}" "${TAG}"
echo "v2ray installed"

python3 config.py
echo $IP
echo $PORT
echo $UUID

sudo systemctl daemon-reload
sudo systemctl start v2ray.service

echo "finished"

sleep 1
echo "may need reboot"
sleep 3

sudo systemctl status v2ray.service



