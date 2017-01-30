# Tieba-Content-Getter
This script can save the content of tieba pages as txt and epub files.

#Usage:
Put words contains the links to catch into linklist.txt at the same directory of getter.py and just run it. Then it will do everything. More settings can be set in the script.

#Format of linklist.txt:
title  # the first line should be the title. All files will be saved in ./title/ folder.
filenamehttp://tieba.baidu.com/p/(pageid) #filename will be the name of the txt file.the link should be put beside.
(otherword): Web 211：http://tieba.baidu.com/p/(pageid)(otherword) #word before': ',word after link,illegal characters of filename spaces and full'：' can be automaticly removed.
$^%^&#%&^%$&*&^$&%&*  #those lines that don't contain a link will be automaticly ignored.

#Dependencies:
This script requires python3.
This script requires python libs : requests, beautifulsoup4 and ebooklib.
This script is tested with python3.6 on Windows10. Other version and platfrom might meet errors.
