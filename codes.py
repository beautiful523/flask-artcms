# coding:utf8
import random
import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# 定义验证码功能
class Codes:
    # 随机一个数字或字母
    def random_chr(self):
        num = random.randint(1, 3)
        if num == 1:
            char = random.randint(48, 57)  # 数字
        elif num == 2:
            char = random.randint(97, 122)  # 小写字母
        else:
            char = random.randint(65, 90)  # 大写字母
        return chr(char)

    # 随机一个干扰字符
    def random_dis(self):
        arr = ["^", "-", "_", ".", "~"]
        return arr[random.randint(0, len(arr) - 1)]

    # 定义干扰字符的颜色
    def random_dis_color(self):
        return (random.randint(65, 255), random.randint(65, 255), random.randint(65, 255),)

    # 定义字符的颜色
    def random_chr_color(self):
        return (random.randint(65, 255), random.randint(65, 255), random.randint(65, 255),)

    def create_code(self):
        width = 240
        height = 60
        # 创建一个图片
        image = Image.new("RGB", (width, height), (192, 192, 192))
        # 创建font对象，定义字体和大小
        font_name = random.randint(1, 3)
        font_file = os.path.join(os.path.dirname(__file__), "static/fonts/") + "/%d.ttf" % font_name
        font = ImageFont.truetype(font_file, 30)
        # 创建draw对象填充干扰像素点
        draw = ImageDraw.Draw(image)
        for x in range(0, width, 5):
            for y in range(0, height, 5):
                draw.point((x, y), self.random_dis_color())
        # 填充干扰字符
        for v in range(0, width, 30):
            w = 5 + v
            # 距离图片上边5到15个像素
            h = random.randint(5, 15)
            dis = self.random_dis()
            draw.text((w, h), dis, self.random_dis_color(), font)
        # 填充字符，需要保存作验证用
        chars = ""
        for v in range(4):
            w = width / 4 * v + 10
            # 距离图片上边5到15个像素
            h = random.randint(5, 15)
            cc = self.random_chr()
            chars += cc
            draw.text((w, h), cc, self.random_chr_color(), font)
        # 模糊效果
        image.filter(ImageFilter.BLUR)
        image_name = "%s.jpg" % uuid.uuid4().hex
        save_dir = os.path.join(os.path.dirname(__file__), "static/code")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image.save(save_dir + "/" + image_name, "jpeg")
        return dict(
            img_name=image_name,
            code=chars
        )
        # image.show()


if __name__ == "__main__":
    c = Codes()
    print(c.create_code())
