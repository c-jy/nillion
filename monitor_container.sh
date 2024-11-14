#!/bin/bash

#wget -O monitor_container.sh https://raw.githubusercontent.com/c-jy/nillion/refs/heads/main/monitor_container.sh && sed -i 's/\r//' monitor_container.sh && chmod +x monitor_container.sh && sudo nohup ./monitor_container.sh > monitor_log.log 2>&1 &


# 确保脚本以 root 权限运行
if [ "$(id -u)" -ne "0" ]; then
  echo "请以 root 用户或使用 sudo 运行此脚本"
  exit 1
fi

sleep_time=500
env=$1
function main() {
    while true; do
        container_monitor

        sleep $sleep_time # 检查间隔，这里是5分钟
    done
}

function container_monitor() {
    container_name="nillion_verifier"
    
    # 检查容器是否存在
    if [ "$(docker ps -q -f name=$container_name)" ]; then
        # docker logs -f ${container_name} --tail 100
        echo "$env 服务器 $container_name 正常运行，等待 $sleep_time 秒后重新查询"
    else
        send_msg "$env 服务器容器 $container_name 未运行，重新启动容器"
        docker start $container_name
        # sudo docker stop nillion_verifier
        # sudo docker start -d --name nillion_verifier
        sleep 2
        if [ "$(docker ps -q -f name=$container_name)" ]; then
            echo "$container_name 正常启动，等待 $sleep_time 秒后重新查询"
        else
            send_msg "$env 服务器 $container_name 启动失败启动，请检查gas是否不足或登录后台检查原因"
        fi
    fi
}

function send_msg() {
    echo $1
    curl -X POST -H "Content-Type: application/json" -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"nillion $1\"}}" https://open.feishu.cn/open-apis/bot/v2/hook/99c1aa52-0568-420a-b337-4946fa4814d7
}

main 