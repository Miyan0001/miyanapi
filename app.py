from flask import Flask,request,redirect,Response
import requests

app = Flask(__name__)
SITE_NAME = 'https://5000-miyan0001-miyan-4n62v1g8a3d.ws-us116.gitpod.io'

@app.route('/',methods=['GET'])
def proxy(path):
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}/')
    return resp.text