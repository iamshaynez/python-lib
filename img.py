import requests
import json
import os
import util
from smms import SMMS


class ImageService(object):
    def __init__(self):
        props = util.Properties(util.CFG_FILE).getProperties()
        self.service = SMMS(props["smms"])

    def download(self, url, filename):
        with open(filename, 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def upload(self, url, filename):
        try:
            os.remove(filename)
        except:
            pass

        self.download(url, filename)
        link = self.service.upload_image(filename)
        try:
            os.remove(filename)
        except:
            pass
        return link

if __name__ == "__main__":
    service = ImageService()
    link = service.upload("https://pbs.twimg.com/media/FiFiMviUcAE8RsH?format=png&name=900x900","./tmp/1.png")
    print(link)


