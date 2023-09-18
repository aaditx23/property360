#!/bin/bash

run_mysql(){
    echo a | sudo -S su
    sudo systemctl start mariadb.service
    echo "Started mariadb"
    sudo mysql -u root
    echo "Stopping mariadb..."
    sudo systemctl stop mariadb.service
    echo "Stopped mariadb."
    exit
}
run_mysql
