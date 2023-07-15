from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, Depends, status
from jose import JWTError, jwt
from fastapi import APIRouter
import time
import json

# 引用crud中的users
from app.crud.sys_users import *
from app.utils.model_postgres import *

# 构建app
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/users/login", tags=["users"])
async def user_login(form_data: UserLogin):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'code': 60204, 'message': '账号或密码错误.'}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["user_name"]}, expires_delta=access_token_expires)
    return {"code": 20000, "data": {"token": access_token}}


@router.get("/users/info", tags=["users"])
async def user_info(current_user: UserInfo = Depends(get_current_active_user)):
    res = get_user_info("user_info", "user_id", current_user["user_id"])
    res_msg = {
        "code": 20000,
        "data": {
            "roles": [
                current_user['role']
            ],
            "introduction": res["introduction"],
            "avatar": res["avatar"],
            "name": res["name"]
        }
    }
    return res_msg


@router.post("/users/logout", tags=["users"])
async def user_logout():
    return {'code': 20000, 'data': 'success'}


@router.get("/users/transaction/list", tags=["users"])
async def users_transaction_list(current_user: UserInfo = Depends(get_current_active_user)):
    mock_msg = {
        'code': 20000,
        'data': {
            'total': 20,
            'items|20': [{
                'order_no': '@guid()',
                'timestamp': int(time.time()),
                'username': '@name()',
                'price': '@float(1000, 15000, 0, 2)',
                'status|1': ['success', 'pending']
            }]
        }
    }
    return mock_msg


