# -*- coding:utf-8 -*-
import os
import re
import pymysql
import sys
import csv
import datetime

#from pandas import Series, DataFrame
#import pandas as pd

reload( sys )
sys.setdefaultencoding('utf-8')


# get the info from ITjuzi
class Write_data_db:

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,
                                    charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def create_firms_table(self,file_path):
        cur=self.__GetConnect()
        cur.execute('show tables;')

        #read the info from the file
        file=open(file_path,'ab+')
        i=0
        p=0
        for eachline in file:
            print i
            if i==0:
               i=i+1
               continue
            re_pattern = '^(.*);(.*);(.*);(.*);(.*);(.*);(.*);(.*);(.*);"(.*)\n*'
            result = re.findall(re_pattern, eachline)
            print result
            if len(result) == 0:
                pass
            else:
                p=p+1
                sql = "INSERT INTO `agency_invest` (`id`,`name`,`telephone`,`address`,`website`,`agency_des`,`inf_from`,`fund_count`,`round_rank`,`invest_area`) VALUES \
                      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(sql,(p,result[0][0],result[0][3],result[0][4],result[0][7],result[0][9],result[0][2],int(result[0][1]),result[0][8],result[0][6]))
                #cur.execute(sql)
                self.conn.commit()
            i=i+1
        cur.close()
    def write_fund_inf_table(self,file_path):
        cur=self.__GetConnect()
        cur.execute('show tables;')

        #read the info from the file
        file=open(file_path,'ab+')
        i=0
        p=0
        for eachline in file:
            print i
            if i==0:
               i=i+1
               continue
            re_pattern = '^(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)\n*'
            result = re.findall(re_pattern, eachline)
            print result
            if len(result) == 0:
                pass
            else:
                #temp_investfirm=re.sub(' ',',',result[0][6])
                firm_list=result[0][6].split(';')
                #print firm_list
                #print firm_list[0]
                #firm_list=list()
                #print result[0][6]
                for temp_firm in firm_list:
                    p=p+1
                    sql = "INSERT INTO `fund_inf` (`agency_name`,`company_name`,`fund_amount`,`round_rank`,`fund_time`,`inf_from`,`project`) VALUES \
                      (%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(sql,(temp_firm,result[0][1],result[0][5],result[0][3],result[0][0],result[0][7],result[0][2]))
                    #cur.execute(sql)
                    self.conn.commit()
            i=i+1
        cur.close()

    def fund_event_score(self,csv_file):

        #Define the rules
        #For invest rank, Pre-A: 10, A:9 B:8 C:7, D:6, IPO:5, Else:7
        #For invest times, 2714: 10,[20,2714):9,[11,20):8,[5,11):7,[2,5):6,[1,2):5
        #For investor fund time, 50年代以前10 60年代9 70年代8  80年代7  90年代6 00年5分；合计10分

        #read the count date from csv, caculate the mean

        #df=pd.read_csv(csv_file,names=['investor','number'])
        # max=df.max().number
        # min=df.min().number
        # median=df.median().number

        csvfile = open(csv_file, 'r')
        agency_count = dict()
        #reader = csvfile.reader(csvfile)
        for line in csvfile:
            print line
            #import  pdb
            #pdb.set_trace()
	    match=re.match('(\S+)\s*(\d+)',line)
	    if match != None:
               agency_name=match.group(1)
               agency_count[agency_name]=match.group(2)
	       print agency_name
	       print match.group(2)

        #Read the event_id/company_id/agency_name/agent_fund_time from db
        cur=self.__GetConnect()
        cur.execute('show tables;')
        company_list=list()
        for i in range(1,19714):
            sql='SELECT id,agency_name,company_name,round_rank,fund_time FROM fund_inf where id={};'.format(i)
            result=cur.execute(sql)
            #print result
	    #import pdb
	    #pdb.set_trace()
            #result=re.findall('^\|\s*(\d+)\s*\|\s*(\S*)\s*\|\s*(\S*)\s*\|\s*(\S*)\s*\|\s*(\S*)\s*\|',result)
            if result != 1:
                print "Error happened when execute the sql {}".format(sql)
            else:
	        temp_result=cur.fetchone()  
                id=temp_result[0]
                agency_name=temp_result[1]
                company_name=temp_result[2]
                round_rank =temp_result[3]
                fund_time = temp_result[4]
		print agency_count['和君资本']
		print agency_name.decode('utf-8')
                #import pdb
		#pdb.set_trace()
                if agency_count.has_key(agency_name.encode('utf-8')):
                    invest_count=int(agency_count[agency_name.encode('utf-8')])
                else:
                    invest_count=1

                #get the invest count score
                if invest_count>=1 and invest_count<2:
                    invest_score=5
                elif invest_count>=2 and invest_count<5:
                    invest_score = 6
                elif invest_count>=5 and invest_count<11:
                    invest_score = 7
                elif invest_count>=11 and invest_count<20:
                    invest_score = 8
                elif invest_count>=20 and invest_count<2794:
                    invest_score = 9
                else:
                    invest_score = 10

                #get the rank score
                if round_rank == 'Pre-A轮':
                    rank_score= 10
                elif round_rank == 'A轮':
                    rank_score=9
                elif round_rank == 'B轮':
                    rank_score=8
                elif round_rank == 'C轮':
                    rank_score=7
                elif round_rank == 'D轮':
                    rank_score=6
                elif round_rank == 'IPO':
                    rank_score=5
                else:
                    rank_score=7

                #Get the found time score
                #time_match=re.match('(\d+)-(\d+)-(\d+)',fund_time)
                if isinstance(fund_time,datetime.date) != True:
                    time_score=5
                else:
                    #year=int(time_match.group(1))
                    if fund_time.year<1960:
                        time_score=10
                    elif fund_time.year<1970 and fund_time.year >= 1960:
                        time_score=9
                    elif fund_time.year < 1980 and fund_time.year >= 1970:
                        time_score = 8
                    elif fund_time.year < 1990 and fund_time.year >= 1980:
                        time_score = 7
                    elif fund_time.year < 2000 and fund_time.year >= 1990:
                        time_score = 6
                    else:
                        time_score = 5

                print invest_score,rank_score,time_score
                total_score=invest_score * 0.5 + rank_score * 0.4 + time_score*0.1
                print total_score
                if company_name in company_list:
		   company_id=company_list.index(company_name)+1
		else:
		   company_list.append(company_name)
		   company_id=len(company_list)
                sql = "INSERT INTO `score` (`id`,`agency_id`,`company_id`,`score`) VALUES \
                  (%s,%s,%s,%s)"
                cur.execute(sql, (id,id, company_id, total_score))
		sql = "INSERT INTO `company` (`id`,`name`) VALUES (%s,%s)"
		cur.execute(sql, (id,company_name))
                # cur.execute(sql)
		#import pdb
		#pdb.set_trace()
                self.conn.commit()
        cur.close()

db_info={'host':'localhost','user':'root','pwd':'root','db':'investmentdb'}
write_db=Write_data_db(db_info['host'],db_info['user'],db_info['pwd'],db_info['db'])
#file_path='itjuzi_firms_worked.txt'
# file_path='itjuzi_events.txt'
# write_db.write_fund_inf_table(file_path)
file_path='tz_num1.txt'
write_db.fund_event_score(file_path)
