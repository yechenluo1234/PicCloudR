# 关于本项目

一个基于 `python` 的 *简单* 图床实现

此项目为作者的第一个 `python` 项目，会有很多不足之处
> 作者没有学过python（抹汗）

## 已实现功能

1. 通过base64上传图片接口
2. 登录接口

# 项目搭建

### 修改配置

修改 `config` 下的 `config.py` 文件

```py
# 保存文件位置（绝对路径）
UPLOAD_FOLDER = r'UPLOAD_FOLDER'

# JET SECRET KEY
JWT_SECRET_KEY = 'JWT_SECRET_KEY'

# 管理员账号及密码
ADMIN_USERNAME='admin'
ADMIN_PASSWORD='123123'

# 端口号
PORT = 5000
```

### 启动项目

```bash
pip install -r requirements.txt
py run.py
```

# 接口文档

## 登录接口

接口地址：`/api/login`

接口类型：`POSH`

接口参数：

```json
{
    "username": "admin",
    "password": "123123"
}
```

响应内容：

```json
{
	"message": "登录成功",
	"token": ""
}
```

## 上传接口 

### 通过base64上传图片

接口地址：`/api/uploadByBase64`

接口类型：`POSH`

接口参数： 

> 注：需传递 `token` 通过 `Authorization` 请求头

```json
{
    "filename": "1.png",
    "imageBase64": ""
}
```

> 注：文件名为 `filename` 文件已存在时会重新命名文件

响应内容：

```json
{
	"file_url": "/images/1.png",
	"message": "图片上传成功"
}
```

> 注：图片访问地址为 `url` + `file_url` 如 `http://127.0.0.1:5000/images/1.png`
