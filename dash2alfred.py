# -*- coding: utf-8 -*-
import sqlite3
import sqliteNowage.sqlite as d
import sys, os
from os.path import join,isfile,isdir
import json
import uuid

suffixKey = {
    "–": '–',
    "FUNDAMENTAL": '∆',
    "FUNDAMENTAL-hangul": '˚',
    "emoji": ',–',
    "symbol": ',,',
    "TEMPORARY": '.,'
}
plistTemplate = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>snippetkeywordprefix</key>
    <string></string>
    <key>snippetkeywordsuffix</key>
    <string>%s</string>
</dict>
</plist>
    '''

str_SnippetJson="""{
      "alfredsnippet" : {
        "snippet" : "%s",
        "uid" : "%s",
        "name" : "%s",
        "keyword" : "%s"
      }
    }
    """

sql_getSnippet="""select 
    s.title,s.body
from 
    snippets s,
    tags t,
    tagsIndex ti
where s.sid=ti.sid
  and ti.tid=t.tid
  and t.tag='%s'
"""

def getSnippetJson(snippetBody, snippetName, uuidStr):
    snippetBody = snippetBody.replace("\\", "\\\\")
    snippetBody = snippetBody.replace("\"", "\\\"")
    snippetBody = snippetBody.replace("\n", "\\n")
    snippetBody = snippetBody.replace("\r", "\\n")

    snippetBody=snippetBody.replace("<","\u003C")
    snippetBody = snippetBody.replace(">", "\u003E")
    snippetBody = snippetBody.replace("\t", "  ") # tab
    # snippetBody = snippetBody.replace(" ", "\u0020") # space

    snippetBody = snippetBody.replace("[", "\u005B")
    snippetBody = snippetBody.replace("]", "\u005D")
    snippetBody = snippetBody.replace(";", "\u003B")
    snippetBody = snippetBody.replace("\.", "\\.")
    snippetBody = snippetBody.replace("\*", "\\*")
    snippetBody = snippetBody.replace("\\\\‘", "x")
    snippetBody = snippetBody.replace("\\\|", "\\\\|")

    return str_SnippetJson % (snippetBody, uuidStr, snippetName, snippetName)

def getSuffix(collectionName):
    return suffixKey[collectionName] if collectionName in suffixKey.keys() else "–"

def createCollectionFolderAndPlist(conn,alfredPath,suffixKey):
    if not isdir(alfredPath):
        print("No Path : " + alfredPath )
        exit()
    collections = d.db_query(conn, 'tags')
    collections=[r[1] for r in collections]
    for i in collections:
        collectionName=i
        directory = alfredPath + collectionName +"/"
        # print(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+"info.plist", 'w') as f:
            f.write(plistTemplate % (getSuffix(collectionName)))
    return collections

def main(dashDbPath, alfredPath):

    conn = sqlite3.connect(dashDbPath)    # #Create Table

    # 1. Create Folder and plist file

    collections=createCollectionFolderAndPlist(conn,alfredPath,suffixKey)

    # 2. create Snippet File
    cnt=0
    for collection in collections:
        snippets=d.db_queryText(conn,sql_getSnippet%collection)
        for s in snippets:
            snippetBody = s[1]
            snippetName = s[0]
            suffix=getSuffix(collection)
            snippetName = s[0].rstrip(suffix)
            uuidStr=uuid.uuid4()
            snippetJson=getSnippetJson(snippetBody, snippetName, uuidStr)
            fname=alfredPath+collection+"/"+snippetName +" ["+str(uuidStr)+"].json"
            if collection=='emoji':
                print(snippetBody,snippetName,suffix)
                print(fname)
            with open(fname,'w') as f:
                f.write(snippetJson)
            # if cnt>100:
            #     exit()
            # else:
            #     cnt+=1





    conn.close()


usage = ''' 
python superResolution.py {images_path} {images_super_path} 
example: 

    python dash2alfred.py                                    \
      /Users/nowage/Dropbox/Data/Dash/dashSnippetsForJMac2017.dash \
      /Users/nowage/Dropbox/Data/Alfred3/Alfred.alfredpreferences/snippets/
'''

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(usage)
    else:
        print('dashDbFilePath       :', sys.argv[1]    )
        print('alfredFolderPath :', sys.argv[2]    )
        dashDbPath       = sys.argv[1]
        alfredPath = sys.argv[2]
        main(dashDbPath, alfredPath)
    print('ok...^^')
