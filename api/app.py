from flask import Flask,request,redirect,Response
import requests

app = Flask(__name__)
SITE_NAME = 'https://crucial-renewing-sparrow.ngrok-free.app'

@app.route('/<path:path>',methods=['GET'])
def proxy(path):
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in     resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
    return response