#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


def db_createTable(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE "t1" (
    "id"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name"  TEXT,
    "age"   integer
    )''')
    c.close()

def db_insert(conn,table,fields,data):
    c = conn.cursor()
    # print("INSERT INTO %s (%s) VALUES (%s) "%(table,str(fields),str(data)))
    c.execute("INSERT INTO %s %s VALUES %s"%(table,str(fields),str(data)))
    # or
    # c.execute( 'insert into t1 (name,age) values(?,?)',('aa',1) ) ## 2D tupple 가능
    #
    conn.commit()
    c.close()

def db_delete(conn,table,whereClause=''):
    c = conn.cursor()
    if len(whereClause)==0:
        whereClause='1=2'
    c.execute("delete from %s where %s"%(table,whereClause))
    conn.commit()

def db_update(conn,table,col,val,whereClause=''):
    # print('----------------------------------------')
    # print("update %s set %s='%s' where %s"%(table,col,val,whereClause))
    c = conn.cursor()
    if len(whereClause)==0:
        whereClause='1=2'
    c.execute("update %s set %s='%s' where %s"%(table,col,val,whereClause))
    conn.commit()

def db_query(conn,table,whereClause=''):
    c = conn.cursor()
    if len(whereClause)==0:
        whereClause='1=1'
    # print("select * from %s where %s "%(table,whereClause))
    c.execute("select * from %s where %s "%(table,whereClause))
    rows = c.fetchall()
    c.close()
    return rows

def db_queryText(conn,text):
    c = conn.cursor()
    c.execute(text)
    rows = c.fetchall()
    c.close()
    return rows


def main():
    conn = sqlite3.connect("/Users/nowage/Dropbox/Data/Dash/dashSnippetsForJMac2017.dash")
    # #Create Table
    # db_createTable(conn)

    #Insert a row of data
    # fields=('Name','age')
    # data=('aa',12)
    # db_insert(conn,'t1',fields,data)

    # Query
    rows=db_query(conn,'tags')
    for i in rows:
        print(i)

    conn.close()


if __name__ == "__main__":
    main()
