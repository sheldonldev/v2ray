import os, json
from decouple import config

UUID = config("UUID")
PORT = config("PORT")

server_config = {
  "inbounds": [
    {
      "sniffing": {
        "enabled": True,
        "destOverride": ["http", "tls"]
      },
      "tag": "tcp",
      "port": int(PORT),
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": UUID,
            "level": 0,
            "alterId": 64
          }
        ]
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "direct"
    },
    {
      "protocol": "blackhole",
      "settings": {},
      "tag": "block"
    }
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {
        "type": "field",
        "outboundTag": "block",
        "protocol": ["bittorrent"]
      }
    ],
    "strategy": "rules"
  }
}

with open('/usr/local/etc/v2ray/config.json', 'w') as f:
    json.dump(server_config, f, indent=4)
