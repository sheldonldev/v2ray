#!/bin/sh

if [ -f .env ]
then
  export $(grep -v '^#' .env | xargs)
fi

export TARGETPLATFORM="linux/amd64"
export TAG="v4.44.0"
export PORT="443"
export UUID="87e209b7-f0b0-4155-ba97-030e8f71eb53"

apt update
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3 -y
apt install python3-pip -y
apt install unzip -y

echo "Prepare to use"
unzip v2ray-linux-64.zip && chmod +x v2ray v2ctl
mv systemd/system/v2ray.service /etc/systemd/system/v2ray.service
mv v2ray v2ctl /usr/local/bin/
mkdir /usr/local/etc/v2ray
mv config.json /usr/local/etc/v2ray/config.json
mkdir /usr/local/share/v2ray
mv geosite.dat geoip.dat /usr/local/share/v2ray/

# Clean
rm *.dat
rm *.json
rm -rf systemd

# create config
pip3 install -r requirements.txt
python3 config.py
echo "v2ray installed"

# start
sudo systemctl daemon-reload
sudo systemctl start v2ray.service
echo "Finished! May need reboot."
sudo systemctl status v2ray.service
