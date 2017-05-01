# coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import json
from multiprocessing.dummy import Pool as tp
import subprocess
import os
import base64
from ebooklib import epub


# 是否抓取内链内容
getinline = False
# 连接线程数
threads = 32
# 增加原作者信息
orginfo = True
# 创建epub
makeepub = True
# 创建总txt
maketxt = True
# 创建单话txt
singletxt = True
# 汉字数字化排序
hznum = True
# 忽略过短贴子
passtoshort = False
# 有效回复的最短长度
validreply = 200
# 除非理解含义否则不要改动！
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2922.1 Safari/537.36'}
htmlparser = 'lxml'
p = None
# p = {"http": "http://127.0.0.1:8787", "https": "https://127.0.0.1:8787"}
pool = tp(processes=threads)
dirname = os.getcwd()
warn = '本文件为自动抓取程序生成的文件'
about = b'PGh0bWw+PGhlYWQ+PC9oZWFkPjxib2R5PjxoMz7mnKzkuabkv6Hmga88L2gzPjxwPuacrOS5pueUseiEmuacrOiHquWKqOS7jueZvuW6pui0tOWQp+aKk+WPluW5tueUn+aIkOOAgjwvcD4KPHA+5Y+v6IO95Ye6546w5ZCE56eN5o6S54mI6Zeu6aKY6K+36Ieq6KGM5paf6YWM5L2/55So44CCPC9wPgo8cD7or7flsIrph43ljp/kvZzogIXlj4rnv7vor5HogIXnmoTlirPliqjmiJDmnpzvvIE8L3A+PC9ib2R5PjwvaHRtbD4='
tabout = b'5pys5Lmm5L+h5oGvCuacrOS5pueUseiEmuacrOiHquWKqOS7jueZvuW6pui0tOWQp+aKk+WPluW5tueUn+aIkOOAggrlj6/og73lh7rnjrDlkITnp43mjpLniYjpl67popjor7foh6rooYzmlp/phYzkvb/nlKjjgIIK6K+35bCK6YeN5Y6f5L2c6ICF5Y+K57+76K+R6ICF55qE5Yqz5Yqo5oiQ5p6c77yB'
style = b'CkBuYW1lc3BhY2UgZXB1YiAiaHR0cDovL3d3dy5pZHBmLm9yZy8yMDA3L29wcyI7CmJvZHkgewogICAgZm9udC1mYW1pbHk6IENhbWJyaWEsIExpYmVyYXRpb24gU2VyaWYsIEJpdHN0cmVhbSBWZXJhIFNlcmlmLCBHZW9yZ2lhLCBUaW1lcywgVGltZXMgTmV3IFJvbWFuLCBzZXJpZjsKfQpoMiB7CiAgICAgdGV4dC1hbGlnbjogbGVmdDsKICAgICB0ZXh0LXRyYW5zZm9ybTogdXBwZXJjYXNlOwogICAgIGZvbnQtd2VpZ2h0OiAyMDA7ICAgICAKfQpvbCB7CiAgICAgICAgbGlzdC1zdHlsZS10eXBlOiBub25lOwp9Cm9sID4gbGk6Zmlyc3QtY2hpbGQgewogICAgICAgIG1hcmdpbi10b3A6IDAuM2VtOwp9Cm5hdltlcHVifHR5cGV+PSd0b2MnXSA+IG9sID4gbGkgPiBvbCAgewogICAgbGlzdC1zdHlsZS10eXBlOnNxdWFyZTsKfQpuYXZbZXB1Ynx0eXBlfj0ndG9jJ10gPiBvbCA+IGxpID4gb2wgPiBsaSB7CiAgICAgICAgbWFyZ2luLXRvcDogMC4zZW07Cn0K'
hznuml = [('九千', '9'), ('八千', '8'), ('七千', '7'), ('六千', '6'), ('五千', '5'), ('四千', '4'), ('三千', '3'), ('两千', '2'), ('二千', '2'), ('一千', '1'), ('千', '1'), ('九百', '9'), ('八百', '8'), ('七百', '7'), ('六百', '6'), ('五百', '5'), ('四百', '4'), ('三百', '3'), ('二百', '2'), ('一百', '1'), ('百', '1'), ('九十', '9'), ('八十', '8'), ('七十', '7'), ('六十', '6'), ('五十', '5'), ('四十', '4'), ('三十', '3'), ('二十', '2'), ('一十', '1'), ('十', '1'), ('九', '9'), ('八', '8'), ('七', '7'), ('六', '6'), ('五', '5'), ('四', '4'), ('三', '3'), ('二', '2'), ('一', '1'), ('零', '0'), ('〇', '0')]


def getpage(link):
    i = 0
    while i < 3:
        try:
            gethtml = requests.get(link, headers=headers, proxies=p)
            if gethtml.status_code == 200:
                break
            else:
                i += 1
        except:
            i += 1
    Soup = BeautifulSoup(gethtml.content, 'lxml')
    return Soup


def getlink(string):
    link = re.findall('(http\:\/\/tieba\.baidu\.com\/p\/)([0-9]{10})', string)
    if link == []:
        link = re.findall('(https\:\/\/tieba\.baidu\.com\/p\/)([0-9]{10})', string)
    if link == []:
        raise ValueError('No Valid Link')
    link = ''.join(link[0]).replace('https', 'http')
    return link


def goodtitle(title):
    return title.replace(' ', '').replace('：', '').replace(':', '').replace('|', '_').replace('"', '_').replace('/', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(';', '')


def FullToHalf(s):
    n = []
    for char in s:
        num = ord(char)
        if 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)


class Title:
    def __init__(self, word=''):
        self.word = FullToHalf(word)
        num = re.findall('(\d{1,10})(\.\d)?(?!\d)', self.word)
        self.num = [float(''.join(i)) for i in num]
        self.hznum = []
        if hznum is True:
            self.ghznum()
        if bool(re.search('s\d{1,3}', self.word, re.IGNORECASE)):
            self.sp = True
        elif ('闲话' or '閒話' or '番外' or '后日谈' or '後日談' or '间章' or '間章') in self.word:
            self.sp = True
        else:
            self.sp = False

    def ghznum(self):
        hznums = re.findall('^[零一二三四五六七八九十百千〇]{1,20}|[零一二三四五六七八九十百千〇]{1,20}(?=[话話章])', self.word)
        chznum = []
        if hznums == []:
            if '序章' not in self.word:
                return
            else:
                self.hznum = ['零']
                self.chznum = [0]
        else:
            for i in hznums:
                if i == '千':
                    i = i.replace('千', '1000')
                if i[-1] == '千':
                    i = i.replace('千', '000')
                if i == '百':
                    i = i.replace('百', '100')
                if i[-1] == '百':
                    i = i.replace('百', '00')
                if i == '十':
                    i = i.replace('十', '10')
                if i[-1] == '十':
                    i = i.replace('十', '0')
                for j in hznuml:
                    i = i.replace(j[0], j[1])
                chznum.append(int(i))
            self.hznum = hznums
            self.chznum = chznum

    def __bool__(self):
        if ('文庫版' or '文库版' or '插图' or '插圖' or '佔坑' or '占坑') in self.word:
            return False
        elif bool(re.search('txt', self.word, re.IGNORECASE)) or bool(re.search('epub', self.word, re.IGNORECASE)):
            return False
        elif self.num == [] and self.hznum == []:
            return False
        else:
            return True

    def __repr__(self):
        return self.word

    def __str__(self):
        return self.word

    def __add__(self, other):
        return self.word + other

    def sortint(self, key=None):
        if self.hznum == []:
            numlist = self.num
        else:
            numlist = self.chznum
        if key is None:
            if len(numlist) == 1:
                return numlist[0]
            else:
                numlist = [numlist[0]] + [int(i) for i in numlist[1:]]
                if numlist[0] == int(numlist[0]):
                    strnum = str(int(numlist[0])).zfill(4) + '.' + ''.join([str(i).zfill(4) for i in numlist[1:]])
                else:
                    strnum = str(numlist[0]).zfill(4) + ''.join([str(int(i)).zfill(4) for i in numlist[1:]])
                return float(strnum)
        elif len(key) == 1:
            return numlist[key[0]]
        else:
            return int(''.join([str(numlist[i]).zfill(5) for i in key]))


class TiebaReply:
    def __init__(self, contain):
        self.tid = str(contain['content']['thread_id'])
        self.pid = str(contain['content']['post_id'])
        self.replynum = contain['content']['comment_num']
        self.pagenum = int(self.replynum) // 10 + 1
        contain = []
        for i in range(1, self.pagenum + 1):
            link = 'http://tieba.baidu.com/p/comment?tid=' + self.tid + '&pid=' + self.pid + '&pn=' + str(i)
            contain.append(getpage(link).find_all('span', class_='lzl_content_main'))
        self.word = [k for i in contain for j in i for k in j.get_text('\n', strip=True).split('\n')]


class TiebaPage:
    def __init__(self, link=''):
        self.link = getlink(link)
        self.pid = self.link[25:35]
        self.page = [getpage(link)]
        try:
            self.tieba = goodtitle(self.page[0].find('title').get_text().split('_')[-2].replace('吧', ''))
            self.title = self.page[0].find('h3').get_text()
            self.pagenum = int(self.page[0].find('span', class_='red', style=None).get_text())
            if self.pagenum > 1:
                for i in range(2, self.pagenum + 1):
                    self.page.append(getpage(link + '?pn=' + str(i)))
            self.posts = []
            for p in self.page:
                try:
                    p_postlist = p.find('div', class_="p_postlist", id="j_p_postlist")
                    postlist = list(p_postlist.find_all('div', class_='l_post l_post_bright j_l_post clearfix '))
                    self.posts = self.posts + postlist
                except AttributeError:
                    pass
            self.contain = [json.loads(i['data-field']) for i in self.posts]
            self.owner = self.contain[0]['author']['user_name']
            self.statues = True
            print('页面 {0} 抓取成功。标题为: {1}'.format(self.link, self.title))
        except:
            self.statues = False
            print('页面 {0} 抓取失败。'.format(self.link))

    def __bool__(self):
        return self.statues


class ZHPage(TiebaPage):
    def getlink(self):
        print('  正在抓取回复...')
        reply = pool.map(TiebaReply, self.contain)
        data1 = [i['content']['content'].replace('https', 'http') for i in self.contain]
        data2 = [i.word for i in reply]
        self.data = [(data1[i], data2[i]) for i in range(len(data1))]
        count = 1
        self.linklist = []
        for i in self.data:
            main = list(BeautifulSoup(i[0], htmlparser).stripped_strings)
            for j in range(len(main) - 1):
                if 'http://tieba.baidu.com/p/' not in main[j] and 'http://tieba.baidu.com/p/' in main[j + 1] and bool(Title(main[j])):
                    try:
                        self.linklist.append((Title(main[j]), getlink(main[j + 1]), int(count)))
                    except ValueError:
                        link = getlink(main[j + 1] + main[j + 2])
                        self.linklist.append((Title(main[j]), link, int(count)))
                    count += 1
            if not len(i[1]) == 0:
                for j in range(len(i[1]) - 1):
                    if 'http://tieba.baidu.com/p/' not in i[1][j] and 'http://tieba.baidu.com/p/' in i[1][j + 1] and bool(Title(i[1][j])):
                        try:
                            self.linklist.append((Title(i[1][j]), getlink(i[1][j + 1]), int(count)))
                        except ValueError:
                            link = getlink(i[1][j + 1] + i[1][j + 2])
                            self.linklist.append((Title(i[1][j]), link, int(count)))
                        count += 1
        return self


class FilePage:
    def __init__(self, tieba, linklist):
        self.tieba = tieba
        self.linklist = linklist


class WordPage(TiebaPage):
    def getword(self):
        self.usefulreply = []
        for i in self.contain:
            try:
                reply = BeautifulSoup(i['content']['content'], htmlparser).get_text('\r\n', strip=True)
                owner = i['author']['user_name']
                if owner == self.owner or len(reply) > validreply:
                    self.usefulreply.append(reply)
            except TypeError:
                pass
        self.word = '\r\n\r\n'.join(self.usefulreply)
        return self.word

    def inline(self):
        self.inlinklist = getlink(self.word)
        for i in self.inlinklist:
            l = WordPage(i).getword()
            self.word = self.word.replace(i, i + '\r\n--------深度抓取内容--------\r\n' + l + '\r\n--------深度抓取内容--------\r\n')

    def stitle(self, title):
        self.otitle = goodtitle(title.word)

    def outputword(self):
        self.getword()
        if getinline is True:
            self.inline()
        self.info = '\r\n作者：' + self.owner + '  原帖地址：' + self.link + '\r\n' + warn + '\r\n\r\n\r\n'
        self.output = self.title + self.info + self.word
        return self.output

    def outputepub(self):
        htmllist = ['<html>\n<head>\n']
        self.info = '\r\n作者：' + self.owner + '  原帖地址：' + self.link + '\r\n' + warn + '\r\n\r\n\r\n'
        self.outputline = self.info.split('\r') + self.word.split('\r')
        htmllist.append('<title>' + self.title + '</title>\n</head>\n<body>\n<div>\n<h3>' + self.title + '</h3>\n')
        for l in self.outputline:
            htmllist.append('<p>' + l + '</p>\n')
        htmllist.append('</div>\n</body>\n</html>')
        self.html = ''.join(htmllist)
        return self.html

    def writetxt(self):
        open(dirname + '\\' + self.tieba + '\\' + self.otitle + '.txt', mode='wb').write(self.output.encode())


def createbook(result):
    (tieba, contentlist) = result
    print('制作Epub选项已开启，正在制作epub。')
    book = epub.EpubBook()
    book.set_identifier(b'id' + base64.b64encode(bytes(tieba, 'utf-8')))
    book.set_title(tieba)
    book.set_language('zh')
    book.add_author("TYTY's Python Tieba Spider Epub Maker")
    sabout = base64.b64decode(about).decode('utf-8')
    cabout = epub.EpubHtml(title='本书信息', file_name='0.xhtml', content=sabout, lang='zh_cn')
    book.add_item(cabout)
    conlist = [epub.EpubHtml(title=i.otitle, file_name=i.otitle + '.xhtml', content=i.outputepub(), lang='zh_cn') for i in contentlist]
    for i in conlist:
        book.add_item(i)
    contuple = conlist
    contuple.insert(0, 'cabout')
    contuple = tuple(contuple)
    book.toc = (epub.Link('0.xhtml', '本书信息', 'intro'), (epub.Section('包含篇章：'), contuple))
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    dstyle = str(base64.b64decode(style))
    css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=dstyle)
    book.add_item(css)
    book.spine = ['nav'] + conlist
    epub.write_epub(dirname + '\\' + tieba + '\\' + tieba + '.epub', book, {})
    print('Epub制作成功。')


def makeatxt(result):
    (tieba, contentlist) = result
    print('制作合集TXT选项已开启，正在制作txt。')
    con = []
    con.append(base64.b64decode(tabout).decode('utf-8') + '\r\n\r\n\r\n\r\n\r\n\r\n')
    for i in contentlist:
        con.append(i.outputword() + '\r\n\r\n\r\n')
    fi = ''.join(con)
    g = open(dirname + '\\' + tieba + '\\' + tieba + '.txt', 'wb')
    g.write(fi.encode('utf-8'))
    print('合集TXT制作成功。')


def readtask(file='linklist.txt'):
    try:
        linelist = list(open(file, 'r').readlines())
    except UnicodeDecodeError:
        linelist = open(file, 'rb').read().decode('utf-8').split('\r\n')
    linklist = []
    count = 1
    for i in range(1, len(linelist)):
        try:
            glink = getlink(linelist[i])
            title = linelist[i].split('http')[0]
            if title == '' and 'http' not in linelist[i-1]:
                title = linelist[i-1].replace('\r\n', '')
            if title.split(': ')[-1] == '':
                title = title.split(': ')[-2]
            else:
                title = title.split(': ')[-1]
            title = title.replace(' ', '').replace('：', '').replace(':', '').replace('|', '_').replace('"', '_').replace('/', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(';', '')
            title = Title(title)
            if bool(title) is True:
                linklist.append((title, glink, int(count)))
                count += 1
        except:
            pass
    return FilePage(linelist[0].replace('\n', ''), linklist)


def sortlist(l, key=None):
    num = 1
    temp = []
    for i in l:
        if i[0].sp is False:
            temp.append((i, i[0].sortint(key)))
            num = i[0].sortint(key)
        else:
            num = num + 0.01
            temp.append((i, num))
    temp.sort(key=lambda x: x[1])
    return [i[0] for i in temp]


def choices():
    print('工作模式: 1.整合贴抓取模式 2.链接列表抓取模式')
    choice1 = input('请输入选项: ')
    if choice1 == '1':
        link = input('请输入整合贴链接: ')
        link = getlink(link)
        Page = ZHPage(link).getlink()
    if choice1 == '2':
        file = input('输入链接列表文件名: ')
        if file == '':
            file = 'linklist.txt'
        Page = readtask(file)
    print('任务列表排序模式: ')
    print('0: 不排序 1: 智能排序 2: 首位排序 3: 末位排序 4: 自定义排序')
    choice2 = input('请选择: ')
    if choice2 == '1':
        sortedlist = sortlist(Page.linklist)
        Page.linklist = sortedlist
    if choice2 == '2':
        sortedlist = sortlist(Page.linklist, key=[0])
        Page.linklist = sortedlist
    if choice2 == '2':
        sortedlist = sortlist(Page.linklist, key=[-1])
        Page.linklist = sortedlist
    if choice2 == '3':
        keyin = input('请输入排序参数(参与排序的数字序号列表，多个序号使用空格分割): ')
        key = [int(i) for i in keyin.split(' ')]
        sortedlist = sortlist(Page.linklist, key=key)
        Page.linklist = sortedlist
    return Page


def work(Page):
    try:
        os.mkdir(Page.tieba)
    except FileExistsError:
        print('目标文件夹已存在，文件可能被覆盖。')
    worklist = [i[1] for i in Page.linklist]
    resultlist = pool.map(WordPage, worklist)
    for i in range(len(resultlist)):
        resultlist[i].stitle(Page.linklist[i][0])
    resultlist = [i for i in resultlist if i]
    for i in resultlist:
        i.getword()
    return (Page.tieba, resultlist)


def save(result):
    if makeepub is True:
        createbook(result)
    if maketxt is True:
        makeatxt(result)
    if singletxt is True:
        for i in result[1]:
            i.writetxt()


if __name__ == '__main__':
    subprocess.call("title 贴吧贴子自动抓取器", shell=True)
    Page = choices()
    result = work(Page)
    save(result)
    subprocess.call("pause", shell=True)
