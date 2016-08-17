# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import uniout
import os
import sys
import csv
from pyquery import PyQuery as pq
reload( sys )
sys.setdefaultencoding('utf-8')


# get the info from ITjuzi
class Spider:


    # init
    def __init__(self):
        self.siteURL = 'https://www.itjuzi.com/investor?page='
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers = {'User-Agent': self.user_agent, 'Referer': "https://www.itjuzi.com/investor"}
    # Get the info from specific investfirm page
    def getPage(self, pageIndex):
        url = self.siteURL + str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    #Get the firm/lable/link/description/events/action from the page
    def getivestorlist(self,pageIndex,writer):
        page=self.getPage(pageIndex)
        print page

        #page='<a target="_blank" href="https://www.itjuzi.com/investor/3917" class="name">侯景超</a></br>'
        re_link=re.compile('<a target="_blank" href="([^"]*)" class="name">([^<]*)</a></br>',re.S)
        link_list=re.findall(re_link,page)
        print link_list

        #page='<span class="des"><a target="_blank" href="https://www.itjuzi.com/investfirm/6480">名盛资本</a> · 投资经理</span>'
        re_info=re.compile('<span class="des"><a target="_blank" href="https://www.itjuzi.com/investfirm/\d*">([^<]*)</a> · ([^<]*)</span>',re.S)
        info_list=re.findall(re_info,page)
        print info_list

        #cwd=os.getcwd()
        for i in range(len(link_list)):
            temp_link=link_list[i]
            page_link=temp_link[0]
            investor_name=temp_link[1]

            print temp_link,investor_name
            temp_info=self.getinvestor(page_link)
            writer.writerow([investor_name,temp_info[8],temp_info[9],temp_info[0],temp_info[1],temp_info[3],temp_info[2],temp_info[6],temp_info[7],temp_info[5],temp_info[4]])
            #writer.write('{};{};{};{}\n'.format(temp_name.encode('utf-8'), temp_event.encode('utf-8'),temp_link.encode('utf-8'), temp_des.encode('utf-8')))
            #image_path=os.path.join(cwd,'invest_firm_lable/{}.jpg'.format(temp_name))

    def getinvestor(self,investor_link):
        request = urllib2.Request(investor_link,headers=self.headers)
        page = urllib2.urlopen(request).read()


        #Get the location info

        gene_info=list()

        re_loc=re.compile('<a href="https://www.itjuzi.com/investor\?prov=.*">([^"]*)</a> · (\S*)\s*</p>',re.S)
        loc_info=re.findall(re_loc,page)
        if len(loc_info):
            loc_city=loc_info[0][0]
            loc_area=loc_info[0][1]
        else:
            loc_city='N/A'
            loc_area='N/A'

        re_title=re.compile('<a href="https://www.itjuzi.com/investfirm/\d+">([^"]*)</a> · (\S*)\s*</span>',re.S)
        title_info=re.findall(re_title,page)
        if len(title_info):
            info_company=title_info[0][0]
            info_title=title_info[0][1]
        else:
            info_company='N/A'
            info_title='N/A'
        #from bs4 import BeautifulSoup
        #soup=BeautifulSoup(page,'lxml')
        #print soup.prettify()

        # import pdb
        # pdb.set_trace()

        page = pq(urllib2.urlopen(request).read())
        events = page('div').filter('.main').eq(0)

        invest_info=pq(events)('div').filter('.pad.block').eq(0).text()
        invest_info = re.findall(u'\u6295\u8d44\u9636\u6bb5\s*(.*)\s*\u6295\u8d44\u9886\u57df\s*(.*)', invest_info)
        invest_phase=invest_info[0][0]
        invest_area = invest_info[0][0]

        intro_info=pq(events)('div').filter('.pad.block').eq(1).text()
        invest_company=pq(events)('div').filter('.right').text()
        work_experience=pq(events)('div').filter('.wp100.ofa.hscroll').eq(0).text()
        edu_info=pq(events)('div').filter('.wp100.ofa.hscroll').eq(1).text()

        gene_info.append(loc_city)
        gene_info.append(loc_area)
        gene_info.append(invest_phase)
        gene_info.append(invest_area)
        gene_info.append(intro_info)
        gene_info.append(invest_company)
        gene_info.append(work_experience)
        gene_info.append(edu_info)
        gene_info.append(info_company)
        gene_info.append(info_title)

        tran_list=list()
        for temp in gene_info:
            if temp == '':
                temp='未收录相关信息'
            tran_list.append(temp)

        print tran_list
        return tran_list






page=Spider()
csv_file = open('itjuzi_investors.csv', 'ab+')
writer=csv.writer(csv_file)
writer.writerow(['investor_name','company_name','investor_title','investor_city','investor_are','invest_phase','invest_area','work_experience','education_info','invest_company','introduction'])
# page=Spider()
for i in range(1,245):
    print i
    page.getivestorlist(i,writer)
#page.getivestorlist(2,'ll')
#page.getinvestor('https://www.itjuzi.com/investor/12')
#page.getInvestfirm('https://www.itjuzi.com/investfirm/6458','try.jpg')
