import pymysql.cursors
from os import environ

#Establishing Database Connection - Using ENV
MYSQL_USER=environ['MYSQL_USER']
MYSQL_PASSWORD=environ['MYSQL_PASSWORD']
MYSQL_HOST=environ['MYSQL_HOST']
MYSQL_DATABASE=environ['MYSQL_DATABASE']


connection = pymysql.connect(
    host = MYSQL_HOST , 
    user = MYSQL_USER ,
    passwd= MYSQL_PASSWORD , 
    db = MYSQL_DATABASE ,
    port=3306
)
