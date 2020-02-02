import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from django_project import settings


class VerifyCode:
    """ 验证码生成器 """
    def __init__(self, request):
        self.request = request
        self.code_len = 4
        self.img_wight = 100
        self.img_height = 30
        self.session_key = 'verify_code'

    def gen_code(self):
        """ 合成验证码 """
        # 获取验证代码
        code = self._get_random_code()
        # 将验证码放入session中
        self.request.session[self.session_key] = code
        # 随机素材，文字颜色、背景颜色、字体
        font_color = ['black', 'darkblue', 'darkred', 'brown', 'green']
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        font_path = os.path.join(settings.BASE_DIR, 'static/fonts/timesbi.ttf')

        # 新建图片
        img = Image.new('RGB', (self.img_wight, self.img_height), bg_color)

        # 画干扰线
        draw = ImageDraw.Draw(img)
        for i in range(1, int(self.code_len / 2) + 1):
            line_color = random.choice(font_color)
            line_width = random.randrange(1, 3)
            point = (
                random.randrange(0, self.img_wight * 0.2),
                random.randrange(0, self.img_height),
                random.randrange(self.img_wight - self.img_wight * 0.2, self.img_wight),
                random.randrange(0, self.img_height)
            )
            draw.line(point, fill=line_color, width=line_width)

        # 绘画验证码
        for index, char in enumerate(code):
            font = ImageFont.truetype(font_path, size=random.randrange(20, 25))
            point = (
                index * self.img_wight / self.code_len,
                random.randrange(0, self.img_height/3)
            )
            color = random.choice(font_color)
            draw.text(xy=point, text=char, fill=color, font=font)

        # 将验证码图片保存到缓存中
        buf = BytesIO()
        img.save(buf, 'gif')
        return buf

    def _get_random_code(self):
        """ 生成随机码 """
        random_str = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        random_code = random.sample(random_str, self.code_len)
        return ''.join(random_code)

    def validate_code(self, code):
        """ 校验验证码是否正确 """
        vcode = self.request.session.get(self.session_key, '').lower()
        code = str(code).lower()
        return vcode == code
