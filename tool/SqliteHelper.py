import sqlite3


class SqliteHelper:

    def create_table(self):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql='''CREATE TABLE illust(
            illust_id INT PRIMARY KEY,
            illust_user_id INT,
            title TEXT,
            bookmarkCount int,
            likeCount INT,
            viewCount INT,
            tags TEXT,
            illust_status INT
            )
            '''
        cursor.execute(sql)
        cursor.close()
        conn.close()

    def insert_data(self,data):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql="insert into illust(illust_id,illust_user_id,title,bookmarkCount,likeCount,viewCount,tags,illust_status)values({},{},'{}',{},{},{},'{}',{})".format(data["illust_id"],data["illust_user_id"],data["title"],
        data["bookmarkCount"],data["likeCount"],data["viewCount"],
        data["tags"],data["illust_status"])
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def select_data(self):
        conn=sqlite3.connect('illust_data.db')
        cursor=conn.cursor()
        sql="SELECT * FROM `illust`"
        cursor.execute(sql)
        cursor.close()
        conn.close()

if __name__ == '__main__':
    sqlite_helper=SqliteHelper()
    #sqlite_helper.create_table()
    tags=['アイドルマスターミリオンライブ!', '最上静香', '北沢志保', 'ポケモン', 'C96', 'イワンコ', 'ミリポケ', 'Pokem@s', 'ルガルガン', 'アイマス500users入り'] 
    #【C96新刊】カランコエ '_'.join(tags)
    illust_data={
        "illust_id":76169625,
        "illust_user_id":46650191,
        "title":"【C96新刊】カランコエ",
        "bookmarkCount":754,
        "likeCount":574,
        "viewCount":16442,
        "tags": '_'.join(tags),
        "illust_status":0,
    }
    print(illust_data["tags"])
    sqlite_helper.insert_data(data=illust_data)
