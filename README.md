# Hengda

这是一个 Python Web 项目，展示了恒达科技公司的主页。

## 功能

- 公司简介
- 新闻动态
- 产品中心
- 服务支持
- 科研基地
- 人才招聘

## 安装

### 前提条件

- Python 3.7
- Git
- Anaconda

### 克隆仓库

```sh
git clone https://github.com/kexinjiang111/hengda.git
```

### 环境创建
在conda中运行以下命令：
```sh
conda create -n pythonweb python=3.7  # 选择你需要的 Python 版本
conda activate pythonweb
```
在 conda 环境中运行以下命令：
```sh
pip install -r requiresments.txt
```
安装tesseract-ocr-w64-setup-v4.1.0.20190314.exe，将中文字符识别库中的两个文件放到\tessdata\目录下
在pytesseract安装包中找到pytesseract.py文件(\Anaconda3\envs\pythonweb\Lib\site-packages\pytesseract)目录下，修改其中代码
```py
tesseract_cmd=r'<tesseractOCR安装目录>\tesseract.exe'
```
### 运行项目
在 conda 环境中运行以下命令：

```py
python manage.py migrate
python manage.py runserver
访问 http://127.0.0.1:8000/ 查看项目。
```



