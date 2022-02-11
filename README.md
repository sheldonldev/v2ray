# README

- ubuntu

- `.env`
```bash
ADDRESS="139.0.0.0"
PORT="00000"
UUID="abcdefgh-ijkm-00oo-bbrl-kkkkol0ll999"
```

- run
```bash
chmod +x ./deploy.sh

# server root
./deploy.sh server

# client user
sudo bash ./deploy.sh client
```

- update config
```bash
# update `.env`, then:

# server
python config.py ENDTYPE=server

# client
python config.py ENDTYPE=client
```
