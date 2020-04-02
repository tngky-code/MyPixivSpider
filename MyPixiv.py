import requests
import os
from lxml import etree
import re
import threading
from queue import Queue
import urllib3
import urllib
import time
from datetime import datetime
import math

urllib3.disable_warnings()

class MyPixiv:
    def __init__(self):
        self.folder = 'PixivIllust'
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.defaultheader = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "",
            "Connection": "keep-alive",
            "Cookie":"first_visit_datetime_pc=2019-12-19+21%3A16%3A37; p_ab_id=0; p_ab_id_2=1; p_ab_d_id=881214245; yuid_b=FWMjGHk; _ga=GA1.2.1087647723.1576757808; __utmz=235335808.1578016887.2.2.utmcsr=mail.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/; a_type=0; b_type=1; login_ever=yes; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_r=; __utma=235335808.1087647723.1576757808.1578023672.1578055255.4; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=46683836=1^9=p_ab_id=0=1^10=p_ab_id_2=1=1^11=lang=zh=1; privacy_policy_agreement=1; _gcl_au=1.1.1653015041.1580380812; r_control_flg=1; _fbp=fb.1.1580380851030.1081795253; rpr_opted_in=1; rpr_uid=09eef720-434d-11ea-9aa6-a9c9887a491e; rpr_is_first_session={%2209eef720-434d-11ea-9aa6-a9c9887a491e%22:1}; PHPSESSID=46650191_xre4dorUT3VOBNkhOGiGtMA5ZxPZcMUm; device_token=7836b37476f21c4be3662fc1590acab4; c_type=24; is_sensei_service_user=1; ki_t=1578016936094%3B1585503148494%3B1585503148494%3B4%3B29; _gid=GA1.2.2078855852.1585503177; tag_view_ranking=_hSAdpN9rx~LJo91uBPz4~RTJMXD26Ak~0xsDLqCEW6~zIv0cf5VVk~t6fkfIQnjP~7WfWkHyQ76~bQoXeIPKKf~ynPLKWGJ1A~m3EJRa33xU~xxn1Q-SAfT~0AlZ2ckzFV~O0WKFZuVbs~ojOWqUhaaT~l-hI-mMchl~XALOkB5ogB~qiGiRRx4e5~OZdc679bTj~BU9SQkS-zU~y8GNntYHsi~HRnhV4P3Qr~jEyj-WOP42~KN7uxuR89w~VJ2-8NDjhH~xZ6jtQjaj9~ugMBP7-Qst~fUbMkuz-EA~pNfuh5ybtG~OSHWvWBpo9~cFYMvUloX0~ZZltVrbyeV~CbhyJ8r4Mo~mHukPa9Swj~1D1VEfvFR5~TBAh5YDdLW~jfnUZgnpFl~t3UPOSEYYz~DHqIUplIEc~rIphCTR6YP~0PNozdwbIq~vo3OX2PTkY~go5jE8nqWm~0J0e27QDgN~UllT3Di21R~xieAY3Zk0r~O1fcKKXBq1~XRVfX4SbmB~dIjQ8RA3xH~6mJb502bSm~UP12ShuBVx~l0PkfZ9vV7~3W4zqr4Xlx~dyJbxIRsK9~ETjPkL0e6r~eASpjB2X6M~EMLHXCKsfZ~5oPIfUbtd6~Ie2c51_4Sp~AMwBN_-Fo_~2-ZLcTJsOe~3EPEM1BGbJ~_fMf86iA_3~HQrKJY4TRh~oq1xLIbBpj~Ru77CoMVRH~ePqY0MNwHR~KZK1KvTPMp~rGFlnffUQd~Yvn1eEKXNf~UR3UZdHtim~5sExEHA8P5~B6uEbiYg7i~CluIvy4vsU~MKnVucuYOn~WM3631l9jF~spPqEvHEF2~1G1bsV2xcg~lJoTN1o2SZ~1MsYTGMqRa~QTp6AjCbvf~yRoNh0Qhm9~FVapwIXT4j~QGRWD70vj2~sQC4pGQx9E~JVFA1XydrI~8WJVvxbZJ2~D6TnwR9Jia~SQZaakhtVv~ATwfQNRWoV~woYIyNhisG; _gat_UA-1830249-3=1"
        }
        self.illust_id_list=[]
        self.num = 0
        self.now=str(datetime.now()).split(' ')[0]

    def get_response(self,url,headers,is_byte=False):
        r=requests.get(url,verify=False,headers=headers)
        if r.status_code != 200:
            r.raise_for_status()
        if is_byte:
            while str(len(r.content)) != r.headers["Content-Length"]:
                time.sleep(1)
                r=requests.get(url,verify=False,headers=headers)
        return r

    def get_ranking_illust(self,mode=0,content=0,illust_num=100):
        #daily_folder="daily_illust"+'_'+self.now+'_'+str(illust_num)
        #daily_folder="weekly_illust"+'_'+self.now+'_'+str(illust_num)
        #daily_folder="monthly_illust"+'_'+str(illust_num)
        #daily_folder="male_r18_illust"+'_'+str(illust_num)
        #daily_folder="weekly_r18_illust"+'_'+str(illust_num)
        daily_folder="daily_r18_illust"+'_'+self.now+'_'+str(illust_num)
        self.folder=os.path.join(self.folder,daily_folder)
        for i in range(math.ceil(illust_num/50)):
            self.illust_id_list+=self.get_illust_id(page=i+1)
        self.check_folder_and_illust()
        self.multi_get_illust(self.illust_id_list)
        
    def get_illust_id(self,mode=0,content=0,page=1):
        #ranking_url='https://www.pixiv.net/ranking.php?mode=monthly&content=illust&p={}'.format(page) #本月插画
        #ranking_url='https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={}'.format(page) #本日插画
        #ranking_url='https://www.pixiv.net/ranking.php?mode=weekly&content=illust&p={}'.format(page) #本周插画
        #ranking_url='https://www.pixiv.net/ranking.php?mode=male_r18&p={}'.format(page) #男R18插画
        #ranking_url='https://www.pixiv.net/ranking.php?mode=weekly_r18&content=illust&p={}'.format(page) #本周R18插画
        ranking_url='https://www.pixiv.net/ranking.php?mode=daily_r18&content=illust&p={}'.format(page) #本日R18插画
        r=self.get_response(ranking_url,self.defaultheader)
        HTML=etree.HTML(r.text)
        illust_url_temp_list=HTML.xpath('//img/@data-src')
        return [item.split('/')[-1].split('_')[0] for item in illust_url_temp_list]

    def check_folder_and_illust(self):
        loacl_illust_path="D:\MyFiles\Pictures\myillust"
        folder = os.path.join(self.root, self.folder)
        existed_file=self.get_local_file_list(folder)+self.get_local_file_list(loacl_illust_path)
        print("Exist Item:", len(existed_file))
        for illust_id in self.illust_id_list.copy():
            if illust_id in existed_file:
                self.illust_id_list.remove(illust_id)
        print(self.illust_id_list)

    def get_local_file_list(self,path):
        file_list=[]
        for file in [[file.split('_')[1] for file in files if '_' in file] for root,dirs,files in os.walk(path)]:
            file_list=file_list+file
        return file_list

    def get_illust_id_list_by_user_id(self,user_id):
        user_profile_ajax_url = "https://www.pixiv.net/ajax/user/{}/profile/all".format(str(user_id))
        page = self.get_response(user_profile_ajax_url,self.defaultheader)
        _data = re.findall('"[0-9]+":null', page.text)
        return [str(str(item).split(":")[0]).strip('"') for item in _data if ':null' in str(item)]

    def get_illusts_by_user_id(self,user_id):
        self.folder=os.path.join(self.folder,str(user_id))
        self.illust_id_list = self.get_illust_id_list_by_user_id(user_id)
        self.check_folder_and_illust()
        self.multi_get_illust(self.illust_id_list)

    def multi_get_illust(self,illust_id_list,max=20):
        get_illust_id_queue=Queue(maxsize=max)
        threads=[]
        task_main = threading.Thread(target=self.add_queue, args=(get_illust_id_queue, illust_id_list))
        task_main.setName("TaskMain")
        task_main.start()
        for i in range(max):
            task = threading.Thread(target=self.get_illust_by_id, args=(get_illust_id_queue,))
            task.start()
            threads.append(task)
        for _task in threads:
            _task.join()
        print("\nTotal Image: ", self.num)

    def add_queue(self,get_illust_queue,illust_id_list):
        for illust_id in illust_id_list:
            _illust_id=illust_id.strip()
            if illust_id and _illust_id:
                get_illust_queue.put(_illust_id)

    def get_illust_by_id(self,get_illust_id_queue):
        while True:
            if get_illust_id_queue.qsize()<=0:
                break
            illust_id = get_illust_id_queue.get()
            orginal_illust_urls,headers,illust_user_id = self.get_orginal_illust_url_by_id(illust_id)
            threads_temp=[]
            for orginal_illust_url in orginal_illust_urls:
                task = threading.Thread(target=self.save_illust, args=(orginal_illust_url,headers,illust_user_id,))
                task.start()
                threads_temp.append(task)
            for _task in threads_temp:
                _task.join()

    def save_illust(self,orginal_illust_url,headers,illust_user_id):
        illust_html=self.get_response(orginal_illust_url,headers,is_byte=True)
        name="{}_{}".format(illust_user_id,orginal_illust_url.rsplit('/',-1)[-1])
        folder = os.path.join(self.root, self.folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
        file = os.path.join(folder, str(name))
        with open(file,'wb') as ill:
            ill.write(illust_html.content)
        print("Pixiv Illust: [ OK | {} ]".format(file))

    def get_orginal_illust_url_by_id(self,illust_id):
        headers = self.defaultheader.copy()
        headers["Referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}".format(illust_id)
        illust_detail_url = "https://www.pixiv.net/touch/ajax/illust/details?illust_id={}".format(illust_id)
        illust_detail_html = self.get_response(illust_detail_url,headers)
        orginal_illust_urls = self.get_orginal_illust_urls(illust_detail_html)
        illust_user_id = re.findall('"user_id":"[^"]*"', illust_detail_html.text)[0].split(':',1)[-1].strip('"')
        return orginal_illust_urls,headers,illust_user_id

    def get_orginal_illust_urls(self,illust_detail_html):
        orginal_illust_urls=[]
        for url in re.findall('"url_big":"[^"]*"', illust_detail_html.text):
            if url not in orginal_illust_urls:
                orginal_illust_urls.append(url) 
        return [url.replace('\\', '').split(':', 1)[-1].strip('"') for url in orginal_illust_urls ] 

if __name__ == '__main__':
    p=MyPixiv()
    #p.get_ranking_illust()
    p.get_illusts_by_user_id(9212166)

    #print(p.get_illust_id(mode=1,content=1)+p.get_illust_id(mode=1,content=1,page=2))
    #print(len(p.get_illust_id(mode=1,content=1)+p.get_illust_id(mode=1,content=1,page=2)))

