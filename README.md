# README


## Ubuntu - Install / Update Config

- clone this repo.

- `.env` example:
```bash
ADDRESS="139.0.0.0"
PORT="00000"
UUID="abcdefgh-ijkm-00oo-bbrl-kkkkol0ll999"
```

```bash
chmod +x ./deploy.sh

# server root
./deploy.sh server

# client user
sudo bash ./deploy.sh client
```


## Android

- Find app on google appstore on the chrome. 
- Copy url to a chrome extention: apk downloader, select your version.
- Download and generate a short link with Wetransfer.
- Typing the short link on Android, download.
- Setup your config and done.
