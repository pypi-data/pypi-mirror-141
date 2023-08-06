from .DEVICE import DEVICE

_globalVar={} # 全局变量, 为避免过多及混乱, 全部储存在一个字典里
# 为保证安全, 在外部不可直接调用 globalVar, 必须通过函数调用
# 在外部调用 get 开头的函数时, 必须确保结果是只读的, 否则会对这里的可变对象的值产生影响
# 请直接使用 from globalVariable import getGlobalValue,setGlobalValue,getAllGlobalVariables,getGlobalVariableNum,clearGlobalVariable,deleteGlobalVariable,getAllKeys,isGlobalVariableExist

_globalVar['device']=DEVICE # 本地电脑为1, 服务器为0, 该值不可在函数中修改

# 币安两个不放在一起, 因为有单独用 API Key 的地方
_globalVar['bnAPIKey']='rxbhL8Bw3ICt6RZPrVxU2Xx8M5a8QblvAuTtZCbDJn6ARlwpXpUjX0780dwvM9P0'
_globalVar['bnSecKey']='vZcrHouv5HuIPrNuJ3tdElwuTkfkwYLK87t3vixaShVcR3co5cAhIb8m4J8Pnk8U'
_globalVar['hbAPI']=['vftwcr5tnh-306f4725-fedde7db-64ba9','a7fe3db2-48b8c48a-a7595d11-6b4bd']
_globalVar['okAPI']=['7ca2d00c-6b73-40cc-899a-a2e667a46c3c','5A0D927A5FC1CC4B39B96E143A84AB43','6b6eT8O07feV3Y6nV4mk5RCS975Q3nZ0']
_globalVar['okAPI2']=['bb7e3ef7-4ac6-4ae5-a82d-d51e2a7d4c2c','27B2AB7200D507C9B3E22F2E6BF453A8','6b6eT8O07feV3Y6nV4mk5RCS975Q3nZ0']
_globalVar['kkAPI']=['AjZy4kIOBWBG7VGz8vJzmUkJMPia3l7OnUrTydF9nZ0sBwCSTzVwqsOm','yAbGjW6M6AAnx/6fmPhyaFa4kizernTm2hrn8kO4yGBCqK3doIqANNMO/M84zdCqy+USJub3fSrjRMMIcRRzmg==']
_globalVar['kkAPI2']=['HieB9ylotOROpPc0NDMwBa4QF8cP11+UStBr3rgThMwJFLmEuLzeJkap','Z5OyXHADo5A0MpqxRWzOI5Uj46Zs5aqoJCeb+my2aNxF2IY6RcJST388B6f775YvwjrxCPeDfBoY/SWblaE7JMaQ']


# coinbase
# 1X4Mp8eywPxVJIRR
# aSH4WhYrVPklaI80DRzkXA65ZuLHzxRD


# bitfinex
# VB0EzWa1upYeyZrHNmDD0kAcY0LqQ3KWbkrB47uw44g
# 88d07OiNWA8Z6EhYGC0hMxj60molp5u15ltL0VOQ77x

# bittrex
# fc6b7f2267084c63964ba3f4e05ddbf5
# f46a73357e9549c8aae05d32eb8dfd41


def getGlobalValue(key):
    global _globalVar
    return _globalVar[key]


def setGlobalValue(key,v):
    global _globalVar
    _globalVar[key]=v


def getAllGlobalVariables():
    global _globalVar
    return _globalVar

def getGlobalVariableNum():
    global _globalVar
    return len(_globalVar)

def clearGlobalVariable():
    global _globalVar
    _globalVar={}

def deleteGlobalVariable(key):
    global _globalVar
    _globalVar.pop(key)


def getAllKeys():
    global _globalVar
    l=[]
    for k in _globalVar:
        l.append(k)
    return l

def isGlobalVariableExist(key):
    global _globalVar
    return key in _globalVar


def addGlobalVariable(key,num=1):
    global _globalVar
    try:
        _globalVar[key]=_globalVar[key]+num
    except:
        return -1
    return 0
