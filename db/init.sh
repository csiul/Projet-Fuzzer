#!/bin/sh
new_password=$(cat /run/secrets/db_root_password)
mysql -h localhost --user=root --password="$(cat /run/secrets/db_old_root_password)" -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('$new_password'); FLUSH PRIVILEGES;"
