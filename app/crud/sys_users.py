from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status

from app.models.users import *
from app.utils.model_postgres import *
from app.core.config import Settings

# 密码生成函数
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = Settings.Api["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.Api["access_token_expire_minutes"]


# 创建一个PostgreSQLClient实例
client = PostgreSQLClient(
    dbname=Settings.Postgres["dbname"], 
    user=Settings.Postgres["user"], 
    password=Settings.Postgres["password"], 
    host=Settings.Postgres["host"], 
    port=Settings.Postgres["port"])


# 创建用户
def create_user(user_name, password, role, department_id=None, permissions_id=None):
    user_data = {
        'user_name': user_name,
        'password': get_password_hash(password),
        'role': role
    }
    if department_id is not None:
        user_data['department_id'] = department_id
    if permissions_id is not None:
        user_data['permissions_id'] = permissions_id
    # 连接到数据库
    client.connect()
    res = client.insert_if_not_exist("users", "user_name", user_data)
    client.disconnect()
    return res


# 插入用户信息
def insert_user_info(user_id, name, introduction, email, avatar):
    user_info_data = {
        'user_id': user_id,
        'name': name,
        'introduction': introduction,
        'email': email,
        'avatar': avatar
    }
    # 连接到数据库
    client.connect()
    res = client.insert_if_not_exist("user_info", 'user_id', user_info_data)
    client.disconnect()
    return res


# 获取用户数据
def get_user(table, field, keys):
    query = f"SELECT * FROM {table} WHERE {field} = %s"
    # 连接到数据库
    client.connect()
    client.cursor.execute(query, (keys,))
    result = client.cursor.fetchall()

    if not result:
        client.disconnect()
        return None

    columns = [desc[0] for desc in client.cursor.description]

    query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {field} = %s)"
    client.cursor.execute(query, (keys,))
    keys_exists = client.cursor.fetchone()[0]
    client.disconnect()

    if keys_exists:
        result_dict = [dict(zip(columns, row)) for row in result]
        return result_dict[0]
    else:
        return None


# 获取用户信息
def get_user_info(table, field, keys):
    query = f"SELECT * FROM {table} WHERE {field} = %s"
    # 连接到数据库
    client.connect()
    client.cursor.execute(query, (keys,))
    result = client.cursor.fetchall()

    if not result:
        client.disconnect()
        return None

    columns = [desc[0] for desc in client.cursor.description]

    query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {field} = %s)"
    client.cursor.execute(query, (keys,))
    keys_exists = client.cursor.fetchone()[0]
    client.disconnect()

    if keys_exists:
        result_dict = [dict(zip(columns, row)) for row in result]
        return result_dict[0]
    else:
        return None


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 转换密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 赋权
def authenticate_user(username: str, password: str):
    user = get_user("users", "user_name", username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


# 创建token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.Api["secret_key"], algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings.Api["secret_key"], algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user("users", "user_name", token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInfo = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="未激活用户")
    return current_user