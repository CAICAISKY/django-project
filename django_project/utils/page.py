import math

from django.db import connection


class PageException(Exception):
    """ 分页器异常类 """
    def __str__(self):
        return "传入的页码不对，请传入正确页码！"


class MyPaginator:
    """ 自定义分页器 """
    def __init__(self, sql, *, params=None, page_size, page_num):
        """
        分页器构造函数
        :param sql: sql语句
        :param params: sql的参数,必须为可迭代对象
        :param page_size: 每页多少条
        :param page_num: 页码
        """
        self.sql = sql
        self.params = params if params is not None else []
        self.page_size = page_size
        self.offset = (page_num - 1) * page_size
        if page_num > self.num_pages or page_num < 1:
            raise PageException

    def page_data(self):
        """
        获取查询数据
        :return: 数据的列表
        """
        sql = self.sql[0: len(self.sql) - 1] + ' LIMIT %s OFFSET %s'
        cursor = connection.cursor()
        params = self.params.copy()
        params.append(self.page_size)
        params.append(self.offset)
        cursor.execute(sql, params)
        return cursor.fetchall()

    @property
    def num_pages(self):
        """ 获取总页数 """
        return math.ceil(self.count / self.page_size)

    @property
    def count(self):
        """ 获取总记录数 """
        sql = 'select count(1) from ({0}) as for_count'.format(self.sql[0: len(self.sql) - 1])
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql, self.params)
        return cursor.fetchone()[0]
