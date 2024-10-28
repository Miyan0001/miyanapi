from flask import *
import requests
import google.generativeai as genai
import os
import subprocess
import json
import time
genai.configure(api_key='AIzaSyDb27FVEnAlJkbZVP15lapXAig3Gf7NMeI')
app = Flask(__name__)



@app.route('/')
def process_home():
    return render_template('index.html'), 200

# @app.route('/duck-ai', methods=['GET'])
# def process_duck_ai():
    # text = request.args.get('text')
    # if not text:
        # return jsonify({'error': 'Missing text parameter'}), 400
    # try:
        # url = 'https://duckduckgo.com/duckchat/v1/chat'
        # payload = json.dumps({
          # 'model': 'gpt-4o-mini',
          # 'messages': [
            # {
              # 'role': 'user',
              # 'content': text
            # }
          # ]
        # })
        
        # headers = {
          # 'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
          # 'Accept': 'text/event-stream',
          # 'Accept-Encoding': 'gzip, deflate, br, zstd',
          # 'Content-Type': 'application/json',
          # 'x-vqd-4': '4-74467779026257759346368850849287520444',
          # 'sec-ch-ua-platform': '\'Android\'',
          # 'sec-ch-ua': '\'Android WebView\';v=\'131\', \'Chromium\';v=\'131\', \'Not_A Brand\';v=\'24\'',
          # 'sec-ch-ua-mobile': '?1',
          # 'origin': 'https://duckduckgo.com',
          # 'sec-fetch-site': 'same-origin',
          # 'sec-fetch-mode': 'cors',
          # 'sec-fetch-dest': 'empty',
          # 'referer': 'https://duckduckgo.com/',
          # 'accept-language': 'en,en-US;q=0.9',
          # 'priority': 'u=1, i',
          # 'Cookie': 'dcm=3'
        # }    
        # def parse_stream_messages(response_text):
            # streams = response_text.strip().split('data: ')
            
            # combined_message = ''
            
            # for stream in streams:
                # if stream and stream != '[DONE]':
                    # try:
                        # data = json.loads(stream.strip())
                        
                        # if 'message' in data and data['message'] is not None:
                            # combined_message += data['message']
                            
                    # except json.JSONDecodeError:
                        # continue
                        
            # return combined_message.strip()
        
        # response = requests.post(url, data=payload, headers=headers)
        # result = parse_stream_messages(response.text)
        # return jsonify({'status':True, 'creator': '@Miyan', 'result': result}), 200
    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# @app.route('/gpt', methods=['GET'])
# def process_gpt():
    # text = request.args.get('text')
    # if not text:
        # return jsonify({'error': 'Missing text parameter'}), 400
    # try:
        # response = requests.get(f'https://api.vihangayt.com/ai/gpt?q={text}')
        # return jsonify({'status':True, 'creator': '@Miyan', 'result': response.json().get('data')}), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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

# @app.route('/gemini-media', methods=['GET'])
# def process_gemini_media():
    # file_url = request.args.get('file_url')
    # model = request.args.get('model')
    # text = request.args.get('text')
    # if not file_url:
        # return jsonify({'error': 'Missing file_url parameter'}), 400
    # if not model:
        # return jsonify({'error': 'Missing model parameter'}), 400
    # if not text:
        # return jsonify({'error': 'Missing text parameter'}), 400
    # if model == 'gemini-flash':
        # model = 'gemini-1.5-flash'
    # if model == 'gemini-pro':
        # model = 'gemini-1.5-pro'
    # response = requests.get(file_url)
    # filename = os.path.basename(file_url)
    # with open(filename, 'wb') as gm:
        # gm.write(response.content)
    # try:
        # myfile = genai.upload_file(filename)
        # model = genai.GenerativeModel(model)
        # response = model.generate_content([myfile,'\n\n',text])
        # return jsonify({'status':True, 'creator': '@Miyan', 'result': response.text, 'file_url': file_url}), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# @app.route('/removebg', methods=['GET'])
# def process_removebg():
    # file_url = request.args.get('file_url')
    # if not file_url:
        # return jsonify({'error': 'Missing file_url parameter'}), 400
    # response = requests.get(file_url)
    # filename = os.path.basename(file_url)
    # with open(filename, 'wb') as gm:
        # gm.write(response.content)
    # try:
        # subprocess.run(['rm', '-rf', f'removebg-{filename}'], check=True)
        # subprocess.run(['rembg', 'i', filename, f'removebg-{filename}'], check=True)
        # return send_file(f'removebg-{filename}',mimetype='image/png',download_name='Miyan.png'), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500



# @app.route('/tiktoksearch', methods=['GET'])
# def process_tiktoksearch():
    # keyword = request.args.get('keyword')
    # if not keyword:
        # return jsonify({'error': 'Missing keyword parameter'}), 400
    # try:
        # run_input = {
            # "keyword": keyword,
            # "limit": 10,
            # "sortType": None,
            # "region": "",
            # "publishTime": "ALL_TIME",
            # "proxyConfiguration": { "useApifyProxy": True },}
        
        # run = client.actor("jQfZ1h9FrcWcliKZX").call(run_input=run_input)
        # return jsonify({'status':True, 'creator': '@Miyan', 'data': run}), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# @app.route('/cloudflare', methods=['GET'])
# def process_bypass_cloudflare():
    # url = request.args.get('url') 
    # if not url:
        # return jsonify({'error': 'Missing keyword parameter'}), 400
    # try:
        # bypass_cloudflare = clodpler.get(url).text
        # return jsonify({'status':True, 'creator': '@Miyan', 'data': bypass_cloudflare}), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# @app.route('/image-enhancer', methods=['GET'])
# def process_image_enhancer():
    # image_url = request.args.get('url')
    
    # if not image_url:
        # return jsonify({'error': 'Missing url parameter'}), 400
    
    # try:
        # api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNTA1NjQxLCJpYXQiOjE3Mjk5Njk2NDEsImp0aSI6ImNYczlKWGRWIiwidXNlcl9pZCI6NDQ3Nn0.Y_3PcLruz1CFfxFKF5kzUqDMDB1P0jPChETk1SBMbrI'
        # request_data = {
            # 'inputs': {
                # 'image': image_url
            # }
        # }

        # response = requests.post(
            # 'https://youml.com/api/v1/recipes/5968/run?wait=600',
            # headers={
                # 'Content-Type': 'application/json',
                # 'creatorization': f'Bearer {api_token}'
            # },
            # json=request_data,
            # allow_redirects=True,
            # timeout=90)

        # result = response.json()
        # values = []
        
        # def find_values(data):
            # if isinstance(data, dict):
                # for key, value in data.items():
                    # if key == 'value' and isinstance(value, str):
                        # values.append(value)
                    # find_values(value)
            # elif isinstance(data, list):
                # for item in data:
                    # find_values(item)

        # find_values(result)
        # return jsonify({'status':True, 'creator': '@Miyan', 'url': values[1]}), 200

    # except requests.RequestException as e:
        # return jsonify({'error': f'API request failed: {str(e)}'}), 500
    # except (IndexError, KeyError) as e:
        # return jsonify({'error': f'Failed to process response: {str(e)}'}), 500
    # except Exception as e:
        # return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


# if __name__ == '__main__':
    # app.run(debug=True, host=0.0.0.0)