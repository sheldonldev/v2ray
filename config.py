import os, json
from decouple import config

ADDRESS = config("ADDRESS")
UUID = config("UUID")
PORT = config("PORT")


server_config = {
    "inbounds": [{
        "port": int(PORT),
        "protocol": "vmess",
        "settings": { "clients": [{ "id": f"{UUID.lower()}" }] }
    }],
    "outbounds": [{
        "protocol": "freedom",
        "settings": {}
    }]
}

client_config = {
    "inbounds": [{
        "port": 10808,
        "listen": "127.0.0.1",
        "protocol": "socks",
        "settings": {
            "udp": True
        }
    },{
        "port": 10809,
        "listen": "127.0.0.1",
        "protocol": "http",
        "settings": {
            "udp": True
        }
    }],
    "outbounds": [{
        "protocol": "vmess",
        "settings": {
        "vnext": [{
            "address": f"{ADDRESS}",
            "port": int(PORT),
            "users": [{ "id": f"{UUID.lower()}" }]
        }]
        }
    },{
        "protocol": "freedom",
        "tag": "direct",
        "settings": {}
    }],
    "routing": {
        "domainStrategy": "IPOnDemand",
        "rules": [{
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "direct"
        }]
    }
}

with open('/usr/local/etc/v2ray/config.json', 'w') as f:
    if os.environ.get('ENDTYPE') == 'server':
        json.dump(server_config, f, indent=4)
    elif os.environ.get('ENDTYPE') == 'client':
        json.dump(client_config, f, indent=4)
    else:
        print("'server' or 'client'?")



