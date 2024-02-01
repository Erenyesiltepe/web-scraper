import requests
import json

cookies = {
    'BXID': 'AAAAAAVjmwzRPSkyJ56IiPcINbnNykU57unve+DpWIC2XOIJog==',
    'region': 'TURKIYE',
    'NSC_JOis2ck3bujiltkdwexni4cp4nzpdds': '14b5a3d96abc0d4515cfad42adc64fb98e1180325c55d3cf3c0e93138bbf62bc4ac3fcbd',
    'NSC_JO1afdbkecz2y1mct020ljedxilundm': '30dfa3db6fa389335402468bb6f364589a4c2971d77fad77a0afdbe44a5f235eb9e54986',
    'NSC_tmc_xxx.cjmfujy.dpn_KCptt_Qppm': '30dfa3db5138885a0a4780511bd8db8dc150ff1203fbee2c2b4810cec0e08c5f0aebe849',
    'main_campaign_TURKIYE': 'yes',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'tr',
    'CHANNEL': 'INTERNET',
    'CPU': '32100',
    'Connection': 'keep-alive',
    'Referer': 'https://www.biletix.com/performance/3OU01/013/TURKIYE/tr',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://www.biletix.com/wbtxapi/api/v1/bxcached/event/getPerformance/414151491/013/INTERNET/tr',
    cookies=cookies,
    headers=headers,
)

print(json.loads(response.text))