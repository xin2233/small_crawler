import requests
import re
import time


# 2021.6.22
# 美女图片大全
# 下载图片

# 请求函数  附带头函数，避免被服务器给拦截了
def request_get(url, ret_type, timeout=5, encoding="GBK"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers, timeout=timeout)
    res.encoding = encoding
    if ret_type == "text":
        return res.text
    elif ret_type == "image":
        return res.content


# 抓取函数
def main():
    urls = [f"http://www.netbian.com/mei/index_{i}.htm" for i in range(2, 201)]
    url = "http://www.netbian.com/mei/index.htm"
    urls.insert(0, url)
    for url in urls:
        print("抓取列表页地址为：", url)
        text = request_get(url, "text")
        format_text(text)


# text    是网站代码
# s_html  '<div class="list">'
# e_html  '<div class="page">'
# 提取s 和e 之间的信息
def split_str(text, s_html, e_html):
    # start = text.find(s_html) + len(e_html)   应该是写错了！
    start = text.find(s_html) + len(s_html)

    # find() 方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束）
    # 范围，则检查是否包含在指定范围内，如果指定范围内如果包含指定索引值，返回的是索引值在字符串中的起始位置。如果不包含索引值，返回-1。

    end = text.find(e_html)
    origin_text = text[start:end]  # 取start到end 中间的所有数据

    return origin_text


# 解析函数   解析出下载地址
def format_text(text):
    origin_text = split_str(text, '<div class="list">', '<div class="page">')
    pattern = re.compile('href="(.*?)"')  # compile() 函数将一个字符串编译为字节代码。
    # 正则  re.findall 的简单用法（返回string中所有与pattern相匹配的全部字串，返回形式为数组）
    # 语法：findall(pattern, string, flags=0)
    hrefs = pattern.findall(origin_text)  # 从origin_text 中把所有和pattern相同的都返回到了hrefs中,以 数组 形式
    hrefs = [i for i in hrefs if i.find("desk") > 0]
    for i in hrefs:
        url = f"http://www.netbian.com{i}"
        print(f"正在下载：{url}")
        text = request_get(url, "text")
        format_detail(text)  #


# 找到 pattern的内容 在origin_text 中找到。
def format_detail(text):
    origin_text = split_str(text, '<div class="pic">', '<div class="pic-down">')
    pattern = re.compile('src="(.*?)"')
    # re.search    扫描整个字符串并返回第一个成功的匹配。
    # group(num=0) 匹配的整个表达式的字符串，
    # group()可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组
    # group（1）是元组中第一个数值
    # src -> Source资源
    image_src = pattern.search(origin_text).group(1)

    # 保存图片
    save_image(image_src)


# 存储函数
def save_image(image_src):
    content = request_get(image_src, "image")
    # Python time.time() 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。
    with open(f"./image/{str(time.time())}.jpg", "wb") as f:
        f.write(content)
        print("图片保存成功")


if __name__ == '__main__':
    main()
