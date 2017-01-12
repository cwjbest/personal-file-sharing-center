
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import web
import os
import time
import config
from urllib import quote
from pinyin import PinYin

# load config file
root = config.root
host = config.host

types = [
    ".h",".cpp",".cxx",".cc",".c",".cs",".html",".js",
    ".php",".java",".py",".rb",".as",".jpeg",".jpg",".png",
    ".gif",".ai",".psd",".mp3",".avi",".rmvb",".mp4",".wmv",
    ".mkv",".doc",".docx",".ppt",".pptx",".xls",".xlsx",
    ".zip",".tar",".gz",".7z",".rar",".pdf",".txt",".exe",
    ".apk",".torrent",".srt",".pyc"
]

render = web.template.render('template')

urls = (
    '/favicon.ico',"Ico",
    '/(.*)','Index',
)
class Ico:
    def GET(self):
        return open("static/img/favicon.ico").read()

def cmp(x,y):
    for i in xrange(0,len(x)):
        if 

def filenamesort(filelist):


class Index:
    def GET(self,path):
        # list all the files
        _path=path
        path = os.path.join(root, path)
        if not os.path.exists(path):
        	yield "文件不存在！"
        if os.path.isdir(path):
            flist = []
            item = os.listdir(path)`
            if not _path=='':
                # 返回上级
                temp={}
                temp['name']="上级目录"
                temp['type']="dir"
                temp["time"]=""
                temp["size"]=""
                temp["encode"]=host+os.path.dirname(_path)
                temp["iftag"]=True
                print "FPATH::",temp["encode"]
                flist.append(temp)
            for i in item:
                if i[0] == '.':
                    continue
                temp = {}
                temp['name'] = i
                temp['type'] = '.' + i.split('.')[-1]
                
                try:
                    types.index(temp['type'])
                except:
                    if os.path.isdir(os.path.join(path, i)):
                        temp['type'] = "dir"
                    else:
                        temp['type'] = "general"


                temp["time"] = time.strftime("%H:%M:%S %Y-%m-%d",
                        time.localtime(os.path.getmtime(os.path.join(path, i))))
                
                size = os.path.getsize(os.path.join(path, i))
                if size < 1024:
                    size = str(size) + ".0 B"
                elif size < 1024 * 1024:
                    size = "%0.1f KB" % (size/1024.0)
                elif size < 1024 * 1024 * 1024:
                    size = "%0.1f MB" % (size/1024.0/1024.0)
                else :
                    size = "%0.1f GB" % (size/1024.0/1024.0/1024.0)
                
                temp["size"] = size
                temp["encode"] = host+quote(os.path.join(_path, i).encode('utf-8'))
                temp["iftag"]=False

                flist.append(temp)
            
            yield render.layout(flist) 
        
        # return a file
        else:
            web.header('Content-Type','application/octet-stream')
            web.header('Accept-Ranges','bytes')
            web.header('Access-Control-Allow-Origin','#')
            web.header('Content-disposition', 'attachment; filename=%s' % os.path.split(_path)[1])
            size = os.path.getsize(os.path.join(root,path))
            web.header('Content-Length','%s' % size)
            with open(os.path.join(root,path)) as file:
                # 增加断点续传
                if web.ctx.env.get('HTTP_RANGE'):
                    web.ctx.status='206 Partial Content'
                    startp=int(web.ctx.env['HTTP_RANGE'].split('=')[1].split('-')[0])
                    file.seek(startp)
                for data in file:
                    yield data

    def DELETE(self,filename):
        try:
            filename = filename.encode('utf-8') 
            os.remove(os.path.join(root,filename))
        except:
            return "success" 


    def POST(self,filename):

        # save a file to disk
        x = web.input(file={})
        
        if 'file' in x:
            filepath= x.file.filename.replace('\','/')     # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]              # splits the and chooses the last part (the filename with extension)
            filename = unicode(filename, "utf8")
            fout = open(os.path.join(root,filename),'w')    # creates the file where the uploaded file should be stored
            fout.write(x.file.file.read())                  # writes the uploaded file to the newly created file.
            fout.close()                                    # closes the file, upload complete.
            
        return "<script>parent.location.reload()</script>" 

# start the application
# it's adaptable to both uwsgi start & python start
app = web.application(urls,globals())
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
    
