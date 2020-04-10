import sqlite3
from datetime import datetime
import os


class SqliteHelper:

    def create_table(self):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql='''CREATE TABLE illust(
        illust_id INT PRIMARY KEY,
        illust_user_id INT,
        title TEXT,
        bookmark_count int,
        like_count INT,
        view_count INT,
        tags TEXT,
        illust_status INT,
        illust_create_time text,
        data_create_time text
        )
        '''
        cursor.execute(sql)
        cursor.close()
        conn.close()

    def insert_data(self,data):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        if not self.check_data_exist_by_id(data["illust_id"]):
            sql='''insert into illust(illust_id,illust_user_id,title,bookmark_count,like_count,view_count,tags,
            illust_status,illust_create_time,data_create_time)
            values({},{},'{}',{},{},{},'{}',{},'{}','{}')'''.format(data["illust_id"],data["illust_user_id"],data["title"],
            data["bookmark_count"],data["like_count"],data["view_count"],
            data["tags"],data["illust_status"],data["illust_create_time"],data["data_create_time"])
            print(sql)
            cursor.execute(sql)
            conn.commit()
        cursor.close()
        conn.close()

    def select_data(self):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql="SELECT * FROM illust"
        print(cursor.execute(sql)) 
        cursor.close()
        conn.close()

    def check_data_exist_by_id(self,id):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql="SELECT * FROM illust where illust_id={}".format(id)
        cursor.execute(sql)
        if len(cursor.fetchall()) > 0 :
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False

def test():
    sqlite_helper=SqliteHelper()
    #sqlite_helper.create_table()
    tags=['アイドルマスターミリオンライブ!', '最上静香', '北沢志保', 'ポケモン', 'C96', 'イワンコ', 'ミリポケ', 'Pokem@s', 'ルガルガン', 'アイマス500users入り'] 
    #【C96新刊】カランコエ '_'.join(tags)
    illust_data={
        "illust_id":76169625,
        "illust_user_id":46650191,
        "title":"【C96新刊】カランコエ",
        "bookmark_count":759,
        "like_count":578,
        "view_count":16687,
        "tags": '_'.join(tags),
        "illust_status":3,
        "illust_create_time":str(datetime.now()),
        "data_create_time":"2018-12-24T15:34:14+00:00",
    }
    #print(illust_data["tags"])
    #sqlite_helper.insert_data(data=illust_data)
    #sqlite_helper.select_data(illust_data)
    #print(str(datetime.now()))


if __name__ == '__main__':
    sqlite_helper=SqliteHelper()
    print(sqlite_helper.check_data_exist_by_id(76169625))
    #illust_status:3 r18 trash
