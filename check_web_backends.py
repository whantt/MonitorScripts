#!/usr/bin/python
import commands
import time
import os
import sys

__author__='Hoo'

WEB_BACKENDS={'www.kldjy.com':['192.168.168.121:80','192.168.168.123:80'],
        'iphone.kldjy.com':['192.168.168.121:80','192.168.168.123:80'],
        'user.xixi.com.cn':['192.168.168.119:80/checkstatus.php','192.168.168.124:80/checkstatus.php'],
        'sv.xixi.com.cn':['192.168.168.103:80','192.168.168.104:80'],
        'umsa.xixi.com.cn':['192.168.168.105:80'],
        'ums.xixi.com.cn':['192.168.168.117:88/release/checkstatus.ums','192.168.168.118:88/release/checkstatus.ums','192.168.168.128:88/release/checkstatus.ums'],
        'kz.xixi.com.cn':['192.168.169.31:80/checkstatus.php','192.168.169.33:80/checkstatus.php'],
        'qcode.xixi.com.cn':['192.168.168.103:80/checkstatus.php','192.168.168.104:80/checkstatus.php'],
        'open.xixi.com.cn':['192.168.168.103:80/checkstatus.php','192.168.168.104:80/checkstatus.php'],
        'map.xixi.com.cn':['192.168.168.103:80/checkstatus.php','192.168.168.104:80/checkstatus.php'],
        'weixin.xixi.com.cn':['192.168.168.103:80/checkstatus.php','192.168.168.104:80/checkstatus.php'],
        'boss.xixi.com.cn':['192.168.168.101:80/checkstatus.php'],
        'channel.xixi.com.cn':['192.168.168.102:80/checkstatus.php','192.168.168.106:80/checkstatus.php'],
        'shop.xixi.com.cn':['192.168.168.102:80/checkstatus.php','192.168.168.106:80/checkstatus.php'],
        'img1.kldjy.com':['192.168.168.137:80','192.168.168.114:80'],
        'www.xixi.com.cn':['192.168.168.102:80','192.168.168.106:80'],
        'www.navione.com.cn':['192.168.168.102:80','192.168.168.106:80'],
        'lbs.xixi.com.cn':['192.168.168.120:80/ds/'],
        'hy.xixi.com.cn':['192.168.168.103:80','192.168.168.104:80'],
        'hnradio.kldlk.com':['192.168.168.120:80'],
        'navi.xixi.com.cn':['192.168.169.21:80/cgi/cgi_test.ums?test=cgitest','192.168.169.22:80/cgi/cgi_test.ums?test=cgitest','192.168.169.23:80/cgi/cgi_test.ums?test=cgitest','192.168.169.36:80/cgi/cgi_test.ums?test=cgitest','192.168.169.37:80/cgi/cgi_test.ums?test=cgitest','192.168.169.38:80/cgi/cgi_test.ums?test=cgitest','192.168.169.39:80/cgi/cgi_test.ums?test=cgitest','192.168.169.40:80/cgi/cgi_test.ums?test=cgitest','192.168.169.41:80/cgi/cgi_test.ums?test=cgitest'],
        'st.xixi.com.cn':['192.168.168.109/tc/controlpanel/login.php','192.168.168.113/tc/controlpanel/login.php','192.168.168.112/tc/controlpanel/login.php','192.168.168.107/tc/controlpanel/login.php'],
        'hyapi.xixi.com.cn':['192.168.168.102:80/checkstatus.php','192.168.168.106:80/checkstatus.php']
        }


def check_backend(domain,url):
    cmd='curl --head -H "Host:%s" %s |grep "200 OK" &>/dev/null' %(domain,url)
    res=commands.getstatusoutput(cmd)
    if res[0] !=0:
        return True

Old_Hosts={}
New_Hosts={}
Rate=60
def main(domain,Hosts):
    if domain in WEB_BACKENDS:
        hosts=[]
        flag=False
        for backend in WEB_BACKENDS[domain]:
            if check_backend(domain,backend):
                #print 'the domain: %s   backend: %s  not available' %(domain,backend)
                hosts.append(backend.split('/')[0])
                Hosts[domain]=hosts
                if not flag:
                    flag=True
            else:
                pass
                #print 'the domain: %s   backend: %s  is ok' %(domain,backend)
        if flag:
            comments=domain+"-Backends-"
            for h in hosts:
                comments=comments+h+"-Failed"
            f_name='/tmp/%s' %domain
            f=open(f_name,'w')
            f.write(comments)
            f.close()
        else:
            pass            
            #if os.path.exists('')




def start():
    global WEB_BACKENDS,Old_Hosts,New_Hosts,Rate
    list=[]
    for i in WEB_BACKENDS.iterkeys():
        main(i,Old_Hosts)
    time.sleep(Rate)
    for i in WEB_BACKENDS.iterkeys():
        main(i,New_Hosts)
    if New_Hosts:
        for domain in New_Hosts.iterkeys():
           if domain in Old_Hosts:
                  for h in Old_Hosts[domain]:
                      print h.split('/')[0]
                      f='/tmp/.domain_%s_%s' %(domain,h.split('/')[0])
                      if not os.path.exists(f):
                         os.system('touch %s' %f)
                         messages="PROBLEM_:%s_%s__has_failed" %(domain,h.split('/')[0])
                         os.system('bash /soft/zabbix/share/zabbix/alertscripts/web_backend.sh "%s"' %messages)
                         print 'send warning sms'
    
    res=os.system('ls /tmp/.domain_* &>/dev/null')
    if res == 0:
        res,out=commands.getstatusoutput(r'ls /tmp/.domain_*')
        recovery={}
        for var in out.split('\n'):
           List=var.strip().split('_')
           if not List[1] in recovery:
                  recovery[List[1]]=[List[2]]
           else:
                  tmp_list=recovery[List[1]]
                  tmp_list.append(List[2])
                  recovery[List[1]]=tmp_list
        for fail_domain in recovery.iterkeys():
           if not fail_domain in New_Hosts:
                  print 'this domain: %s begain to recovery' %fail_domain
                  f=r'/tmp/.domain_%s_*' %(fail_domain)
                  os.system('rm -rf %s' %f)
                  messages="OK_:%s__all_backend_hosts_has_UP" %fail_domain
                  os.system('bash /soft/zabbix/share/zabbix/alertscripts/web_backend.sh "%s"' %messages)
                  print 'send recovery sms'
           else:
                  fail_hosts=recovery[fail_domain]
                  for fail_host in fail_hosts:
                           for h in New_Hosts[fail_domain]:
                                if fail_host != h.split('/')[0]:
                                   print 'host_ip: %s recovery ' %fail_host
                                   f='/tmp/.domain_%s_%s' %(fail_domain,fail_host)
                                   os.system('rm -f %s' %f)                                  
                                   messages="OK_:%s__%s__has_Recovered" %(fail_domain,fail_host)
                                   os.system('bash /soft/zabbix/share/zabbix/alertscripts/web_backend.sh "%s"' %messages)
                                   print 'send recovery sms'
if __name__ == '__main__':
    start()    
                           
