# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import uniout
import os
import sys
reload( sys )
sys.setdefaultencoding('utf-8')

# get the info from ITjuzi
class Spider:


    # init
    def __init__(self):
        self.siteURL = 'https://www.itjuzi.com/investfirm?page='
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.headers = {'User-Agent': self.user_agent, 'Referer': "https://www.itjuzi.com/investfirm"}
    # Get the info from specific investfirm page
    def getPage(self, pageIndex):
        url = self.siteURL + str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    #Get the firm/lable/link/description/events/action from the page
    def getContents(self,pageIndex,writer):
        page=self.getPage(pageIndex)
        re_link=re.compile('<i class="cell pic">\s*<a href="([^"]*)">',re.S)
        link_list=re.findall(re_link,page)
      

        # re_lable=re.compile('<img src="([^"]*)"></span>',re.S)
        # lable_list=re.findall(re_lable,page)
        # print lable_list

        re_name=re.compile('<p class="title"><a href="[^"]*"><span>([^<]*)</span></a></p>',re.S)
        name_list=re.findall(re_name,page)
        change_name_list=list()
        for temp_name in name_list:
            if isinstance(temp_name,unicode):
               print temp_name
               change_name_list.append(temp_name)               
       
            else:
                         
               print temp_name.decode('utf8')
               change_name_list.append(temp_name.decode('utf8'))
        #print change_name_list

        re_des=re.compile('<p class="des"><span>([^<]*)</span></p>',re.S)
        des_list = re.findall(re_des, page)
        change_des_list=list()
        print change_des_list
        for temp_des in des_list:
            if isinstance(temp_des,unicode):
               print temp_des
               change_des_list.append(temp_des)
               
            else:
               temp_des
               print '11',temp_des
               print temp_des.decode('utf8')
               change_des_list.append(temp_des.decode('utf8'))          
        print change_des_list

        re_event = re.compile('<i class="cell fina">(\d*)\S*</i>',re.S)
        event_list = re.findall(re_event, page)
        change_event_list=list()
        for temp_event in event_list:
            print temp_event.decode('utf8')
            change_event_list.append(temp_event.decode('utf8'))
        print change_event_list

        cwd=os.getcwd()
        for i in range(len(change_name_list)):
            temp_name=change_name_list[i]
            temp_link=link_list[i]
            temp_event=change_event_list[i]
            temp_des=change_des_list[i]
            if temp_event =='':
               temp_event=str(0)
            image_path=os.path.join(cwd,'firm_img/{}.jpg'.format(temp_name.encode('utf-8')))
            temp_firm_list=self.getInvestfirm(temp_link,image_path)
            writer.write('{};{};{};{};{};{};{};{};{};{}\n'.format(temp_name.encode('utf-8'), temp_event.encode('utf-8'),temp_link.encode('utf-8'),\
                          temp_firm_list[0],temp_firm_list[1].encode('utf8'),temp_firm_list[2],temp_firm_list[3].encode('utf8'),\
                          temp_firm_list[4],temp_firm_list[5].encode('utf8'),temp_des.encode('utf-8')))
            #image_path=os.path.join(cwd,'invest_firm_lable/{}.jpg'.format(temp_name))



    #Get the investfirm lable
    def getLable(self,lable_link,file_path):

        request = urllib2.Request(lable_link, headers=self.headers)
        response = urllib2.urlopen(request)
        f = open(file_path, 'wb')
        f.write(response.read())

    #Get the investfirm information
    def getInvestfirm(self,firm_link,image_path):
        request = urllib2.Request(firm_link,headers=self.headers)
        page = urllib2.urlopen(request).read()

        firm_info=list()
        #print page
        #Get the description
        # re_des = re.compile('<div class="block block-inc-info">\s*<div class="des">\s*([^<]*)\s*</div>', re.S)
        # des = re.findall(re_des, page)
        # print des
        #Get the phone
        re_phone = re.compile('<li>\s*<i class="fa fa-phone"></i>\s*<span>([^<]*)</span>', re.S)
        phone=re.findall(re_phone, page)
        if len(phone):
           phone=phone[0]
           
        else:
           phone='N/A'
        firm_info.append(phone)


        #Get the location
        re_loc = re.compile('strong>([^<]*)</strong><br>\s*<span class="c-gray t-small">([^<]*)</span><br>', re.S)
        loc=re.findall(re_loc, page)
        
        if len(loc):
           loc=loc[0]
           temp_loc=loc[0].decode('utf-8')
           for i in range(1,len(loc)):
               temp_loc=temp_loc+','+loc[i].decode('utf8')
           loc=temp_loc
    
           
        else:
           loc='N/A'
        firm_info.append(loc)        

        #Get the lable
        re_lable_link = re.compile('<div class="pic ">\s*<img src="([^>]*)">\s*</div>', re.S)
        lable_link = re.findall(re_lable_link, page)
        if len(lable_link):
           lable_link=lable_link[0]
           try:
              self.getLable(lable_link,image_path)
           except:
              lable_link='N/A'
        else:
           lable_link='N/A'
        firm_info.append(lable_link)
        


        # Get the invest scope
        #'<a href="https://www.itjuzi.com/investfirm?invst_scope=3"><b class="tag">医疗健康</b></a>'

        re_scope = re.compile('<a href="https://www.itjuzi.com/investfirm\?invst_scope=\d*"><b class="tag">([^<]*)</b></a>', re.S)
        scope=re.findall(re_scope, page)
        if len(scope):
           temp_scope=scope[0].decode('utf-8')
           for i in range(1,len(scope)):
               temp_scope=temp_scope+','+scope[i].decode('utf8')
           scope=temp_scope
        else:
           scope='N/A'
        firm_info.append(scope)


        #Get the link'网址：'
        re_link = re.compile("\xe7\xbd\x91\xe5\x9d\x80\xef\xbc\x9a([^<]*)/</a>", re.S)
        link=re.findall(re_link, page)
        if len(link):
           link=link[0]
        else:
           link='N/A'
        firm_info.append(link)

        #Get the invest round
        re_round= re.compile('<a href="https://www.itjuzi.com/investfirm\?invst_state=\d*"><b class="tag">([^<]*)</b></a>', re.S)
        round=re.findall(re_round, page)
        if len(round):
           temp_round=round[0].decode('utf-8')
           for i in range(1,len(round)):
               temp_round=temp_round+','+round[i].decode('utf8')
           round=temp_round
        else:
           round='N/A'
        firm_info.append(round)


        #Get the members
        
        print firm_info
        return firm_info

page=Spider()
txtfile = open('itjuzi_firms.txt', 'ab+')
#txtfile.write('机构名称;投资次数;桔子链接;电话;地址;图标链接;投资领域;网站链接;投资轮次;机构简介\n')
# page=Spider()
for i in range(1,6880):
     print i
     page.getContents(i,txtfile)
#page.getContents(1)
#page.getInvestfirm('https://www.itjuzi.com/investfirm/6450','try.jpg')
