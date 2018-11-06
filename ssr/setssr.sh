#! /bin/bash

ssrDir=/home/vicky/code/shadowsocksr/shadowsocks
actLogFile=/var/log/ssr/ssr_$(date +%F_%H-%M-%S).log
logFile=/var/log/shadowsocksr.log
conFile=/opt/tools/ssr/shadowsocks.json
arcConfig=/opt/tools/ssr/shadowsocksXiong.json

case $1 in
    start | restart )
        cd ${ssrScript}
        pwd
        
        case $2 in
            X )
                ./switchXMIp.py
                ;;
            W )
                ./switchWall.py
                ;;
            * )
                ./switchIp.py
                ;;
        esac
        
        touch ${actLogFile}
        sudo ln -sf ${actLogFile} ${logFile}
        cat ${conFile} |grep -Eo '"server":[ ."0-9]+' |sudo tee -a ${logFile}

        cd ${ssrDir}

        sudo python local.py -c ${conFile}  -d $1
#        sudo systemctl restart privoxy
        ;;
   
    stop )
        cd ${ssrDir}

        sudo python local.py -c ${conFile} -d stop
        ;;
    * | help )
        cat >&1 <<- 'EOF'
    Location: $0

    Usage: { start | restart 
             start X | restart X 
             start W | restart W
             stop }
        start will swith ip with doub
        start X swith ip from Xiongmao
        start W swith ip from WallLink
EOF
        ;;
esac

