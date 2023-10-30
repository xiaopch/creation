#!/usr/bin/env python
# coding:utf-8

from bs4 import BeautifulSoup

import requests,re
from datetime import datetime
import pandas as pd
import os
file_name = '0513 观念的跃升_ASR_2023_09_18_114850.md'
new_file_name = '观念的跃升_ASR_2023_09_18_114850.md'
with open(file=new_file_name,mode='w',encoding='utf-8') as fh:
    for line in open(file=file_name,mode='r',encoding='utf-8').readlines():
        print(line)
        fh.write(line+'\r')