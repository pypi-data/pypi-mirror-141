#!/usr/bin/python -u
# coding: utf-8

"""
Copyright (C) 2017 Jacksgong(jacksgong.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
from os.path import exists

from ducat.confloader import ConfLoader
from ducat.helper import get_conf_path, print_unicode
from ducat.logprocessor import LogProcessor
from ducat.terminalcolor import colorize, allocate_color, termcolor, BLACK, RED, RESET

TIME_REGEX = r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'

class LogFileParser:
    filePaths = []
    valid = False
    processor = None
    hideSameTags = None
    keywords = None

    def __init__(self, file_paths, hide_same_tags, keywords):
        self.filePaths = file_paths
        self.hideSameTags = hide_same_tags
        self.keywords = keywords

    def setup(self, yml_file_name):
        for path in self.filePaths:
            if not exists(path):
                exit("log path: %s is not exist!" % path)
        self.processor = LogProcessor(self.hideSameTags)

        loader = ConfLoader()
        loader.load(get_conf_path(yml_file_name))

        self.processor.setup_trans(trans_msg_map=loader.get_trans_msg_map(),
                                   trans_tag_map=loader.get_trans_tag_map(),
                                   hide_msg_list=loader.get_hide_msg_list())
        self.processor.setup_separator(separator_rex_list=loader.get_separator_regex_list())
        highlight_list = loader.get_highlight_list()
        unique_hightlist = set()
        if highlight_list:
            unique_hightlist = unique_hightlist.union(set(highlight_list))
        if self.keywords:
            unique_hightlist = list(unique_hightlist.union(set(self.keywords)))
        print(unique_hightlist)
        self.processor.setup_highlight(list(unique_hightlist))
        self.processor.setup_condition(tag_keywords=loader.get_tag_keyword_map())
        self.processor.setup_regex_parser(regex_exp=loader.get_log_line_regex())

    def color_line(self, line, fileName):
        msg_key, line_buf, match_precondition = self.processor.process(line)
        if not match_precondition:
            return False

        if msg_key is not None:
            print('')
            print_unicode(u''.join(colorize(msg_key + ": ", fg=allocate_color(msg_key))).encode('utf-8').lstrip())

        if fileName:
            print_unicode(u''.join(fileName + ":" + line_buf).encode('utf-8').lstrip())
        else:
            print_unicode(u''.join(line_buf).encode('utf-8').lstrip())
        return True


    def process(self):
        for logPath in self.filePaths:
            stream = open(logPath, "r")
            indexOfLastBackSlant = logPath.rfind("/")
            if not indexOfLastBackSlant:
                indexOfLastBackSlant = 0
            else:
                indexOfLastBackSlant = indexOfLastBackSlant + 1
            fileName = logPath[indexOfLastBackSlant:]
            if len(self.filePaths) == 1:
                fileName = None
            newLine = stream.readline()
            hasMatchLine = False
            while newLine:
                newLineResult = self.color_line(newLine, fileName)
                hasMatchLine = newLineResult or hasMatchLine
                newLine = stream.readline()
            if hasMatchLine and len(self.filePaths) > 1:
                print_unicode(termcolor(fg=BLACK, bg=RED) + "===================文件" + logPath + "结束分割线======================" + RESET)
                                              