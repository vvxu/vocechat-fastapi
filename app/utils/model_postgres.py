import psycopg2
from psycopg2 import errors
from passlib.context import CryptContext
import json
import psycopg2.extras


class PostgreSQLClient:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        """
        :param 
           # 普通搜索可以用这个方式
           query: query like this f"SELECT * FROM {table} WHERE id=1"
           query = f"SELECT * FROM {table} WHERE json_data->>'name' = '王小虎'"
        """
        # 原来的方法
        # self.cursor.execute(query)
        # return self.cursor.fetchall()
        # 新方法
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        results = [dict(row) for row in rows]
        return results

    # 这是一个无脑型插入，不管数据是否重复
    def execute_insert(self, table, values):
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(values.values()))
        self.connection.commit()

    # 插入json
    def execute_insert_json(self, table, values):
        """
        values_dict 必须报告一个json_data的key
        values_dict = {"参数1": "内容1", "参数2": "内容2"..."json_data": "json内容"}
        json内容可以放入dict，自动转为json
        """
        try:
            columns = ', '.join(values.keys())
            placeholders = ', '.join(['%s'] * len(values))
            value_list = []
            for keys, data in values.items():
                if keys == "json_data":
                    value_list.append(json.dumps(data))
                else:
                    value_list.append(data)
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
            self.cursor.execute(query, value_list)
            self.connection.commit()
            return {"code": 0, "msg": f"json数据添加成功!"}
        except:
            return {"code": 1, "msg": f"json数据必须放在json_data下。"}

    def execute_update(self, table, set_values, where_condition):
        try:
            set_columns = ', '.join([f"{key} = %s" for key in set_values.keys()])
            query = f"UPDATE {table} SET {set_columns} WHERE {where_condition}"
            self.cursor.execute(query, list(set_values.values()))
            self.connection.commit()
            return {"code": 0, "msg": f"数据更新成功!"}
        except:
            return {"code": 1, "msg": f"数据更新失败。"}

    def execute_delete(self, table, where_condition):
        """
        :param table:  表名
        :param where_condition: 删除的字段比如，id=1 
        :return: 
        """
        try:
            query = f"DELETE FROM {table} WHERE {where_condition}"
            self.cursor.execute(query)
            self.connection.commit()
            return {"code": 0, "msg": f"数据删除成功!"}
        except:
            return {"code": 1, "msg": f"数据删除失败!"}
        
    # 添加数据，先检查索引是否存在。
    def insert_if_not_exist(self, table, field, values):
        """
        :param table: 表的名称
        :param field: 需要检索是否存在的字段名称
        :param values: 插入内容
        :return: 
        """
        field_value = values[field]

        # 检查数据是否已存在
        query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {field} = %s)"
        self.cursor.execute(query, (field_value,))
        username_exists = self.cursor.fetchone()[0]

        if not username_exists:
            columns = ', '.join(values.keys())
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, list(values.values()))
            self.connection.commit()
            return {"code": 0, "msg": f"数据 '{field_value}' 添加成功!"}
        else:
            return {"code": 1, "msg": f"数据 '{field_value}' 已经存在。"}
