# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:10:48 2020

@author: lenovo
"""

import re
import requests
from lxml import etree
from urllib import request
import json
import time

data={}
peoples = {}
#对people进行初始化
peoples['read']=0
peoples['guan']=0
peoples['beguan']=0

headers = {
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
    'Host': 'accounts.douban.com',
    'Cookie':'bid=yxSDAe8He4g; ll="118300"; viewed="10554308_34985448_34998081"; _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1591262723%2C%22https%3A%2F%2Fbook.douban.com%2Ftag%2F%25E5%25B0%258F%25E8%25AF%25B4%22%5D; _pk_id.100001.2fad=b47a49e0bb647a19.1591236953.5.1591262790.1591260646.; last_login_way=account; _vwo_uuid_v2=D39048CBD73E52C2D3E7894738F32E5B7|415c0b18a6fbd7c3f83e374feb6e645c; gr_user_id=a7029af2-d09c-4769-8a7c-1e2c8836cde2; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; apiKey=; __utma=30149280.1092181277.1591243995.1591265366.1591270244.6; __utmb=30149280.3.10.1591270244; __utmc=30149280; __utmz=30149280.1591270244.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.21615; login_start_time=1591270264086',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Mobile Safari/537.36'
    }

#进入收藏页面：
def Collector(name):
    global peoples
    url0 = 'https://book.douban.com/people/{name}/wish'.format(name=name)
    print(url0)
    with open('记录.txt','a',encoding='utf-8') as fc:
        fc.write(url0+'\n')
    count = 1
    response = GetHTML(url0)
    #print(response)
    while response == None:
        print(count)
        #with open('记录.txt','a',encoding='utf-8') as fc:
        #    fc.write(url0+'\n')
        response = GetHTML(url0)        
        count+=1
        if(count == 10):            
            break 
    if response !=None:
        """    
        with open('User_detail.txt','r',encoding="utf-8") as f:
             f = f.read()
             #print(f)
        """     
        selector = etree.HTML(response)
        #print(selector)
        
        #获得他收藏的书的数目
        Num = selector.xpath('//div[@id="db-usr-profile"]/div[@class="info"]/h1/text()')
        #王老板想读的书(31)
        #print(Num[0]+'--')
        book_Count = int(re.findall(r'想读的书\((.*?)\) ',Num[0])[0])
        peoples['collect']=book_Count
        print(name +'>> 收藏的书共 '+str(book_Count)+' 本')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 收藏的书共 '+str(book_Count)+' 本'+'\n')
        
        #进行首页获取：
        wish(selector,name)
        
        #获得页数--15/页
        page1 = book_Count//15
        if page1 > 4:
            page1 = 4
        if page1 > 1:
            for i in range(1,page1+1):  #进入第二页
                sss = i*15
                print("链接 >> "+ str(sss))
                with open('记录.txt','a',encoding='utf-8') as fc:
                    fc.write("链接 >> "+ str(sss)+'\n')
                urls2 = 'https://book.douban.com/people/{name}/wish?start={page}&sort=time&rating=all&filter=all&mode=grid'.format(name=name,page=sss)
                response = GetHTML(urls2)
                count1 = 1
                #print(response)
                while response == None:
                    print(count1)
                    response = GetHTML(urls2)        
                    count1+=1
                    if(count1 == 10):            
                        return 0 
                if response !=None:
                    selector = etree.HTML(response)
                    wish(selector,name)
        print(name + " >> collects down success")
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name + " >> collects down success"+'\n')

#进行收藏采集    
def wish(selector,name):
    
    #获得收藏的图书id
    book_collect = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//a[@class="nbg"]/@href')
    book_collect=[j.split('/')[-2].strip() for j in book_collect]
    #print(book_collect)
    
    #获得阅读的图书名称
    book_name = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//a[not (@class)]/@title')
    #print(book_name)
    
    #获得收藏时间
    collect_date = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//span[@class="date"]/text()')
    collect_date=[j.replace('\n','').replace(' ','').replace('想读','').strip() for j in collect_date]
    #print(collect_date)
    
    #存储
    for j in range(len(book_collect)):
        #print('{CollectID}\t{UserID}\t{BookID}\t{Collect_date}\n'.format(CollectID=collect_id,UserID=name,BookID=book_collect[j],Collect_date=collect_date[j]))
        with open('User_collect.txt','a+',encoding="utf-8") as fw:
            fw.write('{CollectID}\t{UserID}\t{BookID}\t{BookName}\t{Collect_date}\n'.format(CollectID=collect_id,UserID=name,BookID=book_collect[j],BookName=book_name[j],Collect_date=collect_date[j]))
        collect_id +=1
        #print('collect_id = '+ str(collect_id))

def book_read(userid):
    global peoples
    #https://book.douban.com/people/50593665/collect
    urls = 'https://book.douban.com/people/{userid}/collect'.format(userid=userid)
    ref = 'https://book.douban.com/people/{userid}/'.format(userid=userid)
    
    #用于获得阅读信息的头
    head1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cookie': 'bid=yxSDAe8He4g; ll="118300"; viewed="34985448_34998081"; gr_user_id=1a03f467-c630-4f19-8271-988ad078b693; _vwo_uuid_v2=DCF0260AFC21A1EC7ACDC1F7D8001C91C|aeed3933f455e79d28cc5e6a4176b247; ck=jdLJ; dbcl2="216156056:pclE1raCMnM"; ap_v=0,6.0; _ga=GA1.2.1349045414.1590761332; _gid=GA1.2.929042112.1590773971; __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1590774074%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F50593665%2F%22%5D; _pk_id.100001.3ac3=30b720d2109a84d3.1590761332.3.1590774074.1590767639.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utma=30149280.1349045414.1590761332.1590766779.1590773064.4; __utmb=30149280.7.10.1590773064; __utmc=30149280; __utmz=30149280.1590763041.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.21615; __utma=81379588.304954881.1590761332.1590766779.1590774074.3; __utmb=81379588.1.10.1590774074; __utmc=81379588; __utmz=81379588.1590774074.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/50593665/; push_noty_num=0; push_doumail_num=0',
    #'bid=yxSDAe8He4g; ll="118300"; viewed="34985448_34998081"; ck=jdLJ; dbcl2="216156056:pclE1raCMnM"; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1590774074%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F50593665%2F%22%5D; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f1c28cff-16d9-42ac-86c5-89defee03e7c; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f1c28cff-16d9-42ac-86c5-89defee03e7c=true; __utmt_douban=1; __utmt=1; gr_cs1_f1c28cff-16d9-42ac-86c5-89defee03e7c=user_id%3A1; gr_user_id=1a03f467-c630-4f19-8271-988ad078b693; _vwo_uuid_v2=DCF0260AFC21A1EC7ACDC1F7D8001C91C|aeed3933f455e79d28cc5e6a4176b247; _ga=GA1.2.1349045414.1590761332; _gid=GA1.2.929042112.1590773971; _pk_id.100001.3ac3=30b720d2109a84d3.1590761332.3.1590775035.1590767639.; _pk_ses.100001.3ac3=*; __utma=30149280.1349045414.1590761332.1590766779.1590773064.4; __utmb=30149280.11.10.1590773064; __utmc=30149280; __utmz=30149280.1590763041.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.21615; __utma=81379588.304954881.1590761332.1590774074.1590774591.4; __utmb=81379588.3.10.1590774591; __utmc=81379588; __utmz=81379588.1590774591.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; push_noty_num=0; push_doumail_num=0'
    'Referer': ref,
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Mobile Safari/537.36'
    }
    time.sleep(3)
    response = requests.get(urls,headers=head1)
    #print(response.status_code)
    count = 1
    while response.status_code != 200:
        response = requests.get(urls,headers=head1)
        count +=1
        if count == 10:
            break
    if response.status_code == 200:
        #print(response)
        response.encoding='utf-8'
        selector = etree.HTML(response.text)
        
        #获得他收藏的书的数目
        Num = selector.xpath('//div[@id="db-usr-profile"]/div[@class="info"]/h1/text()')
        #王老板读过的书(31)
        #print(Num[0]+'--')
        book_Count = int(re.findall(r'读过的书\((.*?)\) ',Num[0])[0])
        name = re.findall(r'(.*?)读过的书',Num[0])[0]
        peoples['read']=book_Count
        print(name +'>> 读过的书共 '+str(book_Count)+' 本')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 读过的书共 '+str(book_Count)+' 本'+'\n')
        
        #进行首页获取：
        print(name +'>> 阅读页面：1 获取')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 阅读页面：1 获取'+'\n')
        Read(selector,userid,name)
        
        #获得页数--15/页
        page1 = book_Count//15
        
        if page1 > 4:
            page1 = 4
        if page1 > 1:
            for i in range(1,page1+1):  #进入第二页
                print(name +'>> 阅读页面：'+str(i+1)+' 获取')
                with open('记录.txt','a',encoding='utf-8') as fc:
                    fc.write(name +'>> 阅读页面：'+str(i+1)+' 获取'+'\n')
                
                urls1 = 'https://book.douban.com/people/{name}/collect?start={page}&sort=time&rating=all&filter=all&mode=grid'.format(name=userid,page=(i*15))
                response = requests.get(urls1,headers=head1)
                count = 1
                time.sleep(3)
                while response.status_code != 200:
                    response = requests.get(urls,headers=head1)
                    count +=1
                    if count == 10:
                        break
                if response.status_code == 200:
                    response.encoding='utf-8'
                    selector = etree.HTML(response.text)
                    Read(selector,userid,name)
        print(name +'>> Read down success')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> Read down success'+'\n')
    else:
        with open('error.txt','a',encoding='utf-8') as fc:
            fc.write(str(userid)+'阅读页面失败')

def Read(selector, userid, name):
    #获得阅读的图书id
    book_collect = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//a[@class="nbg"]/@href')
    book_collect=[j.split('/')[-2].strip() for j in book_collect]
    #print(book_collect)
    
    #获得阅读的图书名称
    book_name = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//a[not (@class)]/@title')
    #print(book_name)
    
    #获得阅读时间
    collect_date = selector.xpath('//ul[@class="interest-list"]/li[@class="subject-item"]//span[@class="date"]/text()')
    collect_date=[j.replace('\n','').replace(' ','').replace('读过','').strip() for j in collect_date]
    #print(collect_date)
    
    #存储
    for j in range(len(book_collect)):
        #print('{UserID}\t{UserName}\t{BookID}\t{BookName}\t{Collect_date}\n'.format(UserID =userid ,UserName=name,BookID=book_collect[j],BookName=book_name[j],Collect_date=collect_date[j]))
        with open('阅读.txt','a',encoding='utf-8') as fw:
            fw.write('{UserID}\t{UserName}\t{BookID}\t{BookName}\t{Collect_date}\n'.format(UserID =userid ,UserName=name,BookID=book_collect[j],BookName=book_name[j],Collect_date=collect_date[j]))
    
def guanzhu(userid):
    global peoples
    #https://www.douban.com/people/orangemayer/contacts
    urls = 'https://www.douban.com/people/{userid}/contacts'.format(userid=userid)
    ref = 'https://www.douban.com/people/{userid}/'.format(userid=userid)
    #用于获得关注人信息的头
    head2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': 'bid=yxSDAe8He4g; ll="118300"; viewed="10554308_34985448_34998081"; ap_v=0,6.0; dbcl2="216156056:za1xYxXx7uQ"; ck=UKfR; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f8875898-f14e-43a6-8ece-0c2489774570; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f8875898-f14e-43a6-8ece-0c2489774570=true; gr_cs1_f8875898-f14e-43a6-8ece-0c2489774570=user_id%3A1; gr_user_id=12c2e51f-a5e6-46bd-902e-131db99e79a4; _vwo_uuid_v2=D54E247D7A3D7F4AC7492C7B95361A505|4fb51ded37dbcd0a2392055b70ab6d2f; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1591445846%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; __utmt=1; _pk_id.100001.8cb4=8846724344d78fe4.1591433769.4.1591446569.1591442208.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.228370445.1591433183.1591442214.1591445271.4; __utmb=30149280.11.10.1591445271; __utmc=30149280; __utmz=30149280.1591442214.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmv=30149280.21615',
        'Referer': ref,
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Mobile Safari/537.36'
        }
    response = requests.get(urls,headers=head2)
    time.sleep(3)
    count = 1
    while response.status_code != 200:
        response = requests.get(urls,headers=head2)
        count +=1
        print(count)
        if count == 10:
            break
    if response.status_code == 200:
        response.encoding='utf-8'
        selector = etree.HTML(response.text)
        #获得关注的人数：
        people = selector.xpath('//div[@class="info"]/h1/text()')
        #print(people[0])
        #print(re.findall(r'关注的人\((.*?)\)',people[0]))
        number = int(re.findall(r'关注的人\((.*?)\)',people[0])[0])
        name = re.findall(r'(.*?)关注的人',people[0])[0]
        peoples['guan'] = int(number)
        print(name +'>> 关注的人共 >'+str(number)+' 人')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 关注的人共 >'+str(number)+' 人'+'\n')
        
        #此链接将所有关注人员列出，故只需将本页信息提取即可
        #userid
        ids = selector.xpath('//dl[@class="obu"]/dd/a/@href')
        ids = [j.split('/')[-2] for j in ids]
        #print(ids)
        #print(len(ids))
        #username
        names = selector.xpath('//dl[@class="obu"]/dd/a/text()')
        #print(names)
        
        for i in range(len(ids)):
            #print('{Userid}\t{Username}\t{id}\t{name}\n'.format(Userid=userid,Username=name,id=ids[i],name=names[i]))
            with open('关注.txt','a',encoding='utf-8') as fw1:
                fw1.write('{Userid}\t{Username}\t{id}\t{name}\n'.format(Userid=userid,Username=name,id=ids[i],name=names[i]))
        print(name +'>> 关注人 down success')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 关注人 down success'+'\n')
    else:
        with open('error.txt','a',encoding='utf-8') as fc:
            fc.write(str(userid)+'关注页面失败')
    
def be_guanzhu(userid):
    global peoples
    #https://www.douban.com/people/axianxian/rev_contacts
    urls = 'https://www.douban.com/people/{userid}/rev_contacts'.format(userid=userid)
    ref = 'https://www.douban.com/people/{userid}/'.format(userid=userid)
    #用于获得被关注人信息的头
    head3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',                
        'Cookie': 'bid=yxSDAe8He4g; ll="118300"; viewed="10554308_34985448_34998081"; ap_v=0,6.0; dbcl2="216156056:za1xYxXx7uQ"; ck=UKfR; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f8875898-f14e-43a6-8ece-0c2489774570; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f8875898-f14e-43a6-8ece-0c2489774570=true; gr_cs1_f8875898-f14e-43a6-8ece-0c2489774570=user_id%3A1; gr_user_id=12c2e51f-a5e6-46bd-902e-131db99e79a4; _vwo_uuid_v2=D54E247D7A3D7F4AC7492C7B95361A505|4fb51ded37dbcd0a2392055b70ab6d2f; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1591445846%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.8cb4=8846724344d78fe4.1591433769.4.1591446509.1591442208.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utmt=1; __utma=30149280.228370445.1591433183.1591442214.1591445271.4; __utmb=30149280.7.10.1591445271; __utmc=30149280; __utmz=30149280.1591442214.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmv=30149280.21615',
        'Referer': ref,
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Mobile Safari/537.36'
        }
    count = 1
    response = requests.get(urls,headers=head3)
    time.sleep(3)
    while response.status_code != 200:
        response = requests.get(urls,headers=head3)
        count +=1
        print(count)
        if count == 10:
            break
    if response.status_code == 200:
        response.encoding='utf-8'
        selector = etree.HTML(response.text)
        #获得关注的人员数量
        people = selector.xpath('//div[@class="info"]/h1/text()')
        #print(people[0])
        #print(re.findall(r'关注的人\((.*?)\)',people[0]))
        number = int(re.findall(r'的人\((.*?)\)',people[0])[0])
        peoples['beguan']=number
        #print(number)
        #关注阿闲闲的人
        name = re.findall(r'关注(.*?)的人',people[0])[0]
        print('关注 >> '+name +'>> 共 '+str(number)+' 个人')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write('关注 >> '+name +'>> 共 '+str(number)+' 个人'+'\n')
        #每页记录70个人员
        #计算出页数
        page = number//70
        #print(page)
        
        #进行首页获取：
        print(name +'>> 关注页面：1 获取')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 关注页面：1 获取'+'\n')
        pepple_gaun(selector,userid,name)
        
        '''
        #if page > 1:
        #    page = 1
        if page > 1:
            for i in range(1,2):  #进入第二页
                print(name +'>> 关注页面：'+str(i+1)+' 获取')
                with open('记录.txt','a',encoding='utf-8') as fc:
                    fc.write(name +'>> 关注页面：'+str(i+1)+' 获取'+'\n')
                head4 = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',                
                    'Cookie': 'bid=yxSDAe8He4g; ll="118300"; viewed="10554308_34985448_34998081"; ap_v=0,6.0; dbcl2="216156056:YHYv/LB8FdU"; ck=aomc; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=52bed74d-116d-48b7-9d74-cb16e00511be; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_52bed74d-116d-48b7-9d74-cb16e00511be=true; _vwo_uuid_v2=D39048CBD73E52C2D3E7894738F32E5B7|415c0b18a6fbd7c3f83e374feb6e645c; gr_cs1_52bed74d-116d-48b7-9d74-cb16e00511be=user_id%3A1; gr_user_id=a7029af2-d09c-4769-8a7c-1e2c8836cde2; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1591243853%2C%22https%3A%2F%2Fbook.douban.com%2Fsubject%2F1007305%2F%22%5D; __utmt=1; _pk_id.100001.8cb4=c0a84b9b737bf5fc.1591236959.2.1591244264.1591236959.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.1092181277.1591243995.1591243995.1591243995.1; __utmb=30149280.6.10.1591243995; __utmc=30149280; __utmz=30149280.1591243995.1.1.utmcsr=book.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/1007305/; __utmv=30149280.21615',
                    'Referer': urls,
                    'Host': 'www.douban.com',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Mobile Safari/537.36'
                    }
                #https://www.douban.com/people/16235694/rev_contacts?start=70
                urls = 'https://www.douban.com/people/{userid}/rev_contacts?start={p}'.format(userid=userid,p=(i*70))
                #reff = 'https://www.douban.com/people/{userid}/rev_contacts'.format(userid=userid)
                
                print(urls)
                with open('记录.txt','a',encoding='utf-8') as fc:
                    fc.write(str(urls)+'\n')
                response = requests.get(urls,headers=head4)
                time.sleep(3)
                count = 1
                while response.status_code != 200:
                    response = requests.get(urls,headers=head4)
                    count +=1
                    if count == 10:
                        break
                if response.status_code == 200:
                    response.encoding='utf-8'
                    selector = etree.HTML(response.text)
                    pepple_gaun(selector,userid,name)
        '''
        print(name +'>> 被关注人 down success')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write(name +'>> 被关注人 down success'+'\n')
    else:
        with open('error.txt','a',encoding='utf-8') as fc:
            fc.write(str(userid)+'被关注页面失败')
                    
def pepple_gaun(selector,userid,name):
    #userid
    ids = selector.xpath('//dl[@class="obu"]/dd/a/@href')
    ids = [j.split('/')[-2] for j in ids]
    #print(ids)
    #print(len(ids))
    #username
    names = selector.xpath('//dl[@class="obu"]/dd/a/text()')
    #print(names)
        
    for i in range(len(ids)):
        #print('{Userid}\t{Username}\t{id}\t{name}\n'.format(Userid=userid,Username=name,id=ids[i],name=names[i]))
        with open('被关注.txt','a',encoding='utf-8') as fw2:
            fw2.write('{Userid}\t{Username}\t{id}\t{name}\n'.format(Userid=userid,Username=name,id=ids[i],name=names[i]))

def Login(name, password):
    global peoples
    
    # 使用 requests.Session 模拟登录
    session = requests.Session()
    # 请求登录的 URL
    post_url = 'https://accounts.douban.com/j/mobile/login/basic'

    # 登录时传递的表单数据
    post_data = {
        'ck': '',
        'name': name,
        'password': password,
        'remember': False,
        'ticket': ''
    }
    #使用 session 发起一个 POST 请求，并携带请求头和表单数据
    response = session.post(post_url, data=post_data, headers=headers)
    # 如果模拟登录成功
    
    if response.status_code == 200:        
        print('登录成功')
        with open('记录.txt','a',encoding='utf-8') as fc:
            fc.write('登录成功'+'\n')
        
        try:
            with open('people_type.txt', "r",encoding='utf-8-sig') as fr:
                datas = json.load(fr)
        except:
            datas = {}
        """根据评论中的用户进行信息爬取"""    
        with open('comment-for-user.txt','r', encoding='UTF-8') as f:
            content = f.read()
        content_split = content.split('\n')
        for i in range(len(content_split)):#len(content_split)
            #print(content_split[i])
            contents = content_split[i].split('\t')
            if len(contents) == 9:
                if contents[2] in datas:
                    print(str(contents[2])+'已记录')
                    #with open('记录.txt','a',encoding='utf-8') as fc:
                    #    fc.write(str(contents[2])+'已记录'+'\n')
                else:
                    peoples={'read':0,'guan':0,'beguan':0}
                    #peoples['read']=0
                    #peoples['guan']=0
                    #peoples['beguan']=0
                    #for key in data.keys:
                    #try:
                    userid = contents[2]
                    print(userid)
                    """用户的阅读信息"""
                    #book_read(userid)
                        #print(response.cookies)
                        # 访问登录之后的页面
                        #urls = 'https://book.douban.com/people/50593665/collect'
                        #得到用户id
                        #userid = urls.split('/')[-2]
                        #referer
                        #ref = 'https://www.douban.com/people/'+str(userid)+'/'
                    guanzhu(userid)
                        
                    be_guanzhu(userid)
                    
                    Collector(userid)
                    
                    print(userid+str(peoples))
                    datas.update({userid: peoples})
                    #print(datas)
                    #datas[userid]=peoples
                    #print(datas)
                    print(str(contents[2])+' >> 记录成功')
                    with open('记录.txt','a',encoding='utf-8') as fc:
                        fc.write(str(contents[2])+' >> 记录成功'+'\n')
                    with open('people_type.txt', "w",encoding='utf-8-sig') as fp:
                        fp.write(json.dumps(datas,ensure_ascii=False))
                        """
                        except Exception as e:
                            with open('people_type.txt', "w",encoding='utf-8-sig') as fp:
                                fp.write(json.dumps(data,ensure_ascii=False))
                            print(str(contents[2])+' >> 记录失败',e)
                            with open('记录.txt','a',encoding='utf-8') as fc:
                                fc.write(str(contents[2])+' >> 记录失败'+'\n')
                        """

if __name__ == "__main__":
    
    
    Login('13532271254','1qaz2wsx3edc')