import os
import requests
from urllib.parse import urlparse

import random
API_URL1 = 'https://api2-16-h2.musical.ly/aweme/v1/play/'
API_URL2 = 'https://api2.musical.ly'


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
            url=API_URL2 + '/aweme/v1/aweme/detail/?aweme_id=' + str(valid_id) + '',
            allow_redirects=True
        )
        if "Video has been removed" in request_get_video_id.text:
            return False

        elif len(request_get_video_id.json()['aweme_detail']['video']['play_addr']['url_list']) == 0:
            return False

        else:
            self.nick_name = request_get_video_id.json()['aweme_detail']['author']['nickname']
            self.vid_id = request_get_video_id.json()['aweme_detail']['video']['play_addr']['uri']
            return True

    def download_no_watermark(self):

        if not os.path.exists("./downloads/" + self.nick_name):
            print("Creating directory: " + self.nick_name)
            os.makedirs("./downloads/" + self.nick_name)

        r = requests.get(API_URL1 + '?video_id={vid_id}&vr_type=0&is_play_url=1&source=PackSourceEnum_PUBLISH&media_type=4'.format(vid_id=self.vid_id))
        with open("./downloads/" + self.nick_name + "/" + self.vid_id + ".mp4", "wb") as f:
            f.write(r.content)

        if os.path.exists("./downloads/" + self.nick_name + "/" + self.vid_id + ".mp4"):
            return True

