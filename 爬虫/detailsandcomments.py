# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:04:40 2020

@author: lenovo
"""

import requests
from lxml import etree
import os                  #os模块可以控制文件输入输出，这里用它可以新建文件夹
import csv
import json
import random
import time
import json
import re


def GetHTML(url):
    #反爬虫chrome
    #headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
    try:
        headers1 = {}
        proxiesc = {}
        
        proxies1 =['http://39.83.155.70:80',
                  'http://182.90.40.239:80',
                  'http://27.14.61.188:8080',
                  'http://121.31.75.74:8123',
                  'http://111.176.155.209:3128',
                  'http://121.31.192.11:8123',
                  'http://49.118.245.32:8090',
                  'http://119.48.175.15:8090',
                  ]
        proxies2 =['http://114.224.132.214:8090',
                  'http://27.215.2.2:8090',
                  'http://182.88.4.205:8123',
                  'http://61.184.58.118:3128',
                  'http://171.37.133.64:8123',
                  'http://171.37.154.26:8123',
                  'http://183.23.219.219:8090',
                  'http://110.152.241.50:8090',
                  ]
        proxies3 =['http://183.185.1.6:8090',
                  'http://123.232.177.196:8090',
                  'http://27.12.195.121:8090',
                  'http://171.39.27.94:8123',
                  'http://59.55.250.94:8090',
                  'http://111.182.190.119:3128',
                  'http://182.88.28.204:8123',
                  'http://171.38.135.36:8123',
                  ]      
        
        headers=[
            'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36',
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"
             ] 
        """
        proxies4 =['http://112.195.155.165:80',
                  'http://171.37.161.195:8123',
                  'http://180.175.3.27:63000',
                  'http://110.73.34.11:8123',
                  'http://49.118.184.107:8090',
                  'http://27.9.157.94:8090',
                  'http://119.166.43.8:8080',
                  'http://113.7.130.59:80',
                  ]
        """
        proxies4 =['http://120.1.14.23:6675',
                  'http://112.243.248.167:6675',
                  'http://113.232.140.109:6675',
                  'http://116.112.247.106:6668',
                  'http://112.234.254.193:6675',
                  'http://122.82.217.203:6675',
                  'http://182.40.173.248:6675',
                  'http://61.53.157.210:6675',
                  ]
        
        header = random.choice(headers)
        headers1['User-Agent']=header
        """
        urlss = 'http://proxy.httpdaili.com/apinew.asp?sl=20&noinfo=true&ddbh=1016284544036985252'
        s=requests.get(urlss,headers=headers1)
        #print(s.text)
        proxies = s.text.split('\n') 
        proxies=[j.replace('\r','').strip() for j in proxies]
        """
        #proxie = random.choice(proxies)
        ccn = random.randint(1,5)
        if ccn == 1:
            proxie = random.choice(proxies1)
        elif ccn == 2:
            proxie = random.choice(proxies2)
        elif ccn == 3:
            proxie = random.choice(proxies3)
        else:
            proxie = random.choice(proxies4)
        
        proxiesc['http']=proxie
        #print(headers1)
        ran = random.randint(1,5)
        #print(proxiesc)
        time.sleep(ran*3)
        #proxie = random.choice(proxies)
        #print(str(header)+"----"+str(proxie))
        r=requests.get(url,headers=headers1,proxies=proxiesc)
        r.raise_for_status()
        r.encoding='utf-8'
        #time.sleep(3)
        #r.encoding=r.apparent_encoding
        return r.text
    except:
        return None
    
#进入图书详情页
def bookdetail(book_url):
    global data
    #申明字典存储信息
    book_detail = {}
    book_detail['BookID']='NULL'
    book_detail['BookImage']='NULL'
    book_detail['BookName']='NULL'
    book_detail['BookPress']='NULL'
    book_detail['BookProducer']='NULL'
    book_detail['Bookauthor']='NULL'
    book_detail['BookTranslator']='NULL'
    book_detail['Bookdetail']='NULL'
    book_detail['BookYear']='NULL'
    book_detail['BookPages']='NULL'
    book_detail['BookISBN']='NULL'
    book_detail['BookScore']='NULL'
    book_detail['BookPeople']='NULL'
    #图书id：
    fenci = book_url.split('/')
    bookid = fenci[len(fenci)-2]
    #bookids.append(bookid)
    book_detail['BookID'] = str(bookid)
    
    #进入详情页：
    count = 1
    response = GetHTML(book_url)
    if response == None:
        response = GetHTML(book_url)
        count+=1
        if(count == 10):
            return "down error"
        
    #print(response)
    selector = etree.HTML(response)
    
    #time.sleep(10)
    
    #书名：
    bookname = selector.xpath('//div[@id="wrapper"]/h1/span[@property="v:itemreviewed"]/text()')
    if(len(bookname)!=0):
        book_detail['BookName'] = bookname[0]
        """
        if str(bookname[0]) in data:
            return "already down"
        else:
            with open ('name.txt','a+',encoding='utf-8') as txtfile:
                txtfile.write("'"+str(bookname[0])+"'" + "：'小说',")
        """
    else:
        book_detail['BookName'] = "NULL"
    
    #图片链接：
    #imageurl=selector.xpath('//div[@id="wrapper"]/div[@class="indent"]/div[@class="subject clearfix"]/div[@id="mainpic"]/a[@class="nbg"]/@href')
    imageurl=selector.xpath('//div[@id="wrapper"]//div[@class="indent"]//a[@class="nbg"]/img/@src')
    #下载图片    
    try:
        pic = requests.get(imageurl[0], timeout=10)    
        try:
            dir = 'D:/message2/' + str(bookname[0]) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            print("write succeed !")  
            book_detail['BookImage'] = str(bookname[0])+".jpg"
        except:  
            name = re.sub("[^a-zA-Z0-9\u4e00-\u9fa5]", '', str(bookname[0]))
            #name = ''.join(re.findall('[\u4e00-\u9fa5]',str(bookname[0])))
            dir = 'D:/message2/' + str(name) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            print("write succeed !")  
            book_detail['BookImage'] = str(name)+".jpg"        
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')
        book_detail['BookImage'] = "NULL"        
    
    #提取集体信息
    detail=selector.xpath('//div[@id="content"]//div[@id="info"]//text()')
    if(len(detail)!=0):
        details=[j.replace('\n','').replace(' ','').strip() for j in detail]
        #details = etree.tostring(detail[0])
        #清理提取出信息存在的混淆元素
        while '' in details:
            details.remove('')
        while ':' in details:
            details.remove(':')
        #for c in range(0,len(details)):
        #    if details[c] == '':
        #       del detail(c)
        #print(details)
        
        for c in range(len(details)):
            #图书出版社
            if details[c] == '出版社:':
                c+=1
                book_detail['BookPress']=details[c]
            #图书出品方
            if '出品方' in details[c]:
                c+=1
                book_detail['BookProducer']=details[c]
            #图书作者
            if '作者' in details[c] and '原' not in details[c]:
                c+=1
                book_detail['Bookauthor']=details[c]
                #while details[c+1] == '/':
                #    book_detail['Bookauthor']=str(book_detail['Bookauthor'])+str(details[++c])+str(details[++c])
            #图书译者
            if '译者' in details[c]:
                c+=1
                book_detail['BookTranslator']=details[c]
            #图书出版年
            if '出版年' in details[c]:
                c+=1
                book_detail['BookYear']=str(details[c])
            #图书页数
            if '页数' in details[c]:
                c+=1
                book_detail['BookPages']=details[c]
            #图书国家编号（ISBN）
            if 'ISBN' in details[c]:
                c+=1
                book_detail['BookISBN']=str(details[c])          
        
    #图书评分：
    score=selector.xpath('//div[@id="interest_sectl"]//div[@class="rating_self clearfix"]/strong/text()')      
    if(len(score)!=0):
        book_detail['BookScore'] = score[0]
    else:
        book_detail['BookScore'] = "NULL"
    
    #图书总评价人数：
    people =  selector.xpath('//div[@id="interest_sectl"]//div[@class="rating_sum"]//a/span/text()')   
    if(len(people)!=0):
        book_detail['BookPeople'] = people[0]
    else:
        book_detail['BookPeople'] = "NULL"
    #图书简介
    Bookdetails = selector.xpath('//div[@class="indent" and @id="link-report"]//span[@class="all hidden"]//div[@class="intro"]//text()')        
    #print(Bookdetails)
    if len(Bookdetails) == 0:
        Bookdetails = selector.xpath('//div[@class="indent" and @id="link-report"]//div[@class="intro"]//text()')  
    if(len(Bookdetails)!=0):
        Bookdetails=[j.replace('\n','').replace(',','，').replace(' ','').replace('\t','').strip() for j in Bookdetails]
        #print(Bookdetails)
        s=''.join(Bookdetails)
        book_detail['Bookdetail'] = str(s)    
    
    return book_detail

#图书信息
def book_content(types):
    #data = {}
    #读取存书名的txt文件：
    try:
        with open('type.txt', "r",encoding='utf-8-sig') as txtfile:
            data = json.load(txtfile)
    except:
        data = {}
    url0=u'https://book.douban.com/tag/{type_book}?start={0}&type=T'.format(type_book=types)
    for i in range(0,50):  #一本书50页   --推理-->流行
        #print(i)
        url=url0.format(i*20)
        print(url)
        #response = requests.get(url,headers=header)
        count = 1
        response = GetHTML(url)
        while response == None:
            response = GetHTML(url)
            count+=1
            if(count == 10):
                print('page '+str(i)+'url down fail')
                with open("book_type.txt", "w",encoding='utf-8') as fp:
                    fp.write(json.dumps(data,ensure_ascii=False))
                    #ensure_ascii=False---防止出现乱码
                break
        #response = GetHTML(url)
        if response != None:
            selector = etree.HTML(response)
            #selector = etree.HTML(response.text)
            #print(selector)
            #bookurls=selector.xpath('//td[@valign="top" and not(@width)]/div[@class="pl2"]/a/text()')
            
            #图书链接：
            bookurls=selector.xpath('//li[@class="subject-item"]/div[@class="pic"]/a/@href')
            #如果得到的链接数据为空，说明本类别已爬完
            if len(bookurls) == 0:
                break
            #书名：
            booknames=selector.xpath('//li[@class="subject-item"]/div[@class="info"]/h2/a/text()')
            #对书名进行处理
            booknames=[j.replace('\n','').replace(' ','').strip() for j in booknames]
            booknames=[j for j in booknames if len(j)!=0]
            
            #进入图书页面获取信息
            cc = 1
            for book_count in range(0,len(bookurls)):
                #测试书名是否已存入字典
                if str(booknames[book_count]) in data:
                #已存在--在value值中加入现爬的类标签
                    if '推理' not in (data[str(booknames[book_count])]):                        
                        data[str(booknames[book_count])] = data[str(booknames[book_count])]+',推理'
                    print("page:"+str(i+1)+"---book:"+str(cc)+"--"+str(booknames[book_count])+"--already down")
                    cc+=1
                else:
                    #书名未曾保存---"会出错"，则需要爬取，且加入字典中 
                    data[str(booknames[book_count])]='推理'
                    book = bookdetail(bookurls[book_count]);
                    print(book)                    
                    '''存储图书详情信息'''
                    if len(book) > 4:
                        print(len(book))
                        with open('book_detail.txt', "a",encoding='utf-8') as fp:
                            fp.write('{BookID}\t{BookImage}\t{BookName}\t{BookPress}\t{BookProducer}\t{Bookauthor}\t{BookTranslator}\t{Bookdetail}\t{BookYear}\t{BookPages}\t{BookISBN}\t{BookScore}\t{BookPeople}\n')
                            .format(BookID=book['BookID'],BookImage=book['BookImage'],BookName=book['BookName'],BookPress=book['BookPress'],BookProducer=book['BookProducer'],Bookauthor=book['Bookauthor'],BookTranslator=book['BookTranslator'],
                                    Bookdetail=book['Bookdetail'],BookYear=book['BookYear'],BookPages=book['BookPages'],BookISBN=book['BookISBN'],BookScore=book['BookScore'],BookPeople=book['BookPeople'])
                        #fieldnames = ['BookID', 'BookImage', 'BookName' , 'BookPress', 'BookProducer', 'Bookauthor', 'BookTranslator', 'Bookdetail', 'BookYear' , 'BookPages', 'BookISBN', 'BookScore', 'BookPeople']
                        #save(book,"流行.csv",fieldnames)
                    print("page:"+str(i+1)+"---book:"+str(cc)+"--"+str(booknames[book_count])+"--succeed")
                    cc+=1
                    #以json格式写入文件
                with open("book_type.txt", "w",encoding='utf-8') as fp:
                    fp.write(json.dumps(data,ensure_ascii=False))
                    #ensure_ascii=False---防止出现乱码

    
#记录一整页的评论信息    
def comment_down(url):
    #comment = {}
    #comment1 ={}
    count1 = 0
    response = GetHTML(url)
    while response == None:
        response = GetHTML(url)
        count1+=1
        if(count == 10):
            #print('page '+str(i)+'url down fail')
            with open("comment_type.txt", "w",encoding='utf-8') as fp:
                fp.write(json.dumps(data,ensure_ascii=False))
                #ensure_ascii=False---防止出现乱码
            break
    #response = GetHTML(url)
    if response != None:
        selector = etree.HTML(response)
      
        #selector = etree.HTML(response)
        #评论编号：
        comments_id = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]/@data-cid')    
        
        #提取图书id
        book = selector.xpath('//div[@class="indent subject-info"]/div/a/@href')
        book_id = book[0].split('/')[-2]
        #comment['book_id']=book_id
        
            
        #评论者名称
        names = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]/div[@class="avatar"]/a/@title')
        #print(names)
                
        #评论者id
        user_id = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]/div[@class="avatar"]/a/@href')
        
                
         #评论
        comments = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]//p[@class="comment-content"]/span/text()')
        comments=[j.replace('\n','').replace(' ','').strip() for j in comments]
        #print(comments)
        
        #点赞人数
        comments_people = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]//span[@class="comment-vote"]/span/text()')
        #print(comments_people)
        
        #推荐评分
        comments_score = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]//span[@class="comment-info"]/span[1]/@class')
        #print(len(comments_score))
        for i in range(0,len(comments_score)):
            comments_score[i]=re.findall(r'\d+',comments_score[i])
            comments_score[i] = ''.join(comments_score[i])
            comments_score[i] = str(int(comments_score[i])*2/10)
        comments_score.extend(["null"]*(20-len(comments_score)))       
        #print(comments_score)
        
        
        
        #评论日期：
        comments_data = selector.xpath('//div[@id="comments"]//li[@class="comment-item"]//span[@class="comment-info"]/span[not (@class)]/text()')
        #print(comments_data)        
                
        for i in range(0,len(user_id)):
            #提取user_id
            user_id[i] = user_id[i].split('/')[-2]
            #name = names[i]
            #content = comments[i]
            '''用户训练推荐算法的数据'''
            try:
                with open('comment.txt', 'a+', encoding='utf-8')as f:
                    f.write('{book_id}\t{user_id}\t{name}\t{content}\n'.format(book_id=book_id,user_id=user_id[i],name=names[i],content=comments[i]))
            except Exception as e:
                print("write error==>", e)
                # 记录错误数据
                with open("Comment_error.txt", "w") as f:
                    f.write(str(i) + "--write error,\n")
                pass
            
            #with open('comment_detail.txt', 'a+', encoding='utf-8')as fa:
            #    fa.write('{CommentID}\t{BOOKID}\t{UserID}\t{UserName}\t{Comment_date}\t{Comment_Score}\t{Comment_People}\t{Comment_title}\t{CommentContent}\n'.format(CommentID=comments_id[i],BOOKID=book_id,UserID=user_id[i],UserName=names[i],Comment_date=comments_data[i],Comment_Score=comments_score[i],Comment_People=comments_people[i],Comment_title='title',CommentContent=comments[i]))
            
            try:
                with open('comment_detail.txt', 'a+', encoding='utf-8')as fa:
                    fa.write('{CommentID}\t{BOOKID}\t{UserID}\t{UserName}\t{Comment_date}\t{Comment_Score}\t{Comment_People}\t{Comment_title}\t{CommentContent}\n'.format(CommentID=comments_id[i],BOOKID=book_id,UserID=user_id[i],UserName=names[i],Comment_date=comments_data[i],Comment_Score=comments_score[i],Comment_People=comments_people[i],Comment_title='title',CommentContent=comments[i]))
            except Exception as e:
                print("write error==>", e)
                # 记录错误数据
                with open("Comment_error.txt", "w") as f:
                    f.write(str(i) + "--write error,\n")
                pass
            
def comment_take(types):
    #url = 'https://book.douban.com/subject/4913064/comments/hot?p=2'
    #data = {}
    #读取存书名的txt文件：
    try:
        with open('comment_type.txt', "r",encoding='utf-8-sig') as txtfile:
            data = json.load(txtfile)
    except:
        data = {}
    
    url0=u'https://book.douban.com/tag/{type1}?start={0}&type=T'.format(type1=types)
    for i in range(1,50):  #一本书50页
        #print(i)
        url=url0.format(i*20)
        print(url)
        #response = requests.get(url,headers=header)
        count = 1
        response = GetHTML(url)
        while response == None:
            response = GetHTML(url)
            count+=1
            if(count == 10):
                print('page '+str(i)+'url down fail')
                with open("comment_type.txt", "w",encoding='utf-8') as fp:
                    fp.write(json.dumps(data,ensure_ascii=False))
                    #ensure_ascii=False---防止出现乱码
                break
        #response = GetHTML(url)
        if response != None:
            selector = etree.HTML(response)
            #selector = etree.HTML(response.text)
            #print(selector)
            #bookurls=selector.xpath('//td[@valign="top" and not(@width)]/div[@class="pl2"]/a/text()')
            #图书链接：
            bookurls=selector.xpath('//li[@class="subject-item"]/div[@class="pic"]/a/@href')
            #print(bookurls)
            #如果得到的链接数据为空，说明本类别已爬完
            if len(bookurls) == 0:
                break
            #书名：
            booknames=selector.xpath('//li[@class="subject-item"]/div[@class="info"]/h2/a/text()')
            #对书名进行处理
            booknames=[j.replace('\n','').replace(' ','').strip() for j in booknames]
            booknames=[j for j in booknames if len(j)!=0]
            
            
            #对整一页的所有数据进行循环
            for book_count in range(0,len(bookurls)):#len(bookurls)0,5--5,10--10,15--15,20
                print("开始爬取书籍 >>"+str(book_count)+" >> "+str(booknames[book_count]))
                #测试书名是否已记录
                if str(booknames[book_count]) in data:
                    continue
                else:
                    #未记录过
                    for ccc in range(1,26):
                        urls = str(bookurls[book_count]) + 'comments/hot?p='+str(ccc)
                        comment_down(urls)
                        print('Page >> '+str(ccc)+'>> hot-- down')  
                        urls = str(bookurls[book_count]) + 'comments/new?p='+str(ccc)
                        comment_down(urls)
                        print('Page >> '+str(ccc)+'>> new-- down')
                    data[str(booknames[book_count])]="已记录"
                    with open("comment_type.txt", "w",encoding='utf-8') as fp:
                        fp.write(json.dumps(data,ensure_ascii=False))
                        #ensure_ascii=False---防止出现乱码
                    with open('Comment_error.txt','a+',encoding='utf-8') as f:
                        f.write(str(booknames[book_count])+" >> page--"+str(ccc))
                
    
if __name__ == '__main__':
    
    types = ['小说','外国文学','漫画','推理','历史','心理学','爱情','成长','经济学','管理','科普','互联网']
    for i in types:        
    
        #获取图书详情
        bookdetail(i)
        
        #获取图书评论
        comment_take(i)