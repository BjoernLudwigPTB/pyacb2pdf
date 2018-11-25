import requests


class Downloader():

    def __init__(self, url):
        self.__url = url

    def download(self, output_filename):
        r = requests.get(self.__url, allow_redirects=False)
        # Commented out, so I can manually insert my offer
        # open(output_filename, 'wb').write(r.content)
