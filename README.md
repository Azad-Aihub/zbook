# cow-zlib
依托于cow和Zlibrary-API的z-library插件。

目的是通过机器人去搜索电子书下载到本地，再通过微信发送。

触发口令是 `zlib [书名]`

![alt text](image.png)

## 书籍处理部分借用了 [Zlibrary——API]("https://github.com/bipinkrish/Zlibrary-API", "Zlibrary-API") 项目
感谢大佬的付出

## 配置说明
配置文件里有四个选项，都是用于登录z-library。

根据`Zlibrary-API`大佬的说明，配置文件建议使用 `remix_userid` 和 `remix_userkey`。

获取方式是登录网页版，然后从cookie里获取。

