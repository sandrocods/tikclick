import os
import requests
from urllib.parse import urlparse

import random

API_URL2 = 'https://api.tiktokv.com'


class tikdown:

    def __init__(self):
        self.nick_name = ""
        self.vid_id = ""
        self.url = ""

    def get_id_video(self, video_url):

        if 'tiktok' in video_url:
            if len(urlparse(video_url).path.split('/')[-1]) == 19:
                valid_id = urlparse(video_url).path.split('/')[-1]
            else:
                return False
        else:
            return False

        request_get_video_id = requests.get(
            url=API_URL2 + '/aweme/v1/multi/aweme/detail/?aweme_ids=%5B' + str(valid_id) + '%5D',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            },
            allow_redirects=True
        )
        if "Video has been removed" in request_get_video_id.text:
            return False

        elif len(request_get_video_id.json()['aweme_details'][0]['video']['play_addr']['url_list']) == 0:
            return False

        else:
            self.nick_name = request_get_video_id.json()['aweme_details'][0]['author']['nickname']
            self.vid_id = request_get_video_id.json()['aweme_details'][0]['video']['play_addr']['url_key']
            self.url = request_get_video_id.json()['aweme_details'][0]['video']['play_addr']['url_list'][
                random.randint(0,
                               len(
                                   request_get_video_id.json()[
                                       'aweme_details'][
                                       0][
                                       'video'][
                                       'play_addr'][
                                       'url_list']) - 1)]
            return True

    def download_no_watermark(self):

        if not os.path.exists("./downloads/" + self.nick_name):
            print("Creating directory: " + self.nick_name)
            os.makedirs("./downloads/" + self.nick_name)

        r = requests.get(self.url)
        with open("./downloads/" + self.nick_name + "/" + self.vid_id + ".mp4", "wb") as f:
            f.write(r.content)

        if os.path.exists("./downloads/" + self.nick_name + "/" + self.vid_id + ".mp4"):
            return True

