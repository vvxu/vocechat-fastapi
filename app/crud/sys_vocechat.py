# 引用utils中的方法
from app.utils.model_postgres import *
# 引用config中的方法
from app.core.config import *


# 创建一个PostgreSQLClient实例
client = PostgreSQLClient(
    dbname=Settings.Postgres["dbname"], 
    user=Settings.Postgres["user"], 
    password=Settings.Postgres["password"], 
    host=Settings.Postgres["host"], 
    port=Settings.Postgres["port"])


def voce_find_all(table):
    query = f"SELECT * FROM {table}"
    client.connect()
    results = client.execute_query(query)
    client.disconnect()
    return results


# 查找聊天记录
def voce_find_something(table, field):
    query = f"SELECT * FROM {table} WHERE {field}"
    client.connect()
    results = client.execute_query(query)
    client.disconnect()
    return results


# 插入数据
def voce_insert_msg(table, created_at, user_id, role, msg):
    data = {
        'created_at': created_at,
        'user_id': user_id,
        'role': role,
        'msg': msg
    }
    client.connect()
    client.execute_insert(table, data)
    client.disconnect()


# 插入一个预设的角色
def voce_set_system(ai_system):
    data = {
        'system_name': ai_system[1],
        'system_descript': ai_system[2].replace("\n", ""),
    }
    client.connect()
    res = client.insert_if_not_exist("voce_server_store_system", "system_name", data)
    if res["code"] == 1:
        res = client.execute_update("voce_server_store_system", data, f"system_name='{ai_system[1]}'")
    client.disconnect()
    return res


# 初始插入
def voce_insert_chat_mode(user_id):
    update_data = {
        "user_id": user_id,
        "model": "0"
    }
    client.connect()
    client.insert_if_not_exist("voce_chat_mode", "user_id", update_data)
    client.disconnect()


# 更新用户的聊天模式
def voce_update_chat_mode(user_id, chat_mode):
    update_data = {"model": chat_mode}
    client.connect()
    res = client.execute_update("voce_chat_mode", update_data, f"user_id='{user_id}'")
    client.disconnect()
    return res


# 更新用户的角色设定
def voce_update_user_system(user_id, system):
    update_data = {"system": system}
    client.connect()
    res = client.execute_update("voce_chat_mode", update_data, f"user_id='{user_id}'")
    client.disconnect()
    return res


# 删除用户上下文聊天记录
def voce_delete_something(table, user_id):
    client.connect()
    res = client.execute_delete(table, f"user_id='{user_id}'")
    client.disconnect()
    return res


# 前端删除
def voce_web_delete_something(table, id):
    client.connect()
    res = client.execute_delete(table, f"id='{id}'")
    client.disconnect()
    return res
    

