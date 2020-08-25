from flask import Flask
import hashlib
import setcos#关于腾讯云对象存储的密钥等数据
from qcloud_cos import CosConfig, CosS3Client
from flask import render_template
from flask import request
import os
import time
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log=logging.basicConfig(filename='/var/log/QianDu/QianDuBack.log',level=logging.DEBUG, format=LOG_FORMAT)
file_bucket="file桶name"
sign_bucket="账户桶name"
config = CosConfig(Region=setcos.region, SecretId=setcos.secret_id, SecretKey=setcos.secret_key, Token=setcos.token, Scheme=setcos.scheme)
client = CosS3Client(config)

def check(inuser,inpassword,inhash):
    if inuser=='':
        return '{"code":"400_0","message":"Not User Or Password"}'
    if inpassword=='':
        return '{"code":"400_0","message":"Not User Or Password"}'
    if inhash=='':
        return '{"code":"400_1","message":"Hash Error"}'
    if len(list(inhash)) < 20:
        return '{"code":"400_1","message":"Hash Error"}'
    '''hash check'''
    if inhash[:10] != '加密算法需要申请后可获得':
        return '{"code":"403_0","message":"Hash Error"}'
    if inhash[10:20] != '加密算法需要申请后可获得':
        return '{"code":"403_0","message":"Hash Error"}'
    returnhash='加密算法需要申请后可获得'
    marker=''
    allac_uncheck=[]
    while True:
        response = client.list_objects(
            Bucket=sign_bucket,
            Marker=marker)
        allac_uncheck=allac_uncheck+response['Contents']
        if response['IsTruncated'] == 'false':
            break
        marker = response['NextMarker']

    for allac_uncheck_sign in allac_uncheck:
            each_list_uncheck=allac_uncheck_sign["Key"]
            if inuser+"/" == each_list_uncheck or inuser+"/password.txt" == each_list_uncheck:
                response = client.get_object(
                    Bucket=sign_bucket,
                    Key=inuser+"/password.txt")
                response['Body'].get_stream_to_file("./UserPassword.txt")
                with open("./UserPassword.txt","r") as f:
                    data_password = f.read()
                    if "\n" in data_password:
                        data_password.spilt("\n","")
                os.remove("./UserPassword.txt")
                if data_password==inpassword:
                    return '{"code":"200","message":"ok","user":"'+inuser+'","right":"True","hash":"'+'加密算法需要申请后可获得'+'","gethash":"'+returnhash+'"}'
                else:
                    return '{"code":"403_1","message":"User Or Password Error","gethash":"'+returnhash+'"}'
    return '{"code":"403_1","message":"User Or Password Error","gethash":"'+returnhash+'"}'
app = Flask(__name__)
@app.route('/')
def index():
    return '账户密码确认系统...运行中'

@app.route('/requestpassword', methods = ['GET', 'POST'])
def deal_request():
    if request.method == "GET":
        # get通过request.args.get("param_name","")形式获取参数值
        get_user = request.args.get("user","")
        get_password = request.args.get('password','')
        get_hash = request.args.get('hash','')
        #print(get_password,get_user,type(get_user))
        return check(inuser=get_user,inpassword=get_password,inhash=get_hash)
    else:
        return 'Must Use Get To Check!'

if __name__ == '__main__':
    app.logger.addHandler(log)
    #app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run(port=52012,host='127.0.0.1')
