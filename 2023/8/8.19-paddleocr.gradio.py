# # pip安装飞桨模型库依赖包
# pip install paddleocr
# pip install paddlenlp
# pip install paddlespeech

# # pip安装gradio模型库
# pip install gradio

import gradio as gr
import os

from paddleocr import PaddleOCR, draw_ocr

# #响应函数
def response(image):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr(image, cls=True)
    text = '\n'.join([i[1][0] for i in result[0]])
    # print(result[0])
    return text

# # 上传图片
image_src = gr.Image(label="原始图片")
output = gr.Code(label="OCR识别结果")
demo = gr.Interface(response, image_src, output)

demo.title = "在线图像转文字OCR"
demo.launch()

import webbrowser
webbrowser.open('http://127.0.0.1:7860')