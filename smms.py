import requests
import json
import os

# api util for sm.ms cdn cache

class SMMS(object):
    # init
    def __init__(self, token):
        self.root = 'https://sm.ms/api/v2/'
        self.token = token
        self.profile = None
        self.history = None
        self.upload_history = None
        self.url = None
        self.headers = {'Authorization': self.token}

    # user
    def get_user_profile(self):
        url = self.root+'profile'
        res = requests.post(url, headers=self.headers).json()
        self.profile = res['data']
        print(json.dumps(res, indent=4))

    # image
    def clear_temporary_history(self):
        data = {
            'format': 'json'
        }
        url = self.root+'clear'
        res = requests.get(url, data=data).json()
        print(json.dumps(res, indent=4))

    # image
    def view_temporary_history(self):
        url = self.root+'history'
        res = requests.get(url).json()
        self.history = res['data']
        print(json.dumps(res, indent=4))

    # image
    def delete_image(self, hash):
        url = self.root+'delete/'+hash
        res = requests.get(url).json()
        print(json.dumps(res, indent=4))

    # image
    def view_upload_history(self):
        url = self.root+'upload_history'
        res = requests.get(url, headers=self.headers).json()
        self.upload_history = res['data']
        print(json.dumps(res, indent=4))

    # image
    def upload_image(self, path):
        try:
            files = {'smfile': open(path, 'rb')}
            url = self.root+'upload'
            res = requests.post(url, files=files, headers=self.headers).json()
            if res['success']:
                self.url = res['data']['url']
                # print(json.dumps(res, indent=4))
                return self.url
            else:
                print(res['message'])
                return None
        except Exception as e:
            print(e)
            return None

def convert(url, filename, smms):
    try:
        os.remove(filename)
    except:
        pass
    downloadImage(url, filename)
    cdn = smms.upload_image(filename)
    try:
        os.remove(filename)
    except:
        pass
    return cdn

def downloadImage(url, filename):
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

if __name__ == "__main__":
    smms = SMMS('')

    cdn = convert('https://img9.doubanio.com/view/subject/s/public/s29458844.jpg','./tmp/s29458844.jpg', smms)
    print(cdn)