#!/bin/bash
# bash script for install cron job
# for auto updating domain dns record

# install.sh

# Created by Hager Hu on 2012-12-21.
# Copyright (c) 2012 hagerhu.com. All rights reserved.


CRON_JOB_TXT="cron_job_domain.txt"
INET_ADDRESS_FILE="InetAddress.py"

echo "current:$PWD user_home:$HOME"
echo "store install path in file"

INSTALL_PATH="$HOME/.name_service.yml"
if [ ! -e $INSTALL_PATH ]; then
	touch $INSTALL_PATH
fi

RESULT=`echo "service_dir: $PWD" > $INSTALL_PATH`
echo "result:$?"
echo "store install path in file successed"

CRON_JOB="$PWD/$CRON_JOB_TXT"
if [ ! -e $CRON_JOB ]; then
	#echo "create cron job file"
	touch $CRON_JOB
fi

echo "cron_job_file:$CRON_JOB"

echo "write cron job content to the file"
ADDRESS_FILE="$PWD/$INET_ADDRESS_FILE"
WRITE=`echo "*/5 * * * * python $ADDRESS_FILE" > $CRON_JOB`
echo "write:$?"

CRONTAB=`crontab $CRON_JOB`
#echo "exit:$?"

if [ $? -eq 0 ]; then
	echo "cron job install successed"
fi