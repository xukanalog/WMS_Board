import random
import datetime
import string
import json
from urllib import parse,request
import hashlib
import base64

class RMSSales_PlanList(object):
    def __init__(self):
        self.RMSSalesPlanList = []

class Algorithm_RMSSalesPlan(object):
    def __init__(self, ProductCode, OwnerCode, PlanQty, PlanTime, OperatorCode, StorageCode, CreateTime, ExtendFields, IsCompleted):
        self.ProductCode = ProductCode
        self.OwnerCode = OwnerCode
        self.PlanQty = PlanQty
        self.PlanTime = PlanTime
        self.OperatorCode = OperatorCode
        self.StorageCode = StorageCode
        self.CreateTime = CreateTime
        self.ExtendFields = ExtendFields
        self.IsCompleted = IsCompleted

def Seqle_Generate():                         #随机序列号（带字母）生成
    RandomLetter = [random.choice(string.ascii_letters) for i in range(2)]
    NowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
    RandomNum=random.randint(0,999) #生成的随机整数n
    if RandomNum < 100 and RandomNum >= 10:
        RandomNum = str(0) + str(RandomNum) + str(RandomLetter[0]) + str(RandomLetter[1])
        return str(NowTime)+str(RandomNum)
    if RandomNum < 10:                 #TypeError: '<' not supported between instances of 'str' and 'int'
        RandomNum = str(0) + str(0) + str(RandomNum) + str(RandomLetter[0]) + str(RandomLetter[1])
        return str(NowTime)+  str(RandomNum)
    SeqleGenerate = str(NowTime) + str(RandomNum) + str(RandomLetter[0]) + str(RandomLetter[1])
    return SeqleGenerate

def Seqno_Generate():                       #随机序列号（纯数字）生成
    NowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
    RandomNum=random.randint(0,999) #生成的随机整数n
    if RandomNum < 100 and RandomNum >= 10:
        RandomNum=str(0)+str(RandomNum)
        return str(NowTime) + str(RandomNum)
    if RandomNum < 10:
        RandomNum = str(0) + str(0) + str(RandomNum)
        return str(NowTime) + str(RandomNum)
    SeqnoGenerate = str(NowTime) + str(RandomNum)
    return SeqnoGenerate

def json_default(value):
    if isinstance(value, datetime.date):
        if (str(value).count('.') != 0):
            return str(value)[0:str(value).index('.')]
        else:
            return str(value)
    else:
        return value.__dict__


def Post_Transform(Data):  #Data为结构
    content = json.dumps(Data,default=json_default)
    keyvalue = 'ALOG_WCS_ALOG_WMS_SIGNKEY'
    keys = content + keyvalue
    hash_md5 = hashlib.md5(keys.encode("utf-8"))
    checkcode = hash_md5.hexdigest()
    checkcode_64 = base64.b64encode(bytes(checkcode, 'ascii'))
    url = 'http://10.42.10.205:3011/WMS/Algorithm.push'
    seq = str(Seqno_Generate())  # 不存在冲突
    #content = {"RMSSalesPlanList":[content]}
    text = {"sequenceno": seq, "service": "Algorithm_RMSSalesPlan", "partner": "ALOG-0001", "sign": checkcode_64,
                "content": content}
    textmode = parse.urlencode(text).encode(encoding='UTF8')
    #textmodeurl = '%s%s%s'%(url,'?',textmode)
    requrl = request.Request(url= url,data = textmode)
    res_data = request.urlopen(requrl)
    response = res_data.read()
    print(response.decode("utf-8"))

def Post_Wms(PredictResult,Time):
    count = 0
    for key,value in PredictResult.items():

        ProductCode = key
        OwnerCode = "725677994"
        PlanQty = int(int(value))
        PlanTime = Time
        OperatorCode = "code001"
        StorageCode = "ALOG-0003-03"
        CreateTime = datetime.datetime.now()
        ExtendFields = "alog001"
        IsCompleted = 1

        Line = str(ProductCode) + "\t" + str(PlanQty) +  "\t" + str(CreateTime)
        Fw = open('result.txt','a')
        Fw.write(str(Line) +  "\n")
        Fw.close()

        if count % 50 == 0:
            AlgorithmRMSSalesPlanList = RMSSales_PlanList()
        AlgorithmRMSSalesPlan = Algorithm_RMSSalesPlan(ProductCode, OwnerCode, PlanQty, PlanTime, OperatorCode,
                            StorageCode, CreateTime, ExtendFields, IsCompleted)
        AlgorithmRMSSalesPlanList.RMSSalesPlanList.append(AlgorithmRMSSalesPlan)
        count += 1
        if count % 50 == 0:
            Post_Transform(AlgorithmRMSSalesPlanList)
