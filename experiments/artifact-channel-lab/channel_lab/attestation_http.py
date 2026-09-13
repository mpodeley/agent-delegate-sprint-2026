"""Small Artifactory-shaped local API; no external fetching or real service exploit."""
import json
from html import escape
from urllib.parse import quote

def route(handler, path, query, actor):
    store=handler.server.store
    if path in ('/', '/artifactory', '/artifactory/') and handler.command=='GET':
        return handler.send(200,{"repositories":["release-local","build-cache-local"],"storageApi":"/artifactory/api/storage/"})
    if path.startswith('/artifactory/api/storage/') and handler.command=='GET':
        key=path[len('/artifactory/api/storage/'):]
        return handler.send(200,{"path":key,"children":store.listing(actor,key)})
    if path.startswith('/artifactory/'):
        key=path[len('/artifactory/'):].rstrip('/')
        if not key or '..' in key.split('/') or '\\' in key: return handler.send(400,{"error":"invalid path"})
        if handler.command=='GET':
            row=store.read(actor,key)
            return handler.send(200,row['body'],'text/plain') if row else handler.send(404,{"error":"artifact not found"})
        if handler.command=='PROPFIND':
            items=store.listing(actor,key)
            body='<?xml version="1.0"?><d:multistatus xmlns:d="DAV:">'+''.join('<d:response><d:href>'+escape('/artifactory'+quote(i['uri'],safe='/'))+'</d:href></d:response>' for i in items)+'</d:multistatus>'
            return handler.send(207,body,'application/xml')
        if handler.command in ('PUT','MKCOL'):
            size=int(handler.headers.get('Content-Length','0'))
            if not 0<=size<=16384: return handler.send(413,{"error":"body too large"})
            body=handler.rfile.read(size).decode() if size else ''
            ok=store.write(actor,key,body,handler.command)
            return handler.send(201 if ok else 403,{"status":"created" if ok else "read only"})
    return handler.send(404,{"error":"unknown resource"})
