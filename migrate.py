from app.crud.sys_users import *
from app.core.config import *


# 创建一个PostgreSQLClient实例
client = PostgreSQLClient(
    dbname=Settings.Postgres["dbname"], 
    user=Settings.Postgres["user"], 
    password=Settings.Postgres["password"], 
    host=Settings.Postgres["host"], 
    port=Settings.Postgres["port"])


def create_table(table, values):
    # Connect to the database
    client.connect()

    # Check if the table already exists
    check_table_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table}')"
    table_exists = False

    try:
        result = client.execute_query(check_table_query)
        if len(result) > 0 and result[0][0]:
            table_exists = True
    except Exception as e:
        print("Error occurred while checking table existence:", str(e))

    if table_exists:
        print(f"Table '{table}' already exists.")
    else:
        # Build the CREATE TABLE query
        columns = ', '.join([f"{key} {value}" for key, value in values.items()])
        create_table_query = f"CREATE TABLE {table} ({columns})"

        try:
            # Execute the query to create the table
            client.cursor.execute(create_table_query)
            client.connection.commit()
            print(f"Table '{table}' created successfully.")
        except Exception as e:
            print("Error occurred while creating table:", str(e))

    # Disconnect from the database
    client.disconnect()


# 用户表
table_Users = "users"
table_Users_Columns = {
    'user_id': 'SERIAL PRIMARY KEY',
    'user_name': 'VARCHAR(100)',
    'password': 'VARCHAR(100)',
    'role': 'VARCHAR(10)',
    'department_id': 'INTEGER',
    'permissions_id': 'VARCHAR(100)'
}

# userinfo
table_UserInfo = "user_info"
table_UserInfo_Columns = {
    'user_id': 'INTEGER',
    'name': 'VARCHAR(100)',
    'introduction': 'VARCHAR(100)',
    'email': 'VARCHAR(100)',
    'avatar': 'VARCHAR(100)'
}


# voce_chat
# 聊天模式
table_voce_current_chat_mode = "voce_chat_mode"
table_voce_current_chat_mode_columns = {
    'id': 'SERIAL PRIMARY KEY',
    'user_id': 'VARCHAR(100)',
    'model': 'VARCHAR(10)',
    'system': 'VARCHAR'
}

# 预制的系统行为
table_voce_server_store_system = "voce_server_store_system"
table_voce_server_store_system_columns = {
    'id': 'SERIAL PRIMARY KEY',
    'system_name': 'VARCHAR(100)',
    'system_descript': 'VARCHAR'
}

# 聊天记录完整
table_voce_temp_msg = "voce_temp_msg"
table_voce_temp_msg_columns = {
    'id': 'SERIAL PRIMARY KEY',
    'created_at': 'VARCHAR(20)',
    'user_id': 'VARCHAR(100)',
    'role': 'VARCHAR(20)',
    'msg': 'VARCHAR'
}


# 构建表格
# 创建其他数据表
create_table(table_Users, table_Users_Columns)
create_table(table_voce_current_chat_mode, table_voce_current_chat_mode_columns)
create_table(table_voce_server_store_system, table_voce_server_store_system_columns)
create_table(table_voce_temp_msg, table_voce_temp_msg_columns)


# 添加初始数据
# 创建账号
print(create_user(Settings.Admin["username"], Settings.Admin["password"], 'admin', 0, "admin"))
