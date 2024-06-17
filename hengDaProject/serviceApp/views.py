from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Doc
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
import os


# Create your views here.
def read_file(file_name, size):  #分批读取文件
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def download(request):
    submenu = 'download'
    docList = Doc.objects.all().order_by('-publishDate')
    p = Paginator(docList, 5)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        newList = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(
        request, 'docList.html', {
            'active_menu': 'service',
            'sub_menu': submenu,
            'docList': newList,
            'pageData': pageData,
        })


def getDoc(request, id):
    # 根据ID获取Doc对象，如果找不到则返回404错误
    doc = get_object_or_404(Doc, id=id)

    # 获取文件路径，分割字符串以获取文件目录和文件名
    update_to, filename = str(doc.file).split('/')
    filepath = '%s/media/%s/%s' % (os.getcwd(), update_to, filename)

    # 创建一个StreamingHttpResponse对象，逐块读取文件（每块512字节）
    response = StreamingHttpResponse(read_file(filepath, 512))

    # 设置响应的内容类型为二进制流
    response['Content-Type'] = 'application/octet-stream'

    # 设置响应头，使其作为附件下载，并指定下载文件名
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)

    return response


import numpy as np  # 矩阵运算
import urllib  # url解析
import json  # json字符串使用
import cv2  # opencv包
import os  # 执行操作系统命令
from django.views.decorators.csrf import csrf_exempt  # 跨站点验证
from django.http import JsonResponse  # json字符串响应


def platform(request):
    submenu = 'platform'
    return render(request, 'platForm.html', {
        'active_menu': 'service',
        'sub_menu': submenu,
    })
def ocr(request):
    submenu = 'ocr'
    return render(request, 'ocrtest.html', {
        'active_menu': 'service',
        'sub_menu': submenu,
    })
def read_image(stream=None):
    if stream is not None:
        data_temp = stream.read()
    img = np.asarray(bytearray(data_temp), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


face_detector_path = "serviceApp\\haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(face_detector_path)  # 生成人脸检测器
from PIL import Image
import io
import easyocr
import base64
import pytesseract
@csrf_exempt
def facedetectDemo(request):
    result = {}

    if request.method == "POST":
        if request.FILES.get('image') is not None:  #
            img = read_image(stream=request.FILES["image"])
            '''
            img: width*height*3
            '''
        else:
            result["#faceNum"] = -1
            result["error"] = "No image file uploaded"
            return JsonResponse(result)

        if img.shape[2] == 3:
            '''
            说明是彩色图像
            '''
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩色图像转灰度图像
        else:
            imgGray = img

        #进行人脸检测
        values = face_detector.detectMultiScale(imgGray,
                                           scaleFactor=1.1,
                                           minNeighbors=5,
                                           minSize=(30, 30),
                                           flags=cv2.CASCADE_SCALE_IMAGE)
        '''
        返回值
        values 是一个包含多个检测到的对象（人脸）的矩形列表。每个矩形由一个包含四个整数的元组 (x, y, w, h) 组成。
        x 和 y 是矩形的左上角坐标。
        w 和 h 是矩形的宽度和高度。
        示例解释
        假设 values 返回了 [(50, 50, 100, 100), (150, 150, 80, 80)]，那么这表示检测到两个人脸：
        
        第一个人脸的左上角在 (50, 50)，宽度和高度分别为 100 像素。
        第二个人脸的左上角在 (150, 150)，宽度和高度分别为 80 像素。
        
        '''

        #将检测得到的人脸检测关键点坐标封装
        values = [(int(a), int(b), int(a + c), int(b + d))
                  for (a, b, c, d) in values]

        # 将检测框显示在原图上
        for (w, x, y, z) in values:
            cv2.rectangle(img, (w, x), (y, z), (0, 255, 0), 2)

        retval, buffer_img = cv2.imencode('.jpg', img)  # 在内存中编码为jpg格式
        img64 = base64.b64encode(buffer_img)  # base64编码用于网络传输
        img64 = str(img64, encoding='utf-8')  # bytes转换为str类型
        print(img64)
        result["img64"] = img64  # json封装
        result["face"] = values  # json封装
    return JsonResponse(result)


@csrf_exempt
def ocrtestDemo(request):
    result = {"code": None}
    if request.method == "POST":
        if request.FILES.get("image", None) is not None:
            img = read_image(stream=request.FILES["image"])
        # OpenCV转PIL
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # 执行识别
        code = pytesseract.image_to_string(img, lang='chi_sim')
        print(code)
        result.update({"output": code})
    return JsonResponse(result)
# def ocrtestDemo(request):
#     if request.method == 'POST':
#         if 'image' in request.FILES:
#             image = request.FILES['image']
#             img = Image.open(image)
#             img_byte_array = io.BytesIO()
#             img.save(img_byte_array, format='PNG')
#             img_byte_array = img_byte_array.getvalue()
#
#             reader = easyocr.Reader(['ch_sim', 'en'])  # 支持简体中文和英文
#             result = reader.readtext(img_byte_array)
#
#             text = "\n".join([res[1] for res in result])
#             print(text)
#             return JsonResponse({'text': text})
#         else:
#             return JsonResponse({'error': 'No file uploaded'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

