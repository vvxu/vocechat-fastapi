# vocechat-fastapi
用fastapi写的vocechat的api。
使用postgres存储聊天记录，实现上下文。
可以配置到vercel，但是vercel对响应时间有要求，不能超过10s，如果遇到chatgpt内容超过10秒的话会直接超时中断。

## 需要修改的地方
config
```commandline
app/core/config.py
```

bot_vocechat中，默认使用bot1，根据需要修改。
```commandline
app/utils/bot_vocechat.py
```

### config参数
#### Api
配置fastapi的一些参数

|参数名称| 作用                     |
|-|------------------------|
| HOST | fastapi主机地址  ： 0.0.0.0 |
| APP_NAME | app名称                  |
| PORT | 端口   ：22222            |   
| RELOAD | 自动重载   ：True           |  
| secret_key | JWT密钥                  |    
| access_token_expire_minutes | token存活时间：30           | 
| algorithm | 加密方式：HS256             | 

#### Openai
连接openai的参数

|参数名称| 作用            |
|-|---------------|
| secret | openaiapi的key |
| model | chatgpt版本: "gpt-3.5-turbo"   |

#### VoceChat
连接VoceChat的参数

| 参数名称                   | 作用                              |
|------------------------|---------------------------------|
| url                    | vocechat的url: https://voce.chat |
| bot_config.bot1.bot_id | 第一个机器人的id                       |
| bot_config.bot1.secret | 第一个机器人的secret                   |

#### Postgres
连接Postgres的参数，用来存储聊天记录，实现上下文。

| 参数名称                   | 作用                              |
|------------------------|---------------------------------|
| dbname                    | postgres_dbname |
| user | postgres_user                       |
| password | postgres_password                   |
| host | postgres_host                   |
| port | postgres_port                   |

#### admin
fastapi权限，

| 参数名称                   | 作用              |
|------------------------|-----------------|
| dbname       | postgres_dbname |
| username | fastapi账号       |
| password | fastapi密码       |



## 开始
```commandline
git clone https://github.com/vvxu/vocechat-fastapi.git
cd vocechat-fastapi
# 有上下文需求的配置
python migrate.py

pip install -r requirements.txt
python main.py
```


## 数据结构
```
├── main.py                    # 主文件
├── app                        # 
│   ├── api                    # 路由    
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core                     # 配置文件
│   │   ├── __init__.py
│   │   └── models.py
│   ├── crud                   # 数据库
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── log                     # 日志
│   │   ├── __init__.py
│   │   └── .txt
│   ├── models                 # 数据类型
│   │   ├── __init__.py
│   │   └── some_service.py
│   └── utils                   # 工具
│       ├── __init__.py
│       └──  some_utils.py
└── tests
    ├── __init__.py
    └── test_endpoints.py
```
