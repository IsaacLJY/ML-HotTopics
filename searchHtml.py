import os
import urllib.request as urllib2
from urllib import error
import gzip
from bs4 import BeautifulSoup

# search conference paper titles and find topic words
def search(conf, year, words):
    if os.path.exists("./data/"+conf+year+".html"):
        fread = open("./data/"+conf+year+".html", 'r')
        content = fread.read()
        fread.close()
    else:
        url = "http://dblp.uni-trier.de/db/conf/" + conf + "/" + conf + year + ".html"
        ua_headers = {
            'Host': 'dblp.uni-trier.de',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://dblp.uni-trier.de/db/conf/aaai/',
            'Cookie': 'dblp-view=y; dblp-search-mode=c; dblp-bibtex=2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        request = urllib2.Request(url, headers = ua_headers)
        response = urllib2.urlopen(request)
        html = response.read()

        content = gzip.decompress(html)
        content = bytes.decode(content)
        f = open("./data/"+conf+year+".html", 'w')
        f.write(content)
        f.close()

    soup = BeautifulSoup(content, "html.parser")
    class_list = soup.find_all(attrs={'class':'Z3988'})

    times = {}
    times["total"] = len(class_list)
    for word in words:
        times[word] = 0
    for one in class_list:
        title = one.get('title')
        title = title.lower()
        if title:
            for word in words:
                times[word] = times[word] + title.count(word)
    return times

# write the consequece into file
def search_write(confs, conf_class,  file):
    file.write("ML conference class " + conf_class + "\n")
    for year in range(2017, 2012, -1):
        year = str(year)
        for conf in confs:
            try:
                words_times = search(conf, year, words)
                print(words_times)
                times = "" + str(words_times["total"])
                for word in words:
                    times = times + "," + str(words_times[word])
            except error.URLError as e:
                file.write(year + "," + conf + "," + e.reason + "\n")
            else:
                file.write(year + "," + conf + "," + times + "\n")
            print(conf_class + ": " + conf + year + " complete.")

# write the header of csv file
def write_header(words, file):
    header = ",,total"
    for word in words:
        header = header + "," + word
    file.write(header + "\n")

words = [ "adversarial", "cluster", "kernel"]
confa = ["aaai", "cvpr", "iccv", "icml", "ijcai", "nips", "acl"]
confb = ["colt", "emnlp", "ecai", "eccv", "icra", "aips", "iccbr", "coling", "kr", "uai", "atal", "ppsn"]
confc = ["accv", "conll", "gecco", "ictai", "alt", "icann", "fgr", "icdar", "ilp", "ksem", "iconip", "icpr", "icb", "ijcnn", "pricai", "naacl", "bmvc", "iros", "aistats", "acml"]

if os.path.exists("MLhot.csv"):
    os.remove("MLhot.csv")
f = open("MLhot.csv", 'a')

write_header(words, f)
search_write(confa, "A", f)
search_write(confb, "B", f)
search_write(confc, "C", f)

f.close()
