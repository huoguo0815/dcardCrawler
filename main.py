import urllib.request as request
import requests
import bs4


def getDcardTitleUrl(url):
    req = request.Request(url, headers={  # 模仿使用者去抓取dcard資料避免被拒絕存取
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        #user-agent的代碼會改 要去dcard重新複製
    })
    with request.urlopen(req) as response:  # 連上網站去讀取資料 存在data內
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")  # 透過bs4去解析網站原始碼
    titles = root.find_all("h2", class_="tgn9uw-2 bqeEAL")  # 要看網站的原始碼 找到標題的位置 要注意是h2的class 把每一個標題抓下來 class的標籤會改變 要定時去dcard自己抓

    for title in titles:
        if title.a != None:  # 避免抓到被刪除的貼文
            Link = "https://www.dcard.tw" + (title.a["href"])  # 找到該標題的網址
            print(Link)
            getDcadrContentandDownload(Link)  #進入該貼文去抓取資料



def getDcadrContentandDownload(url):
    req = request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    })
    with request.urlopen(req) as response:
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")
    Content = root.find("div", class_="phqjxq-0 iJJmxb")  # 看網站的原始碼 找到內文的位置 這個也會不定時更改 要去網站重新複製
    text = Content.text  # 把內文存下來
    with open("dcardseasick.txt", "a", encoding="utf-8") as file:  # 讀進檔案內 "a"為不複寫模式
        file.write(text + "\n" + "------------------我是分隔線------------------\n")
        print("下載完成")


def getPTTTitle(url):
    req = request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    })
    with request.urlopen(req) as response:
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")
    titles = root.find_all("div", class_="title")
    for title in titles:
        if title.a != None:
            Link = "https://www.ptt.cc/" + title.a["href"]
            getContent(Link)


def getContent(url):
    req = request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"

    })
    with request.urlopen(req) as response:
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")
    Content = root.find("div", id="main-container")
    # 把所有文字都抓出來
    all_text = Content.text
    # 把整個內容切割透過 "-- " 切割成2個陣列
    pre_text = all_text.split('--')[0]
    # 把每段文字 根據 '\n' 切開
    texts = pre_text.split('\n')
    # 如果你爬多篇你會發現
    contents = texts[2:]
    # 內容
    content = '\n'.join(contents)
    print(content)


def getDcardPicture(url):
    req = request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"

    })
    with request.urlopen(req) as response:
        data = response.read().decode('utf-8')
    test = open("dcardSexPicture.txt", 'a', encoding='UTF-8')
    root = bs4.BeautifulSoup(data, "html.parser")
    sel_jpg = root.select("div.Post_content_NKEl9 div div div img.GalleryImage_image_3lGzO")
    q = 0
    for c in sel_jpg:
        q += 1
        print("第", q, "張:", c["src"])
        test.write("%\n""第 {} 張: {} \n".format(q, c["src"]))
        pic = requests.get(c["src"])
        img2 = pic.content
        pic_out = open("dcardSexPicture.txt" + str(q) + ".png", 'wb')
        pic_out.write(img2)
        pic_out.close()


Dcardrelationship = "https://www.dcard.tw/f/relationship"
Dcardseasick = "https://www.dcard.tw/topics/%E6%9A%88%E8%88%B9"
DcardSex = "https://www.dcard.tw/f/sex"
PTTBY = "https://www.ptt.cc/bbs/Boy-Girl"
getDcardTitleUrl(Dcardseasick)

# today = datetime.date.today()


# getPTTTitle(PTTBY)

# def 先過濾出標題含有作品關鍵字(metas):
# return [meta for meta in metas if '#作品' in meta['title']]


# dcard = Dcard()

# metas = dcard.forums('photography').get_metas(num=100, callback=先過濾出標題含有作品關鍵字)
# posts = dcard.posts(metas).get(comments=False, links=False)

# resources = posts.parse_resources()

# status, fails = posts.download(resources)
# print('成功下載！' if len(fails) == 0 else '出了點錯下載不完全喔')
