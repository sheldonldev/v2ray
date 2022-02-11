#!/bin/sh

if [ -f .env ]
then
  export $(grep -v '^#' .env | xargs)
fi

export ENDTYPE=$1

export IP=${SERVER_ADDRESS}
export PORT=$(( ( RANDOM % 60000 )  + 30000 ))
export UUID=$(uuidgen)

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

/usr/bin/v2ray -config /etc/v2ray/config.json
echo "finished"

sleep 1
echo "please reboot"
sleep 3



