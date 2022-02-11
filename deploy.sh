#!/bin/sh

if [ -f .env ]
then
  export $(grep -v '^#' .env | xargs)
fi

export ENDTYPE=$1

echo "Asia/Shanghai" > /etc/timezone

apt update
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3 -y
apt install unzip -y

echo "Prepare to use"
unzip v2ray.zip && chmod +x v2ray v2ctl
mv systemd/system/v2ray.service /etc/systemd/system/v2ray.service
mv v2ray v2ctl /usr/local/bin/
mkdir /usr/local/etc/v2ray
mv config.json /usr/local/etc/v2ray/config.json
mkdir /usr/local/share/v2ray
mv geosite.dat geoip.dat /usr/local/share/v2ray/
echo "v2ray installed"

# Clean
rm *.dat
rm *.json
rm -rf systemd

# create config
pip install -r requirements.txt
python3 config.py

# start
sudo systemctl daemon-reload
sudo systemctl start v2ray.service
echo "Finished! May need reboot."
sudo systemctl status v2ray.service



