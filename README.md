
# 下载代码

使用 `git` 命令将项目克隆到本地：

``` bash
git clone https://github.com/softtool/captcha-generator.git
```

---

# 创建环境

建议使用 `conda` 来创建独立的 Python 环境。运行以下命令来创建并激活环境：
进入到captcha-generator目录中
``` bash
conda create -p runtime python=3.10
conda activate ./runtime
```

---

# 安装依赖

在激活的环境中，安装项目所需的依赖包：

``` bash
pip install -r requirements.txt
```

---

# 生成图片

进入生成验证码图片的目录，并运行脚本：

``` bash
cd generate/character/ImageCaptcha
python gen_by_image_captcha.py
```
该脚本会基于配置生成对应的验证码图片。您可以根据需求调整脚本中的参数。

---
```

