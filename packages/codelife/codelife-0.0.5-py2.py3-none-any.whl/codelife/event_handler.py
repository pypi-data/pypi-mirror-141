#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 2:14 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : event_handler.py.py
# @Project : codelife
import os
from tkinter.filedialog import asksaveasfilename

from codelife import store


def handle_saving_event():
    # print("save code:")
    editing_stat = store.get_event_stat('editing')
    saving_stat = store.get_event_stat('saving')
    if saving_stat:
        content = saving_stat['args']
        if editing_stat:
            file_path = editing_stat['args']
            # print("file_path:", file_path)
            # print("content:", content)
            with open(file_path, 'w') as f:
                f.write(content)
        else:
            project_dir = store.get_current_project()
            project_dir = project_dir if project_dir else os.getcwd()
            opts = {
                'initialdir': project_dir,
                'initialfile': 'NewFile.txt',
                'defaultextension': '.txt'
            }
            path = asksaveasfilename(**opts)
            #print("path:", path)
            if path:
                with open(path, 'w') as f:
                    f.write(content)
    else:
        print("do nothing")
