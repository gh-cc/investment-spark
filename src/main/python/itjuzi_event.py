# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import uniout
from pyquery import PyQuery as pq
#import csv
import os


# get the info from ITjuzi
class Spider:


    # init
    def __init__(self):
        self.siteURL = 'https://www.itjuzi.com/investevents?page='
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        #self.user_agent ="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER"
        self.headers = {'User-Agent': self.user_agent, 'Referer': "https://www.itjuzi.com/investevents"}



    # Get the info from specific investfirm page
    def getPage(self, pageIndex,writer):
        url = self.siteURL + str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        page= pq(response.read())
        events=page('ul').filter('.list-main-eventset').eq(1)

        for i in range(len(events('li'))):
            temp_events=events('li')[i]
            temp_events=pq(temp_events)('i')

            time=temp_events.eq(0).text()
            link=temp_events.eq(1)('a').attr('href')

            round = temp_events.eq(3).text()
            money=temp_events.eq(4).text()
            #investors=temp_events.eq(5).text()
            investors=''
            for j in range(len(pq(temp_events.eq(5))('a'))):
                print i,j
   
                if j==0:
                   investors=pq(temp_events.eq(5))('a').eq(0).text()
                else:
                   investors=investors+';'+pq(temp_events.eq(5))('a').eq(j).text()
                print investors

            for j in range(len(pq(temp_events.eq(5))('span').filter('.c-gray'))):
                print i,j
   
                if investors=='':
                   investors=pq(temp_events.eq(5))('span').filter('.c-gray').eq(0).text()
                else:
                   investors=investors+';'+pq(temp_events.eq(5))('span').filter('.c-gray').eq(j).text()
                print investors
            
            name=pq(events('p')[2*i]).text()
            kind = pq(events('p')[2 * i + 1])('span').eq(0).text()
            loc=pq(events('p')[2*i+1])('span').eq(1).text()


            #print time, name, kind, round,loc, money, investors, link

            # writer.write([time, name.encode("gb2312"), kind.encode("gb2312"), loc.encode("gb2312"),round.encode("gb2312"), money.encode("gb2312"), investors.encode("gb2312"), link.encode("gb2312")])
            # writer.write('\n')
            csvfile.write('{},{},{},{},{},{},{},{}\n'.format(time.encode('utf-8'),name.encode('utf-8'),kind.encode('utf-8'),round.encode('utf-8'),loc.encode('utf-8'),money.encode('utf-8'), \
                                           investors.encode('utf-8'),link))




csvfile = open('itjuzi_events.txt', 'ab+')
# csvfile.write('\xEF\xBB\xBF')
# writer = csv.writer(csvfile)
csvfile.write('融资时间,融资公司,公司的种类,融资的轮次,公司地址,融资金额, 投资方（以分号分割),链接\n')
page=Spider()
for i in range(1,1428):
    print i
    page.getPage(i,csvfile)


