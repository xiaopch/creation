#!/usr/bin/env python
# coding:utf-8
import openai #openai>=0.27.0
import os
from datetime import datetime
import json

##google asr语音设别
import speech_recognition as sr
##print(sr.__version__)
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

##设置代理
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

### 设置 api key

openai.api_key = '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'

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": "一个自由的技术创业者"}]
        self.filename="./user_messages.json"

    def ask_gpt(self):
        # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]

    def writeTojson(self):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    # 创建文件
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                messages = json.loads(content) if len(content) > 0 else {}
            # 追加
            messages.update({self.user : self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(messages, f)
        except Exception as e:
            print(f"错误代码：{e}")

            

def main():
    print('开始与chatgpt对话:')
    user = 'xiaopeng' #input("请输入用户名称: ")
    
    chat = ChatGPT(user)
    title = ''
    file_content = ''
    
    
    # 循环
    while 1:
        # 限制对话次数
        if len(chat.messages) > 110:
            print("******************************")
            print("*********强制重置对话**********")
            print("******************************")
##            # 写入之前信息
##            chat.writeTojson()
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)
            
        # 提问
        q = input(f"【按下Enter键开始对话】")
        
        # 重置对话
        if q == "x" or q == "X":
            print("*********退出程序**********")
            break
        elif q == "r" or q == "R":
            
            print("**************************")
            print("*********重置对话**********")
            print("**************************")
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)
            continue
        ##保存markdown文件
        elif q == "s" or q == "S":
            # 写入之前信息
            fn_with_time_str = datetime.now().strftime('%Y_%m_%d_%H%M._messages.json')#%Y_%m_%d_%H%M%S
            with open(fn_with_time_str, 'w',encoding='utf-8') as f:
             
                json.dump(chat.messages,f,ensure_ascii=False)
                
            print("**************************")
            print("*****保存markdown文件*****")
            print("**************************")
            time_str = datetime.now().strftime('%m.%d.%H_')#%Y_%m_%d_%H%M%S
            filename = time_str+title+'.md'
            print(filename)
            with open(filename,'w',encoding='utf-8') as fh:
                fh.write('## {}\n'.format(title))
##                fh.write('```\n')
                fh.write(file_content+'\n')
##                fh.write('```')
            chat = ChatGPT(user)
            continue
        ## 录音转文字
        elif len(q) < 2:
            print('录音中...')
            with mic as source:
                r.adjust_for_ambient_noise(source,duration=0.1)
                #参数: source, timeout = None,phrase_time_limit = None snowboy_configuration =None
                audio = r.listen(source,8,15)
            print('录音结束...')
            result = r.recognize_google(audio, language='zh-CN', show_all= True)
            q = result['alternative'][0]['transcript']
            print(q)
            c = input(f"【按下Enter确认，输入c取消】")
            if c == "c" or c == "C":
                continue
##            
            
            
        # GPT搜索
        if len(q)>1:          
            print('GPT开始思考...')
            # 提问-回答-记录
            chat.messages.append({"role": "user", "content": q})
            title = q
            answer = chat.ask_gpt()
            file_content = answer
            
            print(f"【ChatGPT】{answer}")
            chat.messages.append({"role": "assistant", "content": answer})
##            print(chat.messages)
        else:
            print('没有听到语音，请重新开始提问。')


if __name__ == '__main__':
    main()
