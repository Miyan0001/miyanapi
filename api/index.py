from flask import *
from PIL import Image
import requests
import google.generativeai as genai
import os
import subprocess
import json
import time
import cloudscraper
from datetime import datetime
genai.configure(api_key='AIzaSyDb27FVEnAlJkbZVP15lapXAig3Gf7NMeI')
app = Flask(__name__)
scraper = cloudscraper.create_scraper()
import base64

# Use this function to convert an image file from the filesystem to base64
def image_file_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

# Use this function to fetch an image from a URL and convert it to base64
def image_url_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode('utf-8')

@app.route('/')
def process_home():
    return "Hello, World", 200

@app.route('/gpt', methods=['GET'])
def process_duck_ai():
    text = request.args.get('text')
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400
    try:
        url = 'https://duckduckgo.com/duckchat/v1/chat'
        payload = json.dumps({
          'model': 'gpt-4o-mini',
          'messages': [
            {
              'role': 'user',
              'content': text
            }
          ]
        })
        
        headers = {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
          'Accept': 'text/event-stream',
          'Accept-Encoding': 'gzip, deflate, br, zstd',
          'Content-Type': 'application/json',
          'x-vqd-4': '4-74467779026257759346368850849287520444',
          'sec-ch-ua-platform': '\'Android\'',
          'sec-ch-ua': '\'Android WebView\';v=\'131\', \'Chromium\';v=\'131\', \'Not_A Brand\';v=\'24\'',
          'sec-ch-ua-mobile': '?1',
          'origin': 'https://duckduckgo.com',
          'sec-fetch-site': 'same-origin',
          'sec-fetch-mode': 'cors',
          'sec-fetch-dest': 'empty',
          'referer': 'https://duckduckgo.com/',
          'accept-language': 'en,en-US;q=0.9',
          'priority': 'u=1, i',
          'Cookie': 'dcm=3'
        }    
        def parse_stream_messages(response_text):
            streams = response_text.strip().split('data: ')
            
            combined_message = ''
            
            for stream in streams:
                if stream and stream != '[DONE]':
                    try:
                        data = json.loads(stream.strip())
                        
                        if 'message' in data and data['message'] is not None:
                            combined_message += data['message']
                            
                    except json.JSONDecodeError:
                        continue
                        
            return combined_message.strip()
        
        response = requests.post(url, data=payload, headers=headers)
        result = parse_stream_messages(response.text)
        return jsonify({'status':True, 'creator': '@Miyan', 'result': result}), 200
    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (IndexError, KeyError) as e:
        return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/gemini', methods=['GET'])
def process_gemini():
    model = request.args.get('model')
    text = request.args.get('text')
    if not model:
        return jsonify({'error': 'Missing model parameter'}), 400
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400
    if model == 'gemini-flash':
        model = 'gemini-1.5-flash'
    if model == 'gemini-pro':
        model = 'gemini-1.5-pro'
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(text)
        return jsonify({'status':True, 'creator': '@Miyan', 'result': response.text}), 200

    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (IndexError, KeyError) as e:
        return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/gemini-media', methods=['GET'])
def process_gemini_media():
    file_url = request.args.get('file_url')
    model = request.args.get('model')
    text = request.args.get('text')
    if not file_url:
        return jsonify({'error': 'Missing file_url parameter'}), 400
    if not model:
        return jsonify({'error': 'Missing model parameter'}), 400
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400
    if model == 'gemini-flash':
        model = 'gemini-1.5-flash'
    if model == 'gemini-pro':
        model = 'gemini-1.5-pro'
    response = requests.get(file_url)
    filename = os.path.basename(file_url)
    with open(filename, 'wb') as gm:
        gm.write(response.content)
    try:
        myfile = genai.upload_file(filename)
        model = genai.GenerativeModel(model)
        response = model.generate_content([myfile,'\n\n',text])
        return jsonify({'status':True, 'creator': '@Miyan', 'result': response.text, 'file_url': file_url}), 200

    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (IndexError, KeyError) as e:
        return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/image-enhancer', methods=['GET'])
def process_image_enhancer():
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({'error': 'Missing url parameter'}), 400
    
    try:
        api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNTA1NjQxLCJpYXQiOjE3Mjk5Njk2NDEsImp0aSI6ImNYczlKWGRWIiwidXNlcl9pZCI6NDQ3Nn0.Y_3PcLruz1CFfxFKF5kzUqDMDB1P0jPChETk1SBMbrI'
        request_data = {
            'inputs': {
                'image': image_url
            }
        }

        response = requests.post(
            'https://youml.com/api/v1/recipes/5968/run?wait=600',
            headers={
                'Content-Type': 'application/json',
                'creatorization': f'Bearer {api_token}'
            },
            json=request_data,
            allow_redirects=True,
            timeout=90)

        result = response.json()
        values = []
        
        def find_values(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == 'value' and isinstance(value, str):
                        values.append(value)
                    find_values(value)
            elif isinstance(data, list):
                for item in data:
                    find_values(item)

        find_values(result)
        return jsonify({'status':True, 'creator': '@Miyan', 'url': values[1]}), 200

    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (IndexError, KeyError) as e:
        return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/esrgan', methods=['GET'])
def process_esrgan():
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({'error': 'Missing url parameter'}), 400
    
    try:
        api_key = "SG_23213d820f216a76"
        url = "https://api.segmind.com/v1/esrgan"

# Request payload
        data = {
          "image": image_url_to_base64(image_url),  # Or use image_file_to_base64("IMAGE_PATH")
          "scale": 4
        }

        headers = {'x-api-key': api_key}

        response = requests.post(url, json=data, headers=headers)
        with open('enhanced.jpg','wb') as f:
            f.write(response.content)
        return send_file('enhanced.jpg'), 200

    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except (IndexError, KeyError) as e:
        return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/cloudflare', methods=['GET'])
def cloudflare_route():
    url = request.args.get('url')
    if not url:
        return "Where's the url parameter?", 500
    bypass_cloudflare = scraper.get(url).text
    return bypass_cloudflare, 200
    

def format_number(integer):
    return "{:,}".format(int(integer)).replace(",", ".")

def format_date(timestamp, locale='en'):
    return datetime.fromtimestamp(timestamp).strftime('%A, %d %B %Y, %H:%M:%S')

@app.route('/tiktok', methods=['GET'])
def tiktok_dl():
    url = request.args.get('url')
    if not url:
        return "url parameter is missing", 500
    domain = 'https://www.tikwm.com/api/'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.tikwm.com',
        'Referer': 'https://www.tikwm.com/',
        'Sec-Ch-Ua': '"Not)A;Brand" ;v="24" , "Chromium" ;v="116"',
        'Sec-Ch-Ua-Mobile': '?1',
        'Sec-Ch-Ua-Platform': 'Android',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    params = {
        'url': url,
        'count': 12,
        'cursor': 0,
        'web': 1,
        'hd': 1
    }

    try:
        response = requests.post(domain, headers=headers, params=params).json()
        data = []

        if not response['data']['size']:
            for image in response['data']['images']:
                data.append({'type': 'photo', 'url': image})
        else:
            data.append({
                'type': 'watermark',
                'url': 'https://www.tikwm.com' + response['data']['wmplay']
            })
            data.append({
                'type': 'nowatermark',
                'url': 'https://www.tikwm.com' + response['data']['play']
            })
            data.append({
                'type': 'nowatermark_hd',
                'url': 'https://www.tikwm.com' + response['data']['hdplay']
            })

        result = {
            'status': True,
            'title': response['data']['title'],
            'taken_at': format_date(response['data']['create_time']).replace('1970', ''),
            'region': response['data']['region'],
            'id': response['data']['id'],
            'durations': response['data']['duration'],
            'duration': f"{response['data']['duration']} Seconds",
            'cover': 'https://www.tikwm.com' + response['data']['cover'],
            'size_wm': response['data']['wm_size'],
            'size_nowm': response['data']['size'],
            'size_nowm_hd': response['data']['hd_size'],
            'data': data,
            'music_info': {
                'id': response['data']['music_info']['id'],
                'title': response['data']['music_info']['title'],
                'author': response['data']['music_info']['author'],
                'album': response['data']['music_info']['album'] or None,
                'url': 'https://www.tikwm.com' + (response['data']['music'] or response['data']['music_info']['play'])
            },
            'stats': {
                'views': format_number(response['data']['play_count']),
                'likes': format_number(response['data']['digg_count']),
                'comment': format_number(response['data']['comment_count']),
                'share': format_number(response['data']['share_count']),
                'download': format_number(response['data']['download_count'])
            },
            'author': {
                'id': response['data']['author']['id'],
                'fullname': response['data']['author']['unique_id'],
                'nickname': response['data']['author']['nickname'],
                'avatar': 'https://www.tikwm.com' + response['data']['author']['avatar']
            }
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500