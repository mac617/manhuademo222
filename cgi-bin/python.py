#!/usr/bin/python
# !coding:utf8
import cgi, cgitb
import urllib
import urllib2
import re
import sys
import cookielib
import json

reload(sys)
sys.setdefaultencoding('utf8')

form = cgi.FieldStorage()
name = form.getvalue('name')
page = form.getvalue('page')
episode = form.getvalue('episode')
imgs = form.getvalue('imgs')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
}

print "Content-type: text/html"

print

if page is None and episode is None and imgs is None:
    url = "http://www.92mh.cc/search/" + name

    cj = cookielib.CookieJar()  # 获取cookiejar实例

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    req = urllib2.Request(url, headers=headers)

    html = opener.open(req).read()

    contents = re.findall(
        '<a class="imgbox" href="(.*?)" title="(.*?)".*?<img src="(.*?.jpg)".*?<p class="note">(.*?)</p>', html, re.S)

    for content in contents:
        print "<p>%s</p>" % content[1]
        print "<img src='%s' name='%s' onClick='saveUserInfo2(this.name)'>" % (content[2], content[0])
        print "<p>%s</p>" % content[3]
        print "<p>%s</p>" % page

elif page is not None and episode is None:

    url = page

    cj = cookielib.CookieJar()  # 获取cookiejar实例

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    req = urllib2.Request(url, headers=headers)

    html = opener.open(req).read()

    contents = re.findall('<li><a href="(http://www.92mh.cc/manhua/.*?/.*?\.html)"title="(.*?)">.*?</a></li>', html,
                          re.S)

    for content in contents:
        print "<input type='button' name='%s' value='%s' onclick='saveUserInfo3(this.name)'>" % (content[0], content[1])

elif episode is not None and imgs is None:

    url = episode

    req = urllib2.Request(url, headers=headers)

    html = urllib2.urlopen(req).read()

    contents = re.findall('eval.*?,0,\{}\)\)', html, re.S)

    rp_content = str(contents).replace("\\\\\\", "*", ).replace("\'", "\\", ).replace("\\\\", "\'", ).replace("*",
                                                                                                              "\\", )

    content = rp_content[6:][:-2]

    print content

else:
    find_img = re.findall('"images":\[(.*?)]}', imgs, re.S)
    url_img = find_img[0]
    content_img = re.findall('"(.*?)"', url_img, re.S)

    back_img = unicode(str(content_img), 'unicode-escape')

    rp_img = back_img.replace("[", "").replace("]", "").replace("\'", "")

    print rp_img