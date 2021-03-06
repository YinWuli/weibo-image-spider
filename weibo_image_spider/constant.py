# @FILENAME : constant
# @AUTHOR : lonsty
# @DATE : 2020/3/28 14:27
import json
import os
import re
from random import choice

from pydantic import BaseModel

from weibo_image_spider.models.dto import User, PhotoAPI, Status
from weibo_image_spider.utils import read_cookie, convert_to_safe_filename


class Constant(BaseModel):
    search_api = 'https://s.weibo.com/user?q={user}&Refer=SUer_box'
    img_hosts = ['https://wx1.sinaimg.cn', 'https://wx2.sinaimg.cn', 'https://wx3.sinaimg.cn']
    cookies_raw: str = ''
    user = User()
    photo_api = PhotoAPI()
    status = Status()
    nickname = 'lonsty'
    destination: str = 'weibo_images'
    overwrite: bool = False
    thumbnail: bool = False
    max_images: int = 2000
    max_workers: int = 15
    proxies_raw: str = None
    timeout = (5, 5)
    cancel: bool = False
    end_crawler = False

    def __init__(self, **kargs):
        super(Constant, self).__init__(**kargs)
        self.cookies_raw = read_cookie()

    @property
    def cookies(self):
        try:
            return dict([item.split('=')[0], item.split('=')[1]] for item in self.cookies_raw.split('; '))
        except Exception as e:
            return None

    @property
    def img_url_prefix(self):
        return f'{choice(self.img_hosts)}/{"large" if not self.thumbnail else "mw690"}/'

    @property
    def saved_dir(self):
        return os.path.join(os.path.abspath(self.destination), convert_to_safe_filename(self.user.name))

    @property
    def rex_pattern(self):
        return re.compile('(?<=/)\w*?\.(?:jpg|gif)', re.IGNORECASE)

    @property
    def user_photo_api(self):
        return self.photo_api.api

    @property
    def user_search_api(self):
        return self.search_api.format(user=self.nickname)

    @property
    def proxies(self):
        if isinstance(self.proxies_raw, str):
            try:
                return json.loads(self.proxies_raw)
            except Exception:
                print('Warning: proxy has not taken effect due to malformed')
                return None
        return None
