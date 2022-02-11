import os, json

IP = os.environ.get("IP")
UUID = os.environ.get("UUID")
PORT = os.environ.get("PORT")


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
            "address": f"{IP}",
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

with open('/etc/v2ray/config.json', 'w') as f:
    json.dump(server_config, f, indent=4)

with open('/root/config.json', 'w') as f:
    json.dump(client_config, f, indent=4)



