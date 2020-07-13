from helpers import paths
import json
from binanceWrapper.client import Client
from time import time
from datetime import datetime

from status import Status

"""
count = 0
with open('tripsListTable (18).csv', 'r') as f:
    for lineg in f:
        count += 1

print(count)


l = [None, None, None]
print(len(l))

l = [ 1, '[[]]', 3]
for i in range(0,len(l)):
    if i == 1:
        try: l[i] = ast.literal_eval(l[i])
        except: pass
print(l)


def printparams(a, *p):
    print(a)
    #for q in p: print(q)
    print(type(p))

printparams('1', 2, 3)


def foo(a, b='2', c='4', d='5'):
    print(a+b+c+d)

foo('1',d='hi')

"""

testDict = \
    {
        "idTypes": {
            "session": {
                "format": "[s]00aa",
                "inherits": [],
                "lastRecord": ""
            },
            "status": {
                "format": "001",
                "inherits": [
                    "session"
                ],
                "lastRecord": ""
            }
        }
    }

"""
from helpers.idHandler import ID

id1 = ID("session", reset=True)
id0 = ID("status", getNew=False, reset=True)
for i in range(0,1000):
    try:
        id = ID("status")
    except IndexError:
        id1 = ID("status", reset=True)
        id2 = ID("session")


l = [1,2,3]
try:
    for i in range(0,5):
        print(l[i])
except Exception as e:
    print('the exception is: ' + e.__repr__())

for i in range(2):
    sleep(1.5)
    print(time())


dict1 = {"one": 1, "moreNumbers": [2, 3], "aDict": {'a': 'A', 'b': 'B'}}

def fooargs(a, *args):
    print(a)
    for k in args:
        if k in dict1:
            print(dict1[k])
            globals()[k] = dict1[k]
    print(aDict)

fooargs('one', 'one', 'aDict')

#with open(paths.config/"hi.json", 'r') as f:
#    j = json.load(f)

n=3
if n==2: pass
else: print('n is not 2')

print(0<=n<=4)
print(0<=n<=2)

#with open(paths.projectPath/"tests.json", 'w+') as f:
#    json.dump({"a": True, "b": [3]}, f)

with open(paths.projectPath/"tests.json", 'r') as f:
    j = json.load(f)
print(type(j['a']))
for k in j: print(k)



import session

with open(paths.sessionConfig, 'r') as f:
    J = json.load(f)
marketsBuffer = J["sessionData"]["marketsBuffer"]
print(marketsBuffer)
session.marketsBufferFormatCheck(marketsBuffer)
print(marketsBuffer)
marketsBuffer = session.marketsBufferInactiveDeleting(marketsBuffer)
marketsBuffer = session.marketsBufferAmountsSplitting(marketsBuffer)


b = [{'a':1},{'b':True}]
for i in range(len(b)):
    b[i] = 1
print(b)



AK = "vdBlDHNvNdjDyGq2OVOpAasIaw9KCuX64Tkyd8UMPBAKZt9iy0CI4NJsSo0Cugpd"
AS = "OQUD762C24JvzHzFqeWozndcWz4ykfkbQ6ViP8SAenpIRWejWN0zaXOX0y8iU4bc"

client = Client(AK, AS)

print(client.get_trade_fee(symbol = "BNBBTC"))
print(client.get_trade_fee(symbol = "XRPBNB"))
print(client.get_account())
print(client.get_account_status())





d = {"a": 3, "b": 2}
print(d.get("a"))
print(type(d.get("c")))
a = {"a": 2}


f = {**d, **a}
print(f)

now = datetime.fromtimestamp(time()).isoformat()
print(now)
print(datetime.fromisoformat("2019-01-01T01:01:01.000000").timestamp())



marketData = {"tradedCurrency": {"symbol": "DOGE", "relativeTradableAmount": 1},"mainCurrency": {"symbol": "BNB","relativeTradableAmount": 1},"needsRestart": False,"isActive": True}

newStatus = Status("clientOne", marketData, run=True, allow_order_placing=False)
newStatus.get_open_orders(from_server=True)
newStatus.getSimplifiedStatus()
print(newStatus.getPrintableSimplifiedStatus())



class Ex:

    def __init__(self, d):
        self.a = 'a'
        self.d = d

    def self.get_b(bb) = self.GetB(bb)

    class GetB:

        def __init__(self, bb):

    def print_abc(self, cc):
        self.c = cc
        print(self.a + self.b + self.c)



l = [0,1,2]
for i in range(len(l)): l[i]=0
print(l)

d = [{'a': 1, 'b': 2}, {'c': 3}]
for m in d:
    m["isFirstOfTheSession"] = True
print(d)



number = 12313.12313123123
s = str("{:+e}".format(float(number)))
print(s)
print(s[:-5])


number = 12313.12313123123
n1 = number % .0003
print(number - n1)

n2 = float('+4.800000')
for i in range(int('03')):
    n2 /= 10
print(n2)
n2 = int(n2*100000000)
print(n2)
n2 /= 100000000
print(n2)


"""

n = 2995.8256548656
n = round(n,-1)
print(n)