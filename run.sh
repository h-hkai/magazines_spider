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

beforeNum=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use magazines; select count(*) from magazines where pure_download_links is not null"`

scrapy crawl magazines
scrapy crawl cleanDownloadLinks >> $logname 2>&1
scrapy crawl link-ai >> $logname 2>&1
scrapy crawl itcourses

# send message
afterNum=`mysql -uroot -h127.0.0.1 -p"12345678" -Bse "use magazines; select count(*) from magazines where pure_download_links is not null"`
subNum=`expr $afterNum - $beforeNum`
title="magazine-update:-add-$subNum-journals."
URL="https://sctapi.ftqq.com/SCT256309T8D6Sn2WpIVzGDELwhYaUQo2h.send?title=$title"
entireURL="curl -X POST $URL"
eval $entireURL
