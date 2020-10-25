# 千度网盘 开放API V3 开发指南
*通过该指南，您将快速了解并利用千度网盘开放技术*

## 环境
**示例环境以Python语言为主，理论上也可使用其他语言**
###### 你需要：
- Python3
- requests库
 
## 源码
**源码已上传并开源，请遵循许可证要求**  
 
## 服务
**服务器主域名：qianduserver.ngrok2.xiaomiqiu.cn**  
**支持协议：http**
**稳定性：全年91.7%**
**全国Ping平均延迟：33.75ms**
**海外Ping平均延迟：54ms**

## API
#### 登录验证
##### 请求：
**请求网址：qianduserver.ngrok2.xiaomiqiu.cn/requestpassword**

**请求方式：Post**

##### 请求数据：
 - user --用户名
 - password --用户密码
 - hash --哈希运算结果
 
 **hash计算规则：**  
 *hash运算使用sha256算法*  
 hash由以下部分组成  
 *此部分属于核心内容，为防止滥用端口，如需该部分内容请发邮件至qianduzhineng@163.com进行申请，我们会给予评估和结果*  
 
 ##### 返回数据
 **数据格式：JSON**  
 **返回数据组成：**  
 
 - code --返回的状态码
 - message --消息
 - hash（如有） --哈希值 
 - gethash(如有） --哈希值
 - right（如有） --校验是否正确
 - user(如有） --请求的用户名
  
  **状态码含义**
  

| Code  | 含义（该状态码是指已经成功向服务器提交请求返回200状态码之后的回复，非Http状态码） |
| ----- | --------------------------------------------------------------------------------- |
| 200   | 服务器完成了校验，账户名和密码存在且匹配（予以登录）                              |
| 400_0 | 没有传入账户名或密码                                                              |
| 400_1 | 没有传入hash值或hash长度错误                                                      |
| 403_0 | hash值错误                                                                        |
| 403_1 | 账户名或密码错误                                                                  |
| 403_9 | 传入的请求中出现代码注入等危险语句，拒绝执行                                      |
| 503   | 服务器维护，请耐心等待（该状态码仅表示该接口维护，其他接口如未返回503则可用）     |

##### 最佳实践

``` python
import requests
posthash="此处为哈希加密算法，需申请获得"
data = {"user":"获取的账户名",'password':"获取的密码",'hash':posthash}
qstatus_code=requests.get("http://qianduserver.ngrok2.xiaomiqiu.cn/requestpassword").status				   
if qstatus_code!=200:
      print("登录验证服务器异常")
else:
    res=requests.post(url='http://qianduserver.ngrok2.xiaomiqiu.cn/requestpassword',data=data).json()
```
