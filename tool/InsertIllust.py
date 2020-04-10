import requests
import time
import os
import re
from datetime import datetime
import tool.SqliteHelper
import threading
from queue import Queue

def get_response(url,headers,is_byte=False):
    r=requests.get(url,verify=False,headers=headers)
    if r.status_code != 200:
        r.raise_for_status()
    if is_byte:
        while str(len(r.content)) != r.headers["Content-Length"]:
            time.sleep(1)
            r=requests.get(url,verify=False,headers=headers)
    return r

def get_local_illust_id_list(path):
    file_list=[]
    for file in [[file.split('_')[1] for file in files if '_' in file] for root,dirs,files in os.walk(path)]:
        file_list=file_list+file
    return list(set(file_list))

def get_illust_data_by_id(illust_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "",
        "Connection": "keep-alive",
        "Cookie":"first_visit_datetime_pc=2019-12-19+21%3A16%3A37; p_ab_id=0; p_ab_id_2=1; p_ab_d_id=881214245; yuid_b=FWMjGHk; _ga=GA1.2.1087647723.1576757808; __utmz=235335808.1578016887.2.2.utmcsr=mail.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/; a_type=0; b_type=1; login_ever=yes; ki_r=; __utma=235335808.1087647723.1576757808.1578023672.1578055255.4; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=46683836=1^9=p_ab_id=0=1^10=p_ab_id_2=1=1^11=lang=zh=1; privacy_policy_agreement=1; _gcl_au=1.1.1653015041.1580380812; r_control_flg=1; _fbp=fb.1.1580380851030.1081795253; rpr_opted_in=1; rpr_uid=09eef720-434d-11ea-9aa6-a9c9887a491e; rpr_is_first_session={%2209eef720-434d-11ea-9aa6-a9c9887a491e%22:1}; device_token=7836b37476f21c4be3662fc1590acab4; c_type=24; is_sensei_service_user=1; _gid=GA1.2.729629252.1585909235; tag_view_ranking=_hSAdpN9rx~0xsDLqCEW6~LJo91uBPz4~RTJMXD26Ak~BU9SQkS-zU~q3eUobDMJW~y8GNntYHsi~zIv0cf5VVk~RcahSSzeRf~FqVQndhufZ~t6fkfIQnjP~7WfWkHyQ76~bQoXeIPKKf~ynPLKWGJ1A~m3EJRa33xU~xxn1Q-SAfT~0AlZ2ckzFV~O0WKFZuVbs~ojOWqUhaaT~l-hI-mMchl~XALOkB5ogB~52-15K-YXl~WcTW9TCOx9~5tNe8-14sj~ETjPkL0e6r~eaDKZUabpN~NjPfpD1o9t~yUv36CqH7A~engSCj5XFq~i4xDq8M0zV~yS_WrRrWFi~mhPeEpcp6t~xYzU0doFjn~qiGiRRx4e5~OZdc679bTj~HRnhV4P3Qr~jEyj-WOP42~KN7uxuR89w~VJ2-8NDjhH~xZ6jtQjaj9~ugMBP7-Qst~fUbMkuz-EA~pNfuh5ybtG~OSHWvWBpo9~cFYMvUloX0~ZZltVrbyeV~CbhyJ8r4Mo~mHukPa9Swj~1D1VEfvFR5~TBAh5YDdLW~jfnUZgnpFl~t3UPOSEYYz~DHqIUplIEc~rIphCTR6YP~0PNozdwbIq~vo3OX2PTkY~go5jE8nqWm~0J0e27QDgN~ie0shhAARr~Sbp1gmMeRy~gooMLQqB9a~9V46Zz_N_N~0Sds1vVNKR~JN2fNJ_Ue2~oMYuHRGe9g~mir4aNx9oM~4D-QY0hPsZ~QaiOjmwQnI~TALRqPdJaG~McuMpY73VJ~FhRjOaU1Yv~JPMKh5CRaK~H8cy1mILiB~skx_-I2o4Y~Dd2BFtvC_a~AI_aJCDFn0~TmJBC3K3bw~duocPQtNzV~-MuiEJf_Sr~UFjxr4OIYz~6293srEnwa~tKWyFlqScc~QL2G1t5h_V~AZ1ov2QNRs~EUwzYuPRbU~MzyhgX0YIu~u8McsBs7WV~k6ivnrAmsH~qBVGbZbpq5~ujS7cIBGO-~_3oeEue7S7~pnFCwAsnT2~orHGhUVIu0~TWrozby2UO~Lpw_C4vO0A~jrclGyQTmB~CZnOKinv48~VYDUiRsHt2~OBJrLjuGCM~CSLXxI4q2n; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_bc=1; PHPSESSID=46650191_4ZN8oQNoBO2dKvOuXBOY1O9END5faaoa; _gat=1; _gat_UA-1830249-138=1; ki_t=1578016936094%3B1585909254947%3B1585915661094%3B7%3B35"
    }
    headers["Referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}".format(illust_id)
    illust_detail_url = "https://www.pixiv.net/artworks/{}".format(illust_id)
    illust_detail_html = get_response(illust_detail_url,headers)
    tags=re.findall('"tag":"([^"]*)"',illust_detail_html.text)
    illust_data={
        "illust_id":illust_id,
        "illust_user_id":int(re.findall('"userId":"([^"]*)"',illust_detail_html.text)[0]),
        "title":re.findall('"title":"([^"]*)"',illust_detail_html.text)[0],
        "bookmark_count":re.findall('"bookmarkCount":([^"]*),',illust_detail_html.text)[0],
        "like_count":re.findall('"likeCount":([^"]*),',illust_detail_html.text)[0],
        "view_count":re.findall('"viewCount":([^"]*),',illust_detail_html.text)[0],
        "tags": '_'.join(tags),
        "illust_status":2,
        "illust_create_time":str(datetime.now()),
        "data_create_time":re.findall('"createDate":"([^"]*)"',illust_detail_html.text)[0],
    }
    return illust_data

def multi_get_illust_data(loacl_illust_list,max=10):
    loacl_illust_list_queue=Queue(maxsize=max)
    threads=[]
    task_main = threading.Thread(target=add_queue, args=(loacl_illust_list_queue, loacl_illust_list))
    task_main.setName("TaskMain")
    task_main.start()

    for i in range(max):
        task = threading.Thread(target=save_illust_data, args=(loacl_illust_list_queue,))
        task.start()
        threads.append(task)
    for _task in threads:
        _task.join()

def add_queue(loacl_illust_list_queue, loacl_illust_list):
    for illust_id in loacl_illust_list:
        _illust_id=illust_id.strip()
        if illust_id and _illust_id:
            loacl_illust_list_queue.put(_illust_id)

def save_illust_data(loacl_illust_list_queue):
    while True:
        if loacl_illust_list_queue.qsize()<=0:
            break
        illust_id=loacl_illust_list_queue.get()
        Sqlite_Helper=SqliteHelper.SqliteHelper()
        if Sqlite_Helper.check_data_exist_by_id(illust_id):
            continue
        else:
            illust_data= get_illust_data_by_id(illust_id)
            Sqlite_Helper.insert_data(illust_data)
    

if __name__ == '__main__':
    loacl_illust_path=r"D:\MyCode\Python\PixivIllust\trash"
    loacl_illust_list=get_local_illust_id_list(loacl_illust_path)
    multi_get_illust_data(loacl_illust_list)
    #illust_data=get_illust_data_by_id(80594510)
    #Sqlite_Helper=SqliteHelper.SqliteHelper()
    #Sqlite_Helper.insert_data(illust_data)
    filer_tags=["ゲイ","ホモ","巨根","雄っぱい","逆フェラ"
    ,"ふたなり","獣姦","腐向け","妊娠","妊婦","服越し母乳"]


    