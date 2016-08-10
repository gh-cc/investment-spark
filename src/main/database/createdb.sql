#create db and tables ubantu: $ sudo mysql -uroot -proot < "/home/ubuntu/spark/createdb.sql"
#begin create database
drop database if exists investmentdb;
create database investmentdb default character set utf8 collate utf8_general_ci;
use investmentdb;

#begin create tables
create table if not exists agency_invest(
id int primary key not NULL auto_increment,
name varchar(100) not NULL,
telphone varchar(20) default NULL,
address varchar(150) default NULL,
website varchar(100) default NULL,
agency_des varchar(500) default NULL,
inf_from varchar(100) default NULL,
fund_count int default 0,
round_rank varchar(150) default NULL,
invest_area varchar(200) default NULL,
register_capital varchar(100) default NULL,
create_time date default NULL,
register_place varchar(100) default NULL,
manager varchar(150) default NULL,
stockholder varchar(200) default NULL
)engine =innodb auto_increment=1 default charset=utf8;

create table if not exists company(
id int primary key not NULL auto_increment,
name varchar(100) not NULL,
field_type varchar(50) default NULL,
address varchar(150) default NULL,
found_time date default NULL,
register_capital varchar(100) default NULL,
stockholder varchar(200) default NULL,
team varchar(400) default NULL,
round_rank varchar(150) default NULL
)engine =innodb auto_increment=1 default charset=utf8;

create table if not exists fund_inf(
id int primary key not NULL auto_increment,
agency_name varchar(100)  default NULL,
leaderorfollow int  default 2,
company_name  varchar(100)   default NULL,
fund_amount  varchar() default 0.0,
round_rank varchar(50) default NULL,
fund_time date default NULL,
inf_from varchar(100) default NULL,
project varchar(200) default NULL
)engine =innodb auto_increment=1 default charset=utf8;

create table if not exists investor(
id int primary key not NULL auto_increment,
agency_name  varchar(100) default NULL,
education_back varchar(50) default NULL,
sex tinyint default NULL,
age int default NULL,
work_experience varchar(400) default NULL,
position varchar(80) default NULL,
invest_experience varchar(300) default NULL
)engine =innodb auto_increment=1 default charset=utf8;

create table if not exists entrepreneur(
id int primary key not NULL auto_increment,
company_name varchar(100)  default NULL,
education_back varchar(50) default NULL,
sex tinyint default NULL,
age int default NULL,
work_experience varchar(400) default NULL,
family_back  varchar(150) default NULL,
venture_experience varchar(300) default NULL
)engine =innodb auto_increment=1 default charset=utf8;

create table if not exists score(
id int primary key not null auto_increment,
agency_id   int  not null,
company_id  int  not null,
score   double  default 0.0
)engine =innodb auto_increment=1 default charset=utf8;


create table if not exists agencyinvestcount(
id int primary key not null auto_increment,
count_invest  int  default null,
name_agency   varchar(100)  not null
)engine =innodb auto_increment=1 default charset=utf8;


create table if not exists recommresult(
id int primary key not null auto_increment,
company_id  int  default null,
agency_id  int  default  null,
score  double default 0.0
)engine =innodb auto_increment=1 default charset=utf8;