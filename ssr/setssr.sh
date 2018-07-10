#! /bin/bash

ssrDir=/home/vicky/code/shadowsocksr/shadowsocks
logFile=/var/log/ssr/ssr_$(date +%F_%H-%M-%S).log
conFile=/opt/tools/ssr/shadowsocks.json

/opt/tools/ssr/switchIp.py

cd ${ssrDir}

case $1 in
    start | restart )        
        touch ${logFile}
        sudo ln -sf ${logFile} /var/log/shadowsocksr.log
        sudo python local.py -c ${conFile}  -d $1
        
        sudo systemctl restart privoxy
        ;;
    stop )
        sudo python local.py -c ${conFile} -d stop
        ;;
    * | help )
        echo "Usage: $0 {start | restart | stop }"
        ;;
esac
