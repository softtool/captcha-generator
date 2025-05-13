"""
验证码生成脚本

该脚本用于生成随机验证码图片，并将其保存到指定目录。
验证码支持以下类型：
- 纯数字（0-9）
- 英文字母（a-zA-Z）
- 常用汉字（可配置启用）

默认为4位长度，支持命令行参数控制数量。
生成的图片保存在项目根目录下的 images/character/ImageCaptcha 目录中。

使用方法：
1. 确保安装了 captcha 库 (pip install captcha)
2. 运行脚本，生成的验证码文本和图片将显示在控制台和指定目录中。

示例：
python gen_by_image_captcha.py --count 20      # 生成20个默认类型的验证码（数字+字母）
python gen_by_image_captcha.py --chinese      # 启用汉字验证码（需系统字体支持）

支持特性：
- 多字体混合渲染（微软雅黑、Arial 等）
- 字体大小随机变化
- 支持常用汉字过滤（避免生僻字）
"""


from captcha.image import ImageCaptcha
import string
import os
import argparse
import random
import re

ADD_HASH = True  # 控制是否添加随机hash值
COMMON_CHINESE_CHARS = (
    "的了在和是就也你他我啊哦额不这有那说看进来着去上中下左又它们时能可可以对错"
    "你好谢谢再见请问是谁什么为什么怎么这里那里今天明天昨天现在早上中午晚上春天夏天秋天冬天"
    "高兴快乐伤心难过喜欢爱讨厌害怕希望相信想吃喝玩学工作学校老师学生家长孩子朋友家人"
    "大小多少高矮胖瘦快慢冷热干净漂亮清楚明白容易困难认真仔细简单复杂安静热闹有趣无聊"
    # 更多常用字...
)

def generate_random_captcha(length=4, use_digits=True, use_letters=True, use_chinese=False):
    """
    生成随机验证码文本

    :param length: 验证码长度
    :param use_digits: 是否使用数字
    :param use_letters: 是否使用英文字母
    :param use_chinese: 是否使用汉字
    :return: 验证码字符串
    """
    characters = ""
    if use_digits:
        characters += string.digits  # 0-9
    if use_letters:
        characters += string.ascii_letters  # a-zA-Z
    if use_chinese:
        characters += COMMON_CHINESE_CHARS  # 使用常用字集合

    if not characters:
        raise ValueError("必须启用至少一种字符类型（数字、字母或汉字）")

    captcha_text = ''.join(random.choices(characters, k=length))
    return captcha_text
def get_system_font_path(font_name):
    """
    根据字体名称查找系统字体路径
    :param font_name: 字体名称，如 "微软雅黑", "Arial"
    :return: 字体文件路径 or None
    """
    if os.name == "nt":  # Windows
        fonts_dir = os.path.join(os.environ["WINDIR"], "Fonts")
        font_files = {
            "微软雅黑": "msyh.ttc",
            "SimHei": "simhei.ttf",
            "Arial": "arial.ttf",
            "Arial Rounded MT Bold": "ARLRDBD.TTF",
            "Georgia": "georgia.ttf",
            "Impact": "impact.ttf",
            "Comic Sans MS": "comic.ttf",
            "Times New Roman": "times.ttf",
            "Courier New": "cour.ttf"
        }
        font_file = font_files.get(font_name)
        if font_file:
            return os.path.join(fonts_dir, font_file)
    elif os.name == "posix":  # Linux/Mac
        # 可扩展为通过 font_manager 查找字体
        pass
    return None
def generate_captcha_image(captcha_text, use_chinese=False):
    # 基础字体列表
    base_font_names = [
        "Times New Roman",
        "Arial",
        "Georgia",
        "Comic Sans MS",
        "Courier New",
        "Arial Rounded MT Bold"
    ]

    # 如果是中文验证码，则只允许使用“微软雅黑”
    if use_chinese:
        available_font_names = ['微软雅黑']
    else:
        available_font_names = ['微软雅黑'] + base_font_names  # 默认保留中文字体支持（可选）

    # 动态查找字体路径
    available_fonts = []
    for name in available_font_names:
        path = get_system_font_path(name)
        if path and os.path.exists(path):
            available_fonts.append(path)

    if not available_fonts:
        raise RuntimeError("未找到任何可用字体，请检查系统字体或安装相关字体")

    # 设置字体大小范围，随机选择
    font_sizes = random.sample(range(35, 60), 3)  # 从35~60之间随机选3个不同大小

    # 创建 ImageCaptcha 实例
    image_captcha = ImageCaptcha(
        width=160,
        height=60,
        fonts=available_fonts,
        font_sizes=tuple(font_sizes)
    )

    captcha_image = image_captcha.generate_image(captcha_text)

    # 构建保存路径
    save_dir = os.path.abspath(os.path.join(__file__, '..','..', '..', '..', 'images', 'character', 'ImageCaptcha'))
    os.makedirs(save_dir, exist_ok=True)

    # 保存图片
    if ADD_HASH:
        import hashlib
        random_hash = hashlib.md5(captcha_text.encode()).hexdigest()[:8]
        filename = f"{captcha_text}_{random_hash}.png"
    else:
        filename = f"{captcha_text}.png"
    captcha_image.save(os.path.join(save_dir, filename))


def batch_generate_captchas(count=10, length=4, use_digits=True, use_letters=True, use_chinese=False):
    for _ in range(count):
        captcha_text = generate_random_captcha(length, use_digits, use_letters, use_chinese)
        generate_captcha_image(captcha_text, use_chinese=use_chinese)
        print(f"Captcha text: {captcha_text}")

def batch_generate_arithmetic_captchas(count=10):
    """
    批量生成数学运算并打印结果

    :param count: 要生成的数学运算数量
    """
    for _ in range(count):
        expression, result = generate_arithmetic_captcha()
        print(f"Expression: {expression}, Result: {result}")

def generate_arithmetic_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(['+', '-', '*'])
    op = random.choice(['+', '-'])

    if op == '+':
        result = num1 + num2
        expression = f"{num1} + {num2} =？"
    elif op == '-':
        # 确保不产生负数，并修正表达式
        a = max(num1, num2)
        b = min(num1, num2)
        result = a - b
        expression = f"{a} - {b} =？"
    else:
        result = num1 * num2
        expression = f"{num1} * {num2} =？"

    gentext = re.sub(r'[\\/*?:"<>|]', '_', expression)
    generate_captcha_image(gentext,use_chinese=True)
    return expression, str(result)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量生成验证码")
    parser.add_argument("--count", type=int, default=10, help="要生成的验证码数量，默认为10")
    parser.add_argument("--arithmetic", action="store_true", help="是否生成数学运算类验证码")

    args = parser.parse_args()

    # batch_generate_arithmetic_captchas(10)
    # if args.arithmetic:
    #     batch_generate_arithmetic_captchas(args.count)
    # else:
    #     batch_generate_captchas(args.count, use_digits=True, use_letters=True, use_chinese=False)
    batch_generate_captchas(2, use_digits=True, use_letters=True, use_chinese=False)