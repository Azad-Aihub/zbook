import plugins
import requests
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from common.tmp_dir import TmpDir
from plugins import *

import os
import json

from .Zlibrary import Zlibrary


@plugins.register(
    name="ZlibCow",
    desc="A plugin that download ebooks from z-library by Zlibrary",
    version="0.1",
    author="leanfly",
    desire_priority=999,
)
class ZlibCow(Plugin):

    def __init__(self):
        super().__init__

        curdir = os.path.dirname(__file__)

        # 读取配置文件
        config_path = os.path.join(curdir, "config.json")
        conf = None

        if not os.path.exists(config_path):
            logger.debug(f"配置文件不存在{config_path}")
            return
        
        with open(config_path, "r", encoding="utf-8") as f:
            conf = json.load(f)
        
        # 指定z-library登录用户信息
        self.remix_userkey = conf["remix_userkey"]
        self.remix_userid = conf["remix_userid"]
        self.zlib_email = conf["zlib_email"]
        self.zlib_pass = conf["zlib_pass"]

        # 指定书籍保存目录
        self.books_dir = os.path.join(curdir, "books")

        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context

        logger.info("[ZlibCow] inited")


    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        
        content = e_context["context"].content.strip()

        if content.startswith("zlib"):
            book_name = content.split("zlib")[-1].strip()
            book_path = self.download_book(book_name)
            if not book_path:
                _send_text("没有找到相关书籍")
            
            _send_file(book_path, e_context)

            return

    def download_book(self, book_name):
        library = None
        
        if self.remix_userid != "":
            library = Zlibrary(remix_userid=self.remix_userid, remix_userkey=self.remix_userkey)

        if self.remix_userid == "" and self.zlib_email != "":
            library = Zlibrary(email=self.zlib_email, password=self.zlib_pass)

        book = library.search(book_name)

        if book == []:
            return

        filename, filecontent = library.downloadBook(book[0])

        book_path = os.path.join(self.books_dir, filename)
        with open(book_path, "wb") as bookfile:
            bookfile.write(filecontent)

        return book_path
    

def _send_file(file_path, e_context):
    reply = Reply()
    reply.type = ReplyType.FILE
    reply.content = file_path
    e_context["reply"] = reply
    e_context.action = EventAction.BREAK_PASS


def _send_full_type(e_context: EventContext, content: str, reply_type):
    reply = Reply(reply_type, content)
    channel = e_context["channel"]
    channel.send(reply, e_context["context"])


def _send_text(text:str, e_context):
    reply = Reply()
    reply.type = ReplyType.TEXT
    reply.content = text
    e_context["reply"] = reply
    e_context.action = EventAction.BREAK_PASS