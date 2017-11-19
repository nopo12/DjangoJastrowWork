import timeit
import requests
from bs4 import BeautifulSoup

class JastrowDaf:
    # Unicode of all hebrew characters mapped to transliterated symbols for the website.
    word_dict = {

        u'\u05d0':")",# א
        u'\u05d1':"b",# ב
        u'\u05d2':"g",# ג
        u'\u05d3':"d",# ד
        u'\u05d4':"h",# ה
        u'\u05d5':"w",# ו
        u'\u05d6':"z",# ז
        u'\u05d7':"H",# ח
        u'\u05d8':"T",# ט
        u'\u05d9':"y",# י
        u'\u05db':"k",# כ
        u'\u05da':"k",# ך
        u'\u05dc':"l",# ל
        u'\u05de': "m",# מ
        u'\u05dd':"m",# ם
        u'\u05e0':"n",# נ
        u'\u05df':"n",# ן
        u'\u05e1':"s",# ס
        u'\u05e2':"(",# ע
        u'\u05e4':"p",# פ
        u'\u05e6':"S",# צ
        u'\u05e7':"q",# ק
        u'\u05e8':"r",# ר
        u'\u05e9':"$",# ש
        u'\u05ea':"t" # ת

    }

    headers = {
        'Host': 'dukhrana.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'66','Referer':'http://dukhrana.com/lexicon/Jastrow/index.php','Connection':'keep-alive','Upgrade-Insecure-Requests':'1',
        'Cache-Control':'max-age=0'
    }


    def __init__(self,headers,word_dict):
        self.headers = headers
        self.word_dict = word_dict

    def read_input(self):
        #payload = {'cmd': 'search', 'search_string': 't','font':'Estrangelo+Edessa','font_size':'125%'}
        input_word = input("Enter a word: ")
        #word = word.decode('utf-8')
        incoded_input_word = list(input_word)
        word = []
        # Convert letters to symbols
        for letters in incoded_input_word:
            letter = self.word_dict[letters]
            word.append(letter)
        return "".join(word)

    def postRequest(self,word):
        request_body = 'cmd=search&search_string=' + word +'&font=Estrangelo+Edessa&font_size=125%25'
        postRequest = requests.post('http://dukhrana.com/lexicon/Jastrow/index.php', headers=headers,data=request_body)

        htmlCode = postRequest.content
        return htmlCode

    def parse_html(self,htmlCode):

        soup = BeautifulSoup(htmlCode,"html.parser")

        images = soup.find_all("img")
        img = images[1]
        page_src = img["src"]
        return page_src

    def getRequest(self,page_src):
        get_page_url = "http://dukhrana.com/lexicon/Jastrow/" + page_src
        daf = requests.get(get_page_url)
        #info = daf.content.decode("utf-8")

        print(daf.text)

def main():
    getPage = JastrowDaf(JastrowDaf.headers,JastrowDaf.word_dict)
    start = timeit.default_timer()
    user_input = getPage.read_input()
    html_code = getPage.postRequest(user_input)
    source = getPage.parse_html(html_code)
    getSrc = getPage.getRequest(source)
    stop = timeit.default_timer()
    print("The Program took " + str(stop - start) + " seconds")

if __name__ == "__main__":
    main()
