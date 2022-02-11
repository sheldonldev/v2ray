import os, json
from decouple import config

ADDRESS = config("ADDRESS")
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
            "id": f"{UUID}",
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

client_config = {
  "log": {
    "error": "",
    "loglevel": "info",
    "access": ""
  },
  "inbounds": [
    {
      "listen": "127.0.0.1",
      "protocol": "socks",
      "settings": {
        "udp": False,
        "auth": "noauth"
      },
      "port": 10808
    },
    {
      "listen": "127.0.0.1",
      "protocol": "http",
      "settings": {
        "timeout": 360
      },
      "port": 10809
    }
  ],
  "outbounds": [
    {
      "mux": {
        "enabled": False,
        "concurrency": 8
      },
      "protocol": "vmess",
      "streamSettings": {
        "network": "tcp",
        "tcpSettings": {
          "header": {
            "type": "none"
          }
        },
        "security": "none"
      },
      "tag": "proxy",
      "settings": {
        "vnext": [
          {
            "address": f"{ADDRESS}",
            "users": [
              {
                "id": f"{UUID}",
                "alterId": 64,
                "level": 0,
              }
            ],
            "port": int(PORT)
          }
        ]
      }
    },
    {
      "tag": "direct",
      "protocol": "freedom",
      "settings": {
        "domainStrategy": "UseIP",
        "userLevel": 0
      }
    },
    {
      "tag": "block",
      "protocol": "blackhole",
      "settings": {
        "response": {
          "type": "none"
        }
      }
    }
  ],
  "dns": {},
  "routing": {
    "settings": {
      "domainStrategy": "AsIs",
      "rules": []
    }
  },
  "transport": {}
}

with open('/usr/local/etc/v2ray/config.json', 'w') as f:
    if os.environ.get('ENDTYPE') == 'server':
        json.dump(server_config, f, indent=4)
    elif os.environ.get('ENDTYPE') == 'client':
        json.dump(client_config, f, indent=4)
    else:
        print("'server' or 'client'?")



