# 贴吧贴子抓取器

本程序出于抓取贴吧内小说为目的制作，可能应用于其他场景。

## 直接使用方法
确认Python3以及所需package正确安装，按照程序提示操作即可。
### 注意事项
1. 整合贴需要满足一定的格式才能够被正确抓取。详细要求请见下<br>
2. 标题不要出现特殊符号否则可能出现各种无法预料的问题<br>
<br>
## 高级设置
程序头部可以设置各种参数并附有解释。此处给出更加详细的解释。<br>
 getinline = False<br>
  是否检查贴子内包含的指向其他贴子的链接（具体例子见OSO吧）<br>
 threads = 32<br>
  最大连接线程数（32线程暂未发现贴吧有封禁现象）<br>
 orginfo = True<br>
  添加原作者和原帖地址信息（尊重翻译成果，请勿关闭）<br>
 makeepub = True<br>
  制作包含所有章节的epub文件<br>
 maketxt = True<br>
  制作包含所有章节的txt文件<br>
 singletxt = True<br>
  导出每帖的内容到单独的txt文件<br>
 hznum = True<br>
  尝试将汉字表达的数字转化为普通数字以进行排序（不能涵盖所有情况，容易出现误识别，尽量避免使用）<br>
 passtoshort = False<br>
  忽略过短的贴子（往往未进行翻译或使用图片（暂不支持抓取图片））<br>
 validreply = 200<br>
  有效回复值（应对非楼主提供翻译情况。楼主发言不进行过滤）<br>
<br>
## 支持格式举例<br>
1. <br>
  [otherword][num][title]<br>
  http://tieba.baidu.com/p/0000000000<br>
2. <br>
  [otherword][num][title]http://tieba.baidu.com/p/0000000000<br>
3. <br>
  auser: [other][num][title]http://tieba.baidu.com/p/0000000000<br>
  <br>
##### 本程序利用re模块，有较强的适应能力，但不保证非以上格式的情况可以被正确抓取<br>
##### 标题中的半角特殊符号可能导致不可预期的问题<br>
<br>
## 必须模块<br>
本程序需要下列python模块才能正常运行<br>
requests<br>
BeautifulSoup4<br>
ebooklib<br>
<br>
## 已知问题<br>
1. 有时会出现如下错误：<br>
  UserWarning: "b'...'" looks like a filename, not markup. You shouldprobably open this file and pass the filehandle intoBeautiful Soup.<br>
  目前并未发现不良后果，暂不处理<br>
2. 当有多个贴子指定了同一标题时会出现如下错误<br>
  UserWarning: Duplicate name: 'EPUB/xxx.xhtml'<br>
  不属于程序设计问题，暂不处理<br>
  <br>
## 暂未完成功能<br>
<br>
制作存档系统以避免更新后重复抓取内容。<br>
