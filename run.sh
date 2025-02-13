#!/bin/bash

eval "$(/root/anaconda3/bin/conda shell.bash hook)"
cd /root/magazines_spider
conda activate spider

currentdate=$(date +%Y%m%d)
logpath="./log/"
logname=$logpath$currentdate."log"
if [ -e $logname ];then
  touch $logname
fi

beforeNum1=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use magazines; select count(*) from magazines where pure_download_links is not null"`
beforeNum2=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use courses; select count(*) from courses"`

scrapy crawl magazines
scrapy crawl cleanDownloadLinks >> $logname 2>&1
scrapy crawl link-ai >> $logname 2>&1
scrapy crawl itcourses

# send message
afterNum1=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use magazines; select count(*) from magazines where pure_download_links is not null"`
afterNum2=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use magazines; select count(*) from courses"`
subNum1=`expr $afterNum1 - $beforeNum1`
subNum2=`expr $afterNum2 - $beforeNum2`
title="add-magazine:$subNum1-courses:$subNum2."
URL="https://sctapi.ftqq.com/SCT256309T8D6Sn2WpIVzGDELwhYaUQo2h.send?title=$title"
entireURL="curl -X POST $URL"
eval $entireURL
