from flask import Response
import json

def gen_res(msg=None):
    res = Response()
    res.headers.add('Access-Control-Allow-Origin', '*')
    if msg:
        res.data = json.dumps({'msg': msg})
    return res