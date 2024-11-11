from flask import Flask, request, Response
import requests

app = Flask(__name__)
TARGET_URL = 'https://crucial-renewing-sparrow.ngrok-free.app'

def proxy_request(path):
    url = f"{TARGET_URL}/{path}"
    response = requests.get(url, params=request.args, headers={key: value for key, value in request.headers if key != 'Host'})
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return proxy_request(path)