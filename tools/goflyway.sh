#!/usr/bin/env bash

# update log
#
# version: 0.0.03
# date: 2018-10-09
#    1. update for kcp using version 1.3.0a 
#
# version: 0.0.02
# date: 2018-06-04
#    1. add function start_goflyway_pass_site
#

declare -r GoflywayToolVer="0.0.03"
declare -r CurDir=$(cd "$(dirname "$0")"; pwd)
declare -r DownlodDir="/tmp/goflyway"
declare -r FinalDir="/usr/local/goflyway"
declare -r ConfFile="/etc/goflyway/goflyway.ini"
declare -r LogDir="/var/log/goflyway"


#=================================================
#   common function
#=================================================

function green_font(){
     printf "\033[32m %s \033[0m\n" "$@"
}
function green_background_font(){
     printf "\033[42;37m %s \033[0m\n" "$@"
}
function red_font(){
     printf "\033[31m %s \033[0m\n" "$@"
}
function red_background_font(){
     printf "\033[41;37m %s \033[0m\n" "$@"
}
Info=`green_font '[信息]'`
Error=`red_font '[错误]'`
Tip=`red_font '[注意]'`

Separator_1="——————————————————————————————"

function check_sys(){
    [[ $(uname -m) -eq "x86_64" ]] && [[ -f /etc/redhat-release ]]  || {
        echo "this script only support CentOS 7, x86_64"
        exit 1
    }
}
function check_number(){
    expr $1 "+" 10 &> /dev/null

    if [ $? -eq 0 ];then
        echo 0
    else
        echo 1
    fi
}

function get_ip(){
    ip=$(wget -qO- -t1 -T2 ipinfo.io/ip)
    if [[ -z "${ip}" ]]; then
        ip=$(wget -qO- -t1 -T2 api.ip.sb/ip)
        if [[ -z "${ip}" ]]; then
            ip=$(wget -qO- -t1 -T2 members.3322.org/dyndns/getip)
            if [[ -z "${ip}" ]]; then
                ip="VPS_IP"
            fi
        fi
    fi
}

function ini_get_options(){
    ini_file=$1
    section=$2

    options=$(sed -ne "/^\[${section}\]/,/^\[.*\]/ p"  $ini_file  \
    | grep -v "^\[.*\]\|^#" | cut -d "=" -f 1)
    echo ${options}
}

function ini_get_option_value(){
    ini_file=$1
    section=$2
    option=$3

    if grep -q "^\[${section}\]" "$ini_file"; then
        echo $(sed -ne "/^\[${section}\]/,/^\[.*\]/ p"  $ini_file  \
    | grep -v "^\[.*\]\|^#" | grep "${option}"|cut -d "=" -f 2)
    fi

}

function ini_change_option(){
    ini_file=$1
    section=$2
    option=$3
    opt_val=$4

    if ! grep -q "^\[${section}\]" "$ini_file"; then
        # Add section at the end
        echo -e "\n[${section}]" |  tee --append "$ini_file" > /dev/null
    else
        # Remove old values
        sed -i -e "/^\[${section}\]/,/^\[.*\]/ { /^${option}[ \t]*=/ d; }" "$ini_file"
    fi

    # add new option
    sed -i -e "/^\[${section}\]/ a\\
${option}=${opt_val}
" "$ini_file"
}


function add_port(){
    port=$1

    if [[ $(firewall-cmd --list-port | grep "${port}/tcp" | wc -l) -eq 0 ]] ; then
        echo "开启端口 ${port}"
        [[ $(check_number ${port}) -eq 0 ]] && {
            firewall-cmd --add-port=${port}/tcp --permanent
            firewall-cmd --reload
        }
    fi
}
function remove_port(){
    port=$1

    [[ -z ${port} ]] && return
    if [[ $(firewall-cmd --list-port | grep "${port}/tcp" | wc -l) -gt 0 ]] ; then

        echo "关闭端口 ${port}"
        [[ $(check_number ${port}) -eq 0 ]] && {
            firewall-cmd --remove-port=${port}/tcp --permanent
            firewall-cmd --reload
        }
    fi
}

#=================================================
#   goflyway function
#=================================================
function get_latest_ver(){
    echo $(wget --no-check-certificate -qO- https://api.github.com/repos/coyove/goflyway/releases | grep -o '"tag_name": ".*"' |head -n 1| sed 's/"//g' | sed 's/tag_name: //g')

}
function check_installed(){
    [[ -e ${finalDir} ]] && {
        echo "goflyway already installed, please check ${finalDir}"
        exit 1
    }
}



function get_pid(){
    echo `ps -ef |grep -v grep | grep -v goflyway.sh| grep goflyway |awk '{print $2}'`
}

function set_password(){
    echo -e "Please intput goflyway password"
    stty erase '^H' && read -p "(default goflyway.io):" goflywayPwd
    [[ -z "$goflywayPwd" ]] && goflywayPwd="goflyway.io"

    echo && echo ${Separator_1} && echo -e "    密码 : "$(green_font ${goflywayPwd}) && echo ${Separator_1} && echo
}

function set_port(){
    [[ -e ${ConfFile} ]] || set_default_conf
    while true
    do
        echo -e "请输入 goflyway 端口号"
        stty erase '^H' && read -p "(default 8080):" goflywayPort
        [[ -z "$goflywayPort" ]] && goflywayPort="8080"

        [[ $(check_number ${goflywayPort}) -eq 0 ]] && {
            if [[ ${goflywayPort} -ge 1 ]] && [[ ${goflywayPort} -le 65535 ]]; then
                echo &&\
                echo ${Separator_1} &&\
                echo -e "    端口 :  "$(green_font ${goflywayPort}) &&\
                echo ${Separator_1} && echo
                break
            else
                echo -e "${Error} 请输入正确的数字(1-65535)"
            fi
        } || {
            echo -e "${Error} 请输入正确的数字(1-65535)"
        }
    done
}

function set_default_conf(){
    [[ -e $(dirname ${ConfFile}) ]] || {
        mkdir $(dirname ${ConfFile})
    }

    cat > ${ConfFile}<<-EOF
[ServerConfig]
File=${FinalDir}/goflyway
Version=${goflywayLatestVer}
Port=${goflywayPort}
Passwd=${goflywayPwd}
Proxy_Mode=1
EOF
}
function install_goflyway(){
    cd ${CurDir}

    goflywayLatestVer=$(get_latest_ver)
    echo -e  "latest goflyway version: "$(green_font ${goflywayLatestVer})

    if [[ $(uname -m) == "x86_64" ]]; then
        bit='amd64'
    else bit='386'
    fi

    set_password
    set_port
    set_default_conf

    [[ -e "${CurDir}/goflyway_linux_amd64.tar.gz" ]] && {
        rm -f "${CurDir}/goflyway_linux_amd64.tar.gz"
    }
    [[ ! -z ${bit} ]] && {
        wget -N --no-check-certificate "https://github.com/coyove/goflyway/releases/download/${goflywayLatestVer}/goflyway_linux_${bit}.tar.gz"
        #goflyway_linux_amd64.tar.gz
    }

    [[ -e "${CurDir}/goflyway_linux_amd64.tar.gz" ]] || {
        echo "文件下载失败"
        exit 1
    }

    [[ -e ${FinalDir} ]] || {
        mkdir ${FinalDir}
    }
    tar -xzf "goflyway_linux_${bit}.tar.gz" -C ${FinalDir}  && rm -rf "goflyway_linux_${bit}.tar.gz"

    ln -sf ${FinalDir}/goflyway /usr/local/bin/

    start_goflyway

}

function update_goflyway(){
    echo "update_goflyway not implated"
    goflywayLatestVer=$(get_latest_ver)
    echo -e  "latest goflyway version: "$(green_font ${goflywayLatestVer})

    goflywayVer=$(ini_get_option_value ${ConfFile} "ServerConfig" "Version")

    if [[ "${goflywayLatestVer}" == "${goflywayVer}" ]] ; then
        echo "已经是最新版本，无需更新"
    else
        delete_goflyway
        install_goflyway
    fi

}

function update_port(){
    oldPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    set_port

    if [[ ${goflywayPort} != ${oldPort} ]] ; then
        echo "change port from "$(green_font ${oldPort})" to "$(green_font ${goflywayPort})
        ini_change_option  ${ConfFile} "ServerConfig" "Port" ${goflywayPort}
        remove_port ${oldPort}
        stop_goflyway
        start_goflyway
    fi
}

function update_password(){
    oldPwd=$(ini_get_option_value ${ConfFile} "ServerConfig" "Passwd")
    set_password

    if [[ ${goflywayPwd} != ${oldPwd} ]] ; then
        echo "change password from "$(green_font ${oldPwd})" to "$(green_font ${goflywayPwd})
        ini_change_option  ${ConfFile} "ServerConfig" "Passwd" ${goflywayPwd}

        stop_goflyway
        start_goflyway
    fi
}
function check_log(){
    tail -f ${LogDir}/goflyway.log
}

function get_config(){
#     options=($(ini_get_options ${ConfFile} "ServerConfig"))

#     for key in ${options[@]}
#     do
#         option_value=$(ini_get_option_value ${ConfFile} "ServerConfig" ${key})

#         echo -e $(printf "%-30s%s\n" "${key}:" $(green_font ${option_value}))
#     done
    goflywayFile=$(ini_get_option_value ${ConfFile} "ServerConfig" "File")
    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    goflywayPwd=$(ini_get_option_value ${ConfFile} "ServerConfig" "Passwd")
    goflywayVer=$(ini_get_option_value ${ConfFile} "ServerConfig" "Version")

    get_ip
    pid=$(get_pid)

    echo -e "    I  P:   " $(green_font ${ip})
    echo -e "    File:   " $(green_font ${goflywayFile})
    echo -e "    Verion: " $(green_font ${goflywayVer})
    echo -e "    Port:   " $(green_font ${goflywayPort})
    echo -e "    Passwd: " $(green_font ${goflywayPwd})
    echo -e "    PID:    " $(green_font ${pid})

}

function start_goflyway(){
    [[ ! -z $(get_pid) ]] && echo -e "${Error} goflyway 正在运行 !" && exit 1

    [[ -e ${LogDir} ]] || {
        mkdir -p ${LogDir}
    }
    logFile="${LogDir}/goflyway_"$(date +%Y-%m-%d_%H-%M-%S)".log"
    ln -sf ${logFile} ${LogDir}/goflyway.log

    [[ $(which goflyway | wc -l) -eq 1 ]] || {
        echo "goflyway 不能启动"
        echo "检查 goflyway 安装路径"
        exit 1
    }

    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    goflywayPwd=$(ini_get_option_value ${ConfFile} "ServerConfig" "Passwd")
    nohup goflyway -k="${goflywayPwd}" -l=":${goflywayPort}" -U="kcp" > ${logFile} 2>&1 &

    echo "任务已经启动"

    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    add_port ${goflywayPort}

    get_config
}

function start_goflyway_pass_site(){
    [[ ! -z $(get_pid) ]] && echo -e "${Error} goflyway 正在运行 !" && exit 1

    [[ -e ${LogDir} ]] || {
        mkdir -p ${LogDir}
    }
    logFile="${LogDir}/goflyway_"$(date +%Y-%m-%d_%H-%M-%S)".log"
    ln -sf ${logFile} ${LogDir}/goflyway.log

    [[ $(which goflyway | wc -l) -eq 1 ]] || {
        echo "goflyway 不能启动"
        echo "检查 goflyway 安装路径"
        exit 1
    }

    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    goflywayPwd=$(ini_get_option_value ${ConfFile} "ServerConfig" "Passwd")
    nohup goflyway -k="${goflywayPwd}" -l=":${goflywayPort}" -proxy-pass="http://kernel.ubuntu.com/~kernel-ppa/mainline/" > ${logFile} 2>&1 &

    echo "任务已经启动"

    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    add_port ${goflywayPort}

    get_config
}
function stop_goflyway(){
    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    remove_port ${goflywayPort}

    pid=$(get_pid)

    if [[ -z ${pid} ]] ; then
        echo "goflyway 没有启动，无需停止"
    else
        echo "will stop ${pid}"
        kill -9 ${pid}
    fi

}

function delete_goflyway(){
    stop_goflyway
    goflywayPort=$(ini_get_option_value ${ConfFile} "ServerConfig" "Port")
    remove_port ${goflywayPort}

    echo "remove ${FinalDir}" && rm -rf ${FinalDir}

    echo "remove "$(dirname ${ConfFile}) && rm -rf $(dirname ${ConfFile})

    unlink  /usr/local/bin/goflyway


}
function exit_shell(){
    exit 0
}
#=================================================
#   Work
#=================================================
function list_available_task(){
    task_list=("安装 goflyway"  "更新 goflyway")

    declare -A task_array

    task_array["安装_goflyway"]=install_goflyway
    task_array["更新_goflyway"]=update_goflyway
    task_array["更新端口"]=update_port
    task_array["更新密码"]=update_password
    task_array["删除_goflyway"]=delete_goflyway
    task_array["启动_goflyway"]=start_goflyway
    task_array["启动_goflyway_pass_site"]=start_goflyway_pass_site
    task_array["查询_Config"]=get_config
    task_array["查询_Log"]=check_log
    task_array["停止_goflyway"]=stop_goflyway


    task_array["退出_Shell"]=exit_shell

#     task_list=(${!task_array[@]})
    task_list=("安装_goflyway" "更新_goflyway" "删除_goflyway" \
               "启动_goflyway" "启动_goflyway_pass_site" "停止_goflyway" \
               "更新端口" "更新密码" \
               "查询_Config" "查询_Log" \
               "退出_Shell")
    task_num=${#task_list[@]}

    while true
    do
        echo -e "请选择需要执行的任务"
        for((integer=0; integer<${task_num}; integer++))
        do
            echo -e  "\t" $(green_font ${integer}.) ${task_list[${integer}]}
        done
        stty erase '^H' && read -p "请输入数字 [0-$(expr ${task_num} '-' 1)]：" task_index

        if [[ $(check_number ${task_index}) -eq 0 ]] ; then

            [[ ${task_index} -lt 0 || ${task_index} -ge ${task_num} ]] && {
                echo "输入值: ${task_index}"
                echo "任务 index 超出范围，请重新输入"
                continue
            }
        else
            echo "输入值: ${task_index}"
            echo "任务索引必须为数字，请重新输入"
            continue
        fi


        ${task_array[${task_list[${task_index}]}]}
    done
}

function main(){
    check_sys
    check_installed


    list_available_task
}

main

