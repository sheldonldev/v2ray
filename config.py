import os, json
from decouple import config

ADDRESS = config("ADDRESS")
UUID = config("UUID")
PORT = config("PORT")


server_config = {
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "stats": {},
  "api": {
    "tag": "api",
    "services": ["StatsService"]
  },
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    },
    "system": {
      "statsInboundUplink":true,
      "statsInboundDownlink": true
    }
  },
  "inbounds": [
    {
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls"]
      },
      "tag": "tcp",
      "port": int(PORT),
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "email": "99999999@muppets.monster",
            "id": f"{UUID}",
            "level": 0,
            "alterId": 64
          }
        ]
      }
    },
    {
      "listen": "127.0.0.1",
      "port": 10085,
      "protocol": "dokodemo-door",
      "settings": {
        "address": "127.0.0.1"
      },
      "tag": "api"
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
    "settings": {
      "rules": [
        {
          "inboundTag": ["api"],
          "outboundTag": "api",
          "type": "field"
        }
      ]
    },
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
        "udp": false,
        "auth": "noauth"
      },
      "port": "10808"
    },
    {
      "listen": "127.0.0.1",
      "protocol": "http",
      "settings": {
        "timeout": 360
      },
      "port": "10809"
    }
  ],
  "outbounds": [
    {
      "mux": {
        "enabled": false,
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
                "alterId": 0,
                "level": 0,
                "security": "aes-128-gcm"
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



