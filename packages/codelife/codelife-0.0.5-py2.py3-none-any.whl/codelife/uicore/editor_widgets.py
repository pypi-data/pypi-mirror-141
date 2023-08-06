#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/14 10:02 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : editor_widgets.py
# @Project : codelife
from tkinter import Canvas, Text


class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._text_widget = None

    def attach(self, text_widget):
        self._text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self._text_widget.index("@0,0")
        while True:
            dline = self._text_widget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=line_num)
            i = self._text_widget.index("%s+1line" % i)


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._original = self._w + "_original"
        self.tk.call("rename", self._w, self._original)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._original,) + args
        #print("cmd:", cmd)
        try:
            result = self.tk.call(cmd)
            if (args[0] in ("insert", "replace", "delete") or
                    args[0:3] == ("mark", "set", "insert") or
                    args[0:2] == ("xview", "moveto") or
                    args[0:2] == ("xview", "scroll") or
                    args[0:2] == ("yview", "moveto") or
                    args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="tail")

            return result
        except Exception as e:
            print("ignore error")
