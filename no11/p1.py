# download kugou music 
# by zjx
# date : 21/10/16

import requests,re

keyword = input("请输入想要听的歌曲：")
url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery1124006980366032059648_1518578518932&keyword="+keyword+"&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1518578518934"
content = requests.get(url)
filehash = re.findall('"FileHash":"(.*?)"',content.text)[0]
songname = re.findall('"SongName":"(.*?)"',content.text)[0].replace("<\\/em>","").replace("<em>","")

hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash="+filehash
hash_content = requests.get(hash_url)
play_url = re.findall('"play_url":"(.*?)"',hash_content.text)
play_url = ''.join(play_url)
real_download_url = play_url.replace("\\","")

print("客官，请稍等一下，好音乐马上呈上！")
with open(songname+".mp3","wb")as fp:
    fp.write(requests.get(real_download_url).content)