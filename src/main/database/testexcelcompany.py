# -*- coding:utf-8 -*-
import os
import re
import pymysql
import xlrd
import sys
reload( sys )
sys.setdefaultencoding('utf-8')

# Open the workbook and define the worksheet
book = xlrd.open_workbook("/home/ubuntu/spark/companytest1.xlsx")
sheet = book.sheet_by_name("Sheet1")
#创建数据库连接
database = pymysql.connect(host="localhost", user = "root", passwd = "root", db = "investmentdb", charset="utf8")
#获得游标
cursor = database.cursor()
#创建插入语句，并与excel中的column对应
query = """INSERT INTO company(name,field_type,address,found_time,register_capital,stockholder,team,round_rank) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
#遍历excel所有行
for r in range(1, sheet.nrows):
      name = sheet.cell(r,0).value
      field_type = sheet.cell(r,1).value
      address = sheet.cell(r,2).value
      found_time =sheet.cell(r,3).value
      register_capital = sheet.cell(r,4).value
      stockholder = sheet.cell(r,5).value
      team = sheet.cell(r,6).value
      round_rank = sheet.cell(r,7).value
      values = (name,field_type,address,found_time,register_capital,stockholder,team,round_rank)
    #执行一行插入一次
      cursor.execute(query, values)
#关闭游标
cursor.close()
#提交整个插入数据事务
database.commit()
#数据连接关闭
database.close()
#任务结束标识反馈
print "Done!"