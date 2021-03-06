#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import json
from multiprocessing.dummy import Pool as tp
import subprocess
import os
import base64
from ebooklib import epub

#是否抓取内链内容
getinline = False
#连接线程数
threads = 32
#忽略单独链接
ignoresinglelink = True
#增加原作者信息
orginfo = True
#创建epub
makeepub = True
#创建总txt
maketxt = True
#汉字数字化排序
hznum = True
#忽略过短贴子
passtoshort = False


#除非理解含义否则不要改动！
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2922.1 Safari/537.36'}
htmlparser = 'html.parser'
pool = tp(processes=threads)
dirname = os.getcwd()
warn = '本文件为自动抓取程序生成的文件'
about = b'PGh0bWw+PGhlYWQ+PC9oZWFkPjxib2R5PjxoMz7mnKzkuabkv6Hmga88L2gzPjxwPuacrOS5pueUseiEmuacrOiHquWKqOS7jueZvuW6pui0tOWQp+aKk+WPluW5tueUn+aIkOOAgjwvcD4KPHA+5Y+v6IO95Ye6546w5ZCE56eN5o6S54mI6Zeu6aKY6K+36Ieq6KGM5paf6YWM5L2/55So44CCPC9wPgo8cD7or7flsIrph43ljp/kvZzogIXlj4rnv7vor5HogIXnmoTlirPliqjmiJDmnpzvvIE8L3A+PC9ib2R5PjwvaHRtbD4='
tabout = b'5pys5Lmm5L+h5oGvCuacrOS5pueUseiEmuacrOiHquWKqOS7jueZvuW6pui0tOWQp+aKk+WPluW5tueUn+aIkOOAggrlj6/og73lh7rnjrDlkITnp43mjpLniYjpl67popjor7foh6rooYzmlp/phYzkvb/nlKjjgIIK6K+35bCK6YeN5Y6f5L2c6ICF5Y+K57+76K+R6ICF55qE5Yqz5Yqo5oiQ5p6c77yB'
style = b'CkBuYW1lc3BhY2UgZXB1YiAiaHR0cDovL3d3dy5pZHBmLm9yZy8yMDA3L29wcyI7CmJvZHkgewogICAgZm9udC1mYW1pbHk6IENhbWJyaWEsIExpYmVyYXRpb24gU2VyaWYsIEJpdHN0cmVhbSBWZXJhIFNlcmlmLCBHZW9yZ2lhLCBUaW1lcywgVGltZXMgTmV3IFJvbWFuLCBzZXJpZjsKfQpoMiB7CiAgICAgdGV4dC1hbGlnbjogbGVmdDsKICAgICB0ZXh0LXRyYW5zZm9ybTogdXBwZXJjYXNlOwogICAgIGZvbnQtd2VpZ2h0OiAyMDA7ICAgICAKfQpvbCB7CiAgICAgICAgbGlzdC1zdHlsZS10eXBlOiBub25lOwp9Cm9sID4gbGk6Zmlyc3QtY2hpbGQgewogICAgICAgIG1hcmdpbi10b3A6IDAuM2VtOwp9Cm5hdltlcHVifHR5cGV+PSd0b2MnXSA+IG9sID4gbGkgPiBvbCAgewogICAgbGlzdC1zdHlsZS10eXBlOnNxdWFyZTsKfQpuYXZbZXB1Ynx0eXBlfj0ndG9jJ10gPiBvbCA+IGxpID4gb2wgPiBsaSB7CiAgICAgICAgbWFyZ2luLXRvcDogMC4zZW07Cn0K'
hznuml = [('九千', '9'), ('八千', '8'), ('七千', '7'), ('六千', '6'), ('五千', '5'), ('四千', '4'), ('三千', '3'), ('两千', '2'), ('二千', '2'), ('一千', '1'), ('千', '1'), ('九百', '9'), ('八百', '8'), ('七百', '7'), ('六百', '6'), ('五百', '5'), ('四百', '4'), ('三百', '3'), ('二百', '2'), ('一百', '1'), ('百', '1'), ('九十', '9'), ('八十', '8'), ('七十', '7'), ('六十', '6'), ('五十', '5'), ('四十', '4'), ('三十', '3'), ('二十', '2'), ('一十', '1'), ('十', '1'), ('九', '9'), ('八', '8'), ('七', '7'), ('六', '6'), ('五', '5'), ('四', '4'), ('三', '3'), ('二', '2'), ('一', '1'), ('零', '0'), ('〇', '0')]


def getpage(url, ht=htmlparser, hd=headers):
    '''读取页面内容'''
    gethtml = requests.get(url, headers=hd)
    Soup = BeautifulSoup(gethtml.text, ht)
    return Soup


def getword(page, info=''):
    '''获取页面中的文字'''
    try:
        titleget = page.find('h3').get_text()
    except AttributeError:
        titleget = ''
    containget1 = page.find('div', class_='p_postlist').find_all('cc')
    containget2 = [a.find_all('div') for a in containget1]
    containget3 = [b.get_text('\r\n') for a in containget2 for b in a]
    contain = '\r\n\r\n'.join(containget3)
    word = titleget + '\r\n' + info + contain + '\r\n'
    return word


def pages(page):
    '''读取页面数'''
    return int(page.find('span', class_='red', style=None).get_text())


def getpages(link):
    '''处理页面'''
    page = getpage(link)
    pagenum = pages(page)
    word = ''
    if pagenum == 1:
        if orginfo is True:
            info = '作者：' + page.find('li', class_='d_name').get_text('').replace('\n', '') + '  原帖地址：' + link.replace('?see_lz=1', '')
            info = info + '\r\n' + warn + '\r\n'
        else:
            info = ''
        word = getword(page, info)
    else:
        word = getword(page)
        for i in range(2, pagenum + 1):
            page = getpage(link + '&pn=' + str(i))
            word = word + getword(page) + '\r\n'
    return word


def getinline(word):
    '''寻找内链'''
    listtuple = re.findall('(http\:\/\/tieba\.baidu\.com\/p\/)([0-9]{10})', word)
    return [''.join(a) + '?see_lz=1' for a in listtuple]


def process(protuple):
    '''总任务分发'''
    try:
        word = getpages(protuple[0])
    except AttributeError:
        print('页面{0}抓取失败,请检查原帖。跳过文件{1}'.format(protuple[0], protuple[1]))
        return None
    if len(word) < 1024 and passtoshort is True:
        print('页面{0}长度过短,请检查原帖。跳过文件{1}'.format(protuple[0], protuple[1]))
        return None
    if getinline is True:
        inlist = getinline(word)
        if inlist is not None:
            print('页面' + protuple[0] + '发现内链，正在深度抓取。')
            for l in inlist:
                inpage = getpages(l)
                l = l.replace('?see_lz=1', '')
                word = word.replace(l, l + '\r\n--------深度抓取内容--------\r\n' + inpage + '\r\n--------深度抓取内容--------\r\n')
    g = open(dirname + '\\' + maintitle + '\\' + protuple[1] + '.txt', mode='wb')
    g.write(word.encode('utf-8'))
    print('页面{0}抓取成功,保存为{1}.txt'.format(protuple[0], protuple[1]))
    if makeepub or maketxt is True:
        return (protuple[1], word)


def readtasks(f, filemode=True):
    processlist = []
    global pastline
    print('开始抓取。读取网页列表中...')
    maintitle = ''
    for line in f:
        if filemode is True:
            if maintitle == '':
                maintitle = line.replace('\n', '')
        #将首行定为总名
        try:
            link = ''.join(re.findall('(http\:\/\/tieba\.baidu\.com\/p\/)([0-9]{10})', line)[0]) + '?see_lz=1'
            title = line.split('http')[0]
            #若本行无标题则读取上一行
            if title == '':
                if pastline is not None:
                    title = pastline.replace('\n', '')
                elif ignoresinglelink is False:
                    title = ''.join(re.findall('([0-9]{10})', link)[0])
            if title.split(': ')[-1] == '':
                title = title.split(': ')[-2]
            else:
                title = title.split(': ')[-1]
            #处理文件名（防止非法字符)
            title = title.replace(' ', '').replace('：', '').replace(':', '').replace('|', '_').replace('"', '_').replace('/', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(';', '')
            if '文庫版' in title or '文库版' in title or '插图' in title:
                pass
            elif bool(re.search('txt', title, re.IGNORECASE)) or bool(re.search('epub', title, re.IGNORECASE)):
                pass
            elif '序' in title or '终' in title:
                processlist.append((link, title))
            elif hznum is False and re.findall('(\d{1,10})(?!\d)', title) == [] and filemode is False:
                pass
            elif hznum is True and re.findall('(\d{1,10})(?!\d)', hztonum(title)) == [] and filemode is False:
                pass
            else:
                processlist.append((link, title))
            pastline = None
        except IndexError:
            pastline = line
    processlist = list(set(processlist))
#    print(processlist)
#    try
    choice = input('请选择排序方式:0.字符串排序 1.首数字排序 2.次数字排序 3.末数字排序 4.章-话排序:')
    if not choice == 'pass':
        try:
            processlist.sort(key=lambda x: getfilenum(x[1], choice))
        except (KeyError, ValueError):
            print('排序失败，不使用排序。')
#    except:
#        print('选择的方案排序失败!使用字符串排序方案。')
#        processlist.sort()
    if filemode is True:
        return (maintitle, processlist)
    else:
        return processlist


def refilename(instr):
    outstr = instr.replace('：', '').replace(':', '').replace('|', '_').replace('"', '_').replace('/', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').encode('gbk', 'ignore').decode('gbk')
    return outstr


def txttohtml(txt):
    htmllist = ['<html>\n<head>\n']
    txtline = txt.split()
    htmllist.append('<title>' + txtline[0] + '</title>\n</head>\n<body>\n<div>\n<h3>' + txtline[0] + '</h3>\n')
    for l in txtline[1:]:
        htmllist.append('<p>' + l + '</p>\n')
    htmllist.append('</div>\n</body>\n</html>')
    return ''.join(htmllist)


def createbook(title, content):
    print('制作Epub选项已开启，正在制作epub。')
    book = epub.EpubBook()
    book.set_identifier(b'id' + base64.b64encode(bytes(title, 'utf-8')))
    book.set_title(title)
    book.set_language('zh')
    book.add_author('Python Tieba Spider Epub Maker by TYTY')
    sabout = base64.b64decode(about).decode('utf-8')
    cabout = epub.EpubHtml(title='本书信息', file_name='0.xhtml', content=sabout, lang='zh_cn')
    book.add_item(cabout)
    conlist = [epub.EpubHtml(title=i[0], file_name=i[0].replace('.txt', '').replace('Web', '') + '.xhtml', content=txttohtml(i[1]), lang='zh_cn') for i in content]
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
    epub.write_epub(dirname + '\\' + title + '\\' + title + '.epub', book, {})
    print('Epub制作成功。')


def makeatxt(title, content):
    print('制作合集TXT选项已开启，正在制作txt。')
    con = []
    con.append(base64.b64decode(tabout).decode('utf-8') + '\r\n\r\n\r\n\r\n\r\n\r\n')
    for i in content:
        con.append(i[0] + '\r\n\r\n' + i[1] + '\r\n\r\n\r\n')
    fi = ''.join(con)
    g = open(dirname + '\\' + title + '\\' + title + '.txt', 'wb')
    g.write(fi.encode('utf-8'))
    print('合集TXT制作成功。')


def hztonum(instr):
    instr2 = re.findall('[零一二三四五六七八九十百千〇]{1,20}', instr)
    if instr2 == []:
        return instr
    else:
        orstr = instr2[0]
        instr2 = instr2[0]
    if instr2[-1] == '千':
        instr2 = instr2.replace('千', '000')
    if instr2[-1] == '百':
        instr2 = instr2.replace('百', '00')
    if instr2 == '十':
        instr2 = instr2.replace('十', '10')
    if instr2[-1] == '十':
        instr2 = instr2.replace('十', '0')
    for i in hznuml:
        instr2 = instr2.replace(i[0], i[1])
    return instr.replace(orstr, instr2)


def getfilenum(instr, choice):
#    print(instr)
    if hznum is True:
        instr = hztonum(instr)
    if '序' in instr:
        return 0
    if '闲' in instr or '閒' in instr:
        return 10000
    if '终话' in instr or '终章' in instr:
        return 5000
    if choice == '0':
        return None
    if choice == '1':
        return float(''.join(re.findall('(\d{1,10})(\.\d)?(?!\d)', instr)[0]))
    if choice == '2':
        return float(''.join(re.findall('(\d{1,10})(\.\d)?(?!\d)', instr)[1]))
    if choice == '3':
        return float(''.join(re.findall('(\d{1,10})(\.\d)?(?!\d)', instr)[-1]))
    if choice == '4':
        return int(''.join([i.zfill(5) for i in re.findall('(\d{1,10})(?!\d)', instr)[:2]]))


def getrword(e):
    (pid, num) = e
    pnum = num // 10 + 2
    li = []
    for i in range(1, pnum):
        link = 'http://tieba.baidu.com/p/comment?tid=' + tid + '&pid=' + pid + '&pn=' + str(i)
        li = li + getpage(link).get_text().split('回复')
    return li


def findreply(tag):
    hn = tag.name == 'div'
    if tag.has_attr('class') is True:
        if tag['class'] == ['j_lzl_r', 'p_reply']:
            hc = True
        else:
            hc = False
    else:
        hc = False
    h = hc and hn
    return h


def parsezp(link, am=False):
    page = getpage(link)
    pagenum = pages(page)
    global tid
    tid = re.findall('\d{10}', link)[0]
    title = page.find('title').get_text().split('_')[-2].replace('吧', '')
    llist = page.find_all(findreply)
    word = ''
    if pagenum == 1:
        word = getword(page).split('\r\n')
    else:
        word = getword(page).split('\r\n')
        for i in range(2, pagenum + 1):
            page = getpage(link + '&pn=' + str(i))
            llist = llist + page.find_all(findreply)
            word = word + getword(page).split('\r\n')
    d = [json.loads(i['data-field']) for i in llist]
    e = [(str(i['pid']), i['total_num']) for i in d if i['total_num'] is not None]
    rlist = pool.map(getrword, e)
    word = word + [j for i in rlist for j in i]
    if am is True:
        return '\r\n'.join(word)
    linklist = readtasks(word, False)
    return (title, linklist)


if __name__ == '__main__':
    c1 = input('1.读取linklist.txt 2.从整合贴抓取')
    if c1 == '1':
        f = open('linklist.txt', mode='r')
        (maintitle, processlist) = readtasks(f)
    if c1 == '2':
        link = input('请输入整合贴链接:')
        (maintitle, processlist) = parsezp(link)
    try:
        os.mkdir(maintitle)
    except FileExistsError:
        print('目标文件夹已存在，文件可能被覆盖。')
    if makeepub and maketxt is False:
        pool.map(process, processlist)
    else:
        content = pool.map(process, processlist)
        content = [i for i in content if i is not None]
        if makeepub is True:
            createbook(maintitle, content)
        if maketxt is True:
            makeatxt(maintitle, content)
    subprocess.call("pause", shell=True)
