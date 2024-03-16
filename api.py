import json
import time

import requests

import asyncio

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        response = await asyncio.to_thread(requests.get, self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = await asyncio.to_thread(requests.post, self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        print(data)
        return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = await asyncio.to_thread(requests.get, self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            # print(data)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            # else:
                # print('[api] : generating image...')

            attempts -= 1
            await asyncio.sleep(delay)