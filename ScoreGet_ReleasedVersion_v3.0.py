'''
使用说明：使用前先根据你的情况修改部分代码，修改好后保存然后双击就进入运行状态了。要保持本脚本可以正常运行，需要保持网络正常、脚本窗口不关闭。如果想停止接收邮件，关闭该窗口即可。
首先需要选择用于发送成绩信息的邮箱，需要在邮箱提供商处设置开启SMTP，并将SMTP服务器、发件邮箱用户名、发件邮箱密码依次替换19-21行的对应内容，并用发件邮箱的地址替换22行的对应内容
然后选择用于收件的邮箱（可与发件邮箱相同），替换23行的对应内容（如果有多个收件人，需要用List保存各个收件人的邮箱地址并用该List替换）
最后需要获取Cookie。Chrome的获取方法：在浏览器中打开https://app.buaa.edu.cn/buaascore/wap/default/index，并用自己的统一认证账号登录，然后按下F12，在最上面一栏中点"Application"，在左边栏点"Cookies"左边的小三角，选中"Cookies"下第一个项，将每个元素的名称和值按'Name':'Value'的格式填入代码中的cookies，也就是把cookies建立成由【名称到值的映射】构成的字典

'''
import re
import requests
import os
import time
from html.parser import HTMLParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
sum=0
listcourse=[]
listxuefen=[]
listgpa=list()
postcontent={
    'token':'',
    'title':'',
    'content':''}
def get_gpa(course,xuefen):
    gpa=4-((3*((100-course)**2))/1600)
    if gpa<=1:
        gpa=0
    return gpa

def get_jiaquan(course,xuefen):
    sumcourse=0
    xuefensum=0
    for i in range(len(xuefen)):
        sumcourse=sumcourse+course[i]*xuefen[i]
        xuefensum=xuefensum+xuefen[i]
    return sumcourse/xuefensum


    
def send_mail():
 
    sendurl='http://www.pushplus.plus/send'
    
    r=requests.post(sendurl,json=postcontent)
    print(r.text)
   

    

url=r"https://app.buaa.edu.cn/buaascore/wap/default/index"
data={
    'xq':'2',
    'year':'2022-2023'
}
cookies={  # 用你的cookie替换

}
while True:
    sum+=1
    print("这是第",sum,"次查询\n")

    print(time.ctime())
    try:
        r=requests.post(url,headers={'User-agent':'Mozilla 5.10'},cookies=cookies,data=data)
    except:
        time.sleep(60)
        continue
    r.encoding='utf8'
    f1=open("html.txt","w")
    webstr=r.text.encode('gbk','ignore').decode('gbk')
    f1.write(webstr)
    f1.close()
    print("code=",r.status_code)
    st=webstr.find('list: ')
    ed=webstr.find('\n',st)
    scorestr=webstr[st:ed]
    st=webstr.find('gpa:')
    ed=webstr.find('\n',st)
    gpa=webstr[st+5:ed-1]
    st,ed=0,0
    scorelist=[]
    try:
        f2=open('scorelist.txt','r')
        courseinfo=f2.readlines()
       # print(courseinfo)
        f2.close()
        #input()
    except:
        courseinfo=[]
    coursename=[]
    sumscorelist=[]
    sumlistxuefen=[]
    sumlistgpa=[]
    sumlistcourse=[]
    for coursedict in courseinfo:
        if(eval(coursedict)['kccj']=='暂未出分'):
            continue
        coursename.append(eval(coursedict)['kcmc'])
        # scorelist.append(coursedict)
        sumscorelist.append(eval(coursedict))
    newlist=[]
    flag=False
    while True:
        null='暂未出分'
        st=scorestr.find('{',st+1)
        ed=scorestr.find('}',ed+1)
        subdict={}
        if st==-1 or ed==-1:
            break

        #scorestr.replace('null','0')
        #print(scorestr[st:ed+1])
        if scorestr[st:ed+1].find('null')==-1:
            subdict=eval(scorestr[st:ed+1])
            print(subdict)
            scorelist.append(subdict)
            if subdict not in sumscorelist:
                sumscorelist.append(subdict)
            print(scorelist)
            
        try:
            coursename.index(subdict['kcmc'])
        except:#send notification
            try:
                newlist.append((subdict['kcmc'],subdict['kccj']))
                flag=True
            except:
                pass
   
    if flag:
        postcontent['title']='你的GPA变为:'+gpa
        
        content= ''#'<center><h4><b>新出分的课程</b></h4></center>'
        #content+='<hr class="my-2">'
        for (name,score) in newlist:
            postcontent['content']+='<b>'+name+'</b>\n <b>分数：</b>'+score+'\n'
        postcontent['content']+='<hr class="my-2"> <center><h4><b>本学期所有已出成绩课程信息</b></h4></center><hr class="my-2">'
        for i in range(len(scorelist)):
          
            
            if scorelist[i]['fslx']!='两级制' and scorelist[i]['kccj']!="缺考":
                try:
                   listxuefen.append(float(scorelist[i]['xf']))
                   listcourse.append(int(scorelist[i]['kccj']))
                   listgpa.append(get_gpa(listcourse[i],listxuefen[i]))
                except:
                    if scorelist[i]['fslx']=="五级制":
                        if scorelist[i]['kccj']=="优秀":
                            listcourse.append(100);
                        if scorelist[i]['kccj']=="良好":
                            listcourse.append(83.67);
                        if scorelist[i]['kccj']=='中等':
                            listcourse.append(74.70177871);
                        if scorelist[i]['kccj']=='及格':
                            listcourse.append(64.976198569163);
                        if scorelist[i]['kccj']=='不及格':
                            listcourse.append(0);
                        print(scorelist[i]['fslx'],listxuefen,listgpa,listcourse)
                
                        listgpa.append(get_gpa(listcourse[i],listxuefen[i]))
            else:
                listcourse.append(0)
                listxuefen.append(0)
                listgpa.append(0)
            postcontent['content']+='<b>'+str(i+1)+'、'+scorelist[i]['kcmc']+'</b>\n<b>分数：</b>'+scorelist[i]['kccj']+'\n<b>分数类型：</b>'+scorelist[i]['fslx']+'\n<b>学分：</b>'+scorelist[i]['xf']+'\n<b>课程类型：</b>'+scorelist[i]['kclx']+'\n<b>课程GPA：</b>'+str(round(listgpa[i],2))+'\n'
        postcontent['content']+='<b>本学期加权平均分：</b>'+str(round(get_jiaquan(listcourse,listxuefen),5))+'\n<b>本学期GPA：</b>'+str(round(get_jiaquan(listgpa,listxuefen),5))
        print(postcontent['content'])
        postcontent['content']+='<hr class="my-2"> <center><h4><b>所有已出成绩课程信息</b></h4></center><hr class="my-2">'
        print(sumscorelist)
        for i in range(len(sumscorelist)):
          
                
            if sumscorelist[i]['fslx']!='两级制' and sumscorelist[i]['kccj']!="缺考":
                try:
                   sumlistxuefen.append(float(sumscorelist[i]['xf']))
                   sumlistcourse.append(int(sumscorelist[i]['kccj']))
                   sumlistgpa.append(get_gpa(sumlistcourse[i],sumlistxuefen[i]))
                except:
                    if sumscorelist[i]['fslx']=="五级制":
                        if sumscorelist[i]['kccj']=="优秀":
                            sumlistcourse.append(100);
                        if sumscorelist[i]['kccj']=="良好":
                            sumlistcourse.append(83.67);
                        if sumscorelist[i]['kccj']=='中等':
                            sumlistcourse.append(74.70177871);
                        if sumscorelist[i]['kccj']=='及格':
                            sumlistcourse.append(64.976198569163);
                        if sumscorelist[i]['kccj']=='不及格':
                            sumlistcourse.append(0);
                        print(sumscorelist[i]['fslx'],sumlistxuefen,sumlistgpa,sumlistcourse)
                
                        sumlistgpa.append(get_gpa(sumlistcourse[i],sumlistxuefen[i]))
            else:
                sumlistcourse.append(0)
                sumlistxuefen.append(0)
                sumlistgpa.append(0)
            postcontent['content']+='<b>'+str(i+1)+'、'+sumscorelist[i]['kcmc']+'</b>\n<b>分数：</b>'+sumscorelist[i]['kccj']+'\n<b>分数类型：</b>'+sumscorelist[i]['fslx']+'\n<b>学分：</b>'+sumscorelist[i]['xf']+'\n<b>课程类型：</b>'+sumscorelist[i]['kclx']+'\n<b>课程GPA：</b>'+str(round(sumlistgpa[i],2))+'\n'
        postcontent['content']+='<hr class="my-2"> <b>总加权平均分：</b>'+str(round(get_jiaquan(sumlistcourse,sumlistxuefen),5))+'\n<b>总GPA：</b>'+str(round(get_jiaquan(sumlistgpa,sumlistxuefen),5))+'\nVersion:3.0\nLastUpdate:2023-07-08'
        
        print( sumlistxuefen,sumlistgpa,sumlistcourse)
        send_mail()
    f2=open('scorelist.txt','w')
    for dic in sumscorelist:
        f2.write(str(dic)+'\n')
    f2.close()
    listxuefen.clear()
    listgpa.clear()
    listcourse.clear()
    sumlistxuefen.clear()
    sumlistgpa.clear()
    sumlistcourse.clear()
    time.sleep(60)
