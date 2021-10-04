import json
import time
import requests
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models

gaojinData="流量告警"
gaojinResult="流量结果"
gaojinSatus="告警状态"

SecretId = os.environ["SecretId"]
SecretKey = os.environ["SecretKey"]

regions = ["ap-hongkong"]
percent = 0.80  # 流量限额，1表示使用到100%关机，默认设置为95%

#key参数  
def doCheck():
    try:
        # 参数
        ids = SecretId.split(",")
        keys = SecretKey.split(",")
        # print(ids)

        for i in range(len(ids)):
            for ap in regions:
                dofetch(ids[i], keys[i], ap)

    except TencentCloudSDKException as err:
        print(err)


def dofetch(id, key, region):
    # 以下不用管
    global gaojinSatus
    global gaojinResult
    cred = credential.Credential(id, key)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
    #获取实例列表
    req_instances = models.DescribeInstancesRequest()
    params = {}
    req_instances.from_json_string(json.dumps(params))
    resp_instances = client.DescribeInstances(req_instances) 
    s1=json.loads(resp_instances.to_json_string())['InstanceSet']
    for j in range (len(s1)):
        params.setdefault("InstanceIds",[]).append(s1[j]['InstanceId'])#获取实例ID        
    
    #获取实例流量
    req = models.DescribeInstancesTrafficPackagesRequest()
    req.from_json_string(json.dumps(params))  
    resp = client.DescribeInstancesTrafficPackages(req)
    s2=json.loads(resp.to_json_string())["InstanceTrafficPackageSet"]
    GB=1024*1024*1024
    for i in range (len(s2)):
        InstanceId= s2[i]['InstanceId']
        s3= s2[i]['TrafficPackageSet'][0]
        InstanceState =s1[i]["InstanceState"]
        TrafficPackageTotal = round(s3['TrafficPackageTotal']/GB,2)
        TrafficUsed = round(s3['TrafficUsed']/GB,2)
        TrafficPackageRemaining=str(round(s3['TrafficPackageRemaining']/GB,2)) 
        unUseScore=(float(TrafficUsed)/float(TrafficPackageTotal))*100.0
        UesdScore=(float(TrafficPackageRemaining)/float(TrafficPackageTotal))*100.0
        shutdownScore=str((float(percent)/1.0)*100.0)
        #告警数据
        global gaojinData
        gaojinData="腾讯云轻量应用服务器流量告警："+"\n"+"\n"+"服务器："+"["+str(i+1)+"]"+" "+"腾讯轻量云"+"\n"+"\n"+"流量告警数据:\n"+"已使用："+str(TrafficUsed)+"GB"+"\n"+"总流量："+str(TrafficPackageTotal)+"GB"+"\n"+"剩余量："+str(TrafficPackageRemaining)+"GB"+"\n"+"使用比："+str(unUseScore)+"%"+"\n"+"未用比："+str(UesdScore)+"%"+"\n"+"关机比："+shutdownScore+"0000000000"+"%"
        print (gaojinData)
        #获取实例状态          
        #print (i+1,"：",InstanceId,":","已使用：",TrafficUsed,"总流量：",TrafficPackageTotal,"剩余：",TrafficPackageRemaining)
        if (InstanceState == "RUNNING"):
            gaojinSatus="流量告警状态：运行中!"
            print(gaojinSatus)
            #实例流量超出限制自动关闭
            if (TrafficUsed/TrafficPackageTotal<percent):
                #告警结果：
                gaojinResult="流量告警结果：剩余流量充足！"
                print (gaojinResult)
            else:
                gaojinResult="流量告警结果：流量超出限制，自动关闭！"
                print(gaojinResult)
                req_Stop = models.StopInstancesRequest()
                params_Stop = {

                }
                params_Stop.setdefault("InstanceIds",[]).append(InstanceId)
                req_Stop.from_json_string(json.dumps(params_Stop))
                resp_Stop = client.StopInstances(req_Stop) 
                print(resp_Stop.to_json_string())
        else:
            gaojinSatus="流量告警状态：已关机!"
            print(gaojinSatus)
        
        #添加时间戳
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "（该时间较北京时间晚8小时）")
        print ("---------------------------------------------")

#except TencentCloudSDKException as err: 
 #   print(err) 

if __name__ == '__main__':
     doCheck()
    # ck_kafka()
     pass
