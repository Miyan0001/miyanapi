from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/pixiv', methods=['GET'])
def search_illusts():
    url = "https://www.pixiv.net/touch/ajax/search/illusts"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate",
        'x-user-id': "94263110",
        'x-requested-with': "mark.via.gp",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'accept-language': "en-US,en;q=0.9"
        'Cookie': '2024-04-03%2004%3A40%3A06; webp_available=1; cc1=2024-04-03%2004%3A40%3A06; __cf_bm=bFgcDe3ii0g4jGx2F3DaTDiqI45tTIjmVirfgKzgTA4-1712086806-1.0.1.1-PmaKCsuVW2_qPpzumrNho6ncdxvJbWvzelbYkqw0GT5cwcVnzPFr0qlfKc7hBR6M8RfL93yA8hcxjHuyGgOwCPtaXw.WiW7v1bE_EoD9qa8; p_ab_id=4; p_ab_id_2=4; p_ab_d_id=2029578662; __utma=235335808.2120078818.1712086808.1712086808.1712086808.1; __utmc=235335808; __utmz=235335808.1712086808.1.1.utmcsr=pixiv.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; yuid_b=hCloOQA; _lr_geo_location_state=JB; _lr_geo_location=ID; _fbp=fb.1.1712086811148.1166980283; privacy_policy_agreement=6; _gid=GA1.2.910677620.1712086814; _ga_MZ1NL4PHH0=GS1.1.1712086816.1.0.1712086819.0.0.0; PHPSESSID=94263110_Fw0KsX7pznqpdYz3lK8R9yh9XYu50q0o; device_token=716919cff64a5320628cdf79ef4516b7; c_type=21; privacy_policy_notification=0; a_type=0; b_type=0; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^6=user_id=94263110=1^9=p_ab_id=4=1^10=p_ab_id_2=4=1^11=lang=en=1^20=webp_available=yes=1; FCNEC=%5B%5B%22AKsRol-vCV9Hxuv0y5QgiXeC7T-BFYOrFVWJvquAW_a5dNJiomRpbw066zUVZyChY-7_loUKPrge1Xgfo4sIaFNaT5QLn_P22E2gS5ixUk2rUaobfhHC_pIaUYonV7bEpHq41Veo260DpW-4UuhCLkY4qTNun5Wopw%3D%3D%22%5D%5D; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; AMZN-Token=v2FweIBDV2dteXFXRmk0S2gzYlJ4WFFqZldkbTJrTkZ4WmVMTFNjMkV3RTRjNkdreWV1OGJscVpVQmhNcmVtVjlKamlISkIyK1QxcWV3a2gxM3lTZ0FWT3huQ21sWG0vTUlqRE9EbUg3bEErMmRJeWF5SXRySm16R2dYbVFpV1RPQ05vZGJrdgFiaXZ4HFNlKy92VWp2djcwMTc3KzlZeHQrNzcrOWRBQT3/; _pbjs_userid_consent_data=3524755945110770; _pubcid=4aecfda8-5100-45c7-9836-613f14880002; __gads=ID=a6eeb3b4c0a14363:T=1712086878:RT=1712086878:S=ALNI_MYl268T5t3l4KpQWHzo5sdDEn5fzQ; __eoi=ID=a5a1aef87f689702:T=1712086878:RT=1712086878:S=AA-AfjY3vOosEQzzth1nrPh5ZE5t; _im_vid=01HTG5941DFM57X0VR5XJ0HD20; cto_bundle=I5qpx19idyUyQnhKMHhYQnpLYjRqRWZQYXglMkZRYWNnY1V4WTdxOFpUTU5xd3c4c0p6M3FJRFYwZHVJSGIxNmFFc3ZoTWtmckNpTjJnb0lIUkRpajB1cWNMS3VocjNxWHdKZ3hKRWNuNzcyeGJKT3B2UkdKUHhLbGpCZGlycFF6UDhpWjBVOXlKRmpkODZZOSUyQmRSYTBuN2hXTk9QYkElM0QlM0Q; cto_bidid=hHBLll94dnBBd3pBRG0yJTJCT0dHNlJxMnB3SVUwMnY0UG1ESVRSeTdMQTVUT0xYQ29CaGdGdjFQdThVYVRqYnhrS3IzaWJzR2Vpb0FkWEowVzNxdlBUWXFydyUyQjlwbGhUaHlkUm5HaW9nOTNWJTJCUGc0ayUzRA; MgidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A1%7D%2C%22C1298385%22%3A%7B%22page%22%3A1%2C%22time%22%3A%221712086885038%22%7D%2C%22C1298391%22%3A%7B%22page%22%3A1%2C%22time%22%3A%221712086885023%22%7D%7D; __utmb=235335808.8.9.1712086837707; _ga_3WKBFJLFCP=GS1.1.1712086807.1.1.1712087230.0.0.0; _ga=GA1.1.2120078818.1712086808`
    }

    # Get 'word' parameter from query string
    pcknm = request.args.get('query', '')

    params = {
        'include_meta': "1",
        's_mode': "s_tag",
        'type': "all",
        'word': pcknm,
        'csw': "0",
        'lang': "en",
        'version': "08a9c37ead5e5b84906f6cbcdb92429ae5d13ac8"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        sifat = data['body']['illusts']
        return jsonify(sifat)  # Return JSON response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
