# 导入pymysql模块
import pymysql
import wx
import time

class Sql_operation(object):
    '''数据库操作'''

    # 用构造函数实现数据库连接，并引入mydb参数，实现调用不同的数据库
    def __init__(self, host, mydb, port, user, password):
        # 实例变量
        self.connect_success = 0
        # 打开数据库连接
        try:
            self.db = pymysql.connect(host=host, port=int(port), user=user, password=password,
                                      db=mydb,
                                      charset="utf8")
            # 创建游标对象
            self.cursor = self.db.cursor()
            self.connect_success = 1
        except Exception as e:
            raise e

    # 查询记录.
    def SelectRecord(self, sql, param):
        try:
            if param == ():
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, param)
            # 处理结果
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            raise e

    # 添加记录.
    def AddRecord(self, sql, param):
        try:
            self.cursor.execute(sql, param)  # 添加多条记录.
            self.db.commit()
        except Exception as e:
            raise e

    # 更新记录.
    def UpdateData(self, sql, param):
        try:
            self.cursor.execute(sql, param)
            self.db.commit()
        except Exception as e:
            raise e

    # 删除记录.
    def DeleteRecord(self, sql, param):
        try:
            self.cursor.execute(sql, param)
            self.db.commit()
        except Exception as e:
            raise e

    # 用析构函数实现数据库关闭
    def __del__(self):
        # 关闭数据库连接
        self.db.close()
        self.cursor.close()
