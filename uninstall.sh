#!/bin/bash

# uninstall.sh

# Created by Hager Hu on 2012-12-21.
# Copyright (c) 2012 hagerhu.com. All rights reserved.

crontab_list=`crontab -l`
echo "result:$? info:\n$crontab_list"

if [ $? -eq 0 ]
then
	echo "cron job exists"
	
	echo "do remove operation === start"
	crontab_remove=`crontab -r`

	if [ $? -eq 0 ]
	then
		echo "uninstall successed"
	else
		echo "uninstall failed"
	fi
	echo "do remove operation === end"
else
	echo "cron job doesn't exist, no need to remove"
fi


echo "remove install path in the user home"

INSTALL_PATH="$HOME/.name_service.yml"

if [ -e $INSTALL_PATH ]
then
	rm $INSTALL_PATH
else
	echo "no name service existed"
fi


if [ $? -eq 0 ]
then
	echo "remove the name service file successed"
else
	echo "unable to remove name service file"
fi