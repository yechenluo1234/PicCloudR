# 关于本项目

一个基于 `python` 的 _简单_ 图床实现

此项目为作者的第一个 `python` 项目，会有很多不足之处

> 作者没有学过 python（抹汗）

## 已实现功能

1. 通过 base64 上传图片接口
2. 登录接口
3. 图片根据日期分文件存储
4. 删除过时文件夹接口
5. 通过文件上传图片接口

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

#debug
DEBUG = False
```

### 启动项目

```bash
pip install -r requirements.txt
python run.py
# 可能为 python3 和 pip3
```

#### 解决反代导致返回的图片url协议错误:

1. Nginx
    ```yaml
    proxy_set_header X-Forwarded-Proto $scheme
    ```
2. Apache
    ```yaml
    RequestHeader set X-Forwarded-Proto "https" env=HTTPS
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

### 上传图片接口
接口地址: `/api/upload`

接口类型: `POST`

接口参数:


> 注：需传递 `token` 通过 `Authorization` 请求头，遵循 `Bearer Token`认证方案

+ image (类型: 文件)

   >上传的图片文件，支持格式：.jpg, .png, .gif

请求示例:
```typescript
import axios from 'axios';

// 获取文件上传的 input 元素
const fileInput = document.getElementById('your-file-input') as HTMLInputElement;
const imageFile = fileInput.files[0];

// 获取认证 Token
const token = 'your_token_here'; // 替换为实际的认证 token

// 构建 FormData 对象
const formData = new FormData();
formData.append('image', imageFile);

// 构建请求头部
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'multipart/form-data',
};

// 构建请求配置
const config = {
  headers: headers,
};

// 发起请求
axios.post('https://your-api-host/api/upload', formData, config)
  .then((response) => {
    console.log('Success:', response.data);
  })
  .catch((error) => {
    console.error('Error:', error.response.data);
  });
```

### 通过 base64 上传图片

接口地址：`/api/uploadByBase64`

接口类型：`POSH`

接口参数：

> 注：需传递 `token` 通过 `Authorization` 请求头，遵循 `Bearer Token`认证方案

```json
{
  "filename": "1.png",
  "imageBase64": ""
}
```

> 注：文件名为 `filename` 文件已存在时会重新命名文件

响应内容：

> 上传成功响应码为 `201`

```json
{
  "file_url": "http://127.0.0.1:5000/images/1.png",
  "message": "图片上传成功"
}
```


## 删除接口

### 删除过时文件夹

接口地址：`/api/deleteOldFiles`

接口类型：`POSH`

接口参数：

> 注：需传递 `token` 通过 `Authorization` 请求头，遵循 `Bearer Token`认证方案

```json
{
  "days": 3 //过时天数，即只保留3天之内的文件
}
```

响应内容：

> 上传成功响应码为 `200`

```json
{
  "message": "删除成功"
}
```

