import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    global_page_src = ""
    name = TextField('Name:', validators=[validators.required()])



@app.route("/", methods=['GET', 'POST'])
def hello():
    # Unicode of all hebrew characters mapped to transliterated symbols for the website.
    global global_page_src
    word_dict = {

        u'\u05d0': ")",  # א
        u'\u05d1': "b",  # ב
        u'\u05d2': "g",  # ג
        u'\u05d3': "d",  # ד
        u'\u05d4': "h",  # ה
        u'\u05d5': "w",  # ו
        u'\u05d6': "z",  # ז
        u'\u05d7': "H",  # ח
        u'\u05d8': "T",  # ט
        u'\u05d9': "y",  # י
        u'\u05db': "k",  # כ
        u'\u05da': "k",  # ך
        u'\u05dc': "l",  # ל
        u'\u05de': "m",  # מ
        u'\u05dd': "m",  # ם
        u'\u05e0': "n",  # נ
        u'\u05df': "n",  # ן
        u'\u05e1': "s",  # ס
        u'\u05e2': "(",  # ע
        u'\u05e4': "p",  # פ
        u'\u05e6': "S",  # צ
        u'\u05e7': "q",  # ק
        u'\u05e8': "r",  # ר
        u'\u05e9': "$",  # ש
        u'\u05ea': "t"  # ת

    }

    headers = {
        'Host': 'dukhrana.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '66', 'Referer': 'http://dukhrana.com/lexicon/Jastrow/index.php', 'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        #print(name)
        if form.validate():
            # Save the comment here.
            word_search = name

            encoded_input_word = list(word_search)
            word = []
            # Convert letters to symbols
            for letters in encoded_input_word:
                # Only allows hebrew letters to be typed
                try:
                    letter = word_dict[letters]
                    word.append(letter)
                except:
                    pass # Do nothing


            final_word = "".join(word)


            request_body = 'cmd=search&search_string=' + final_word + '&font=Estrangelo+Edessa&font_size=125%25'
            postRequest = requests.post('http://dukhrana.com/lexicon/Jastrow/index.php', headers=headers,
                                            data=request_body)
            htmlCode = postRequest.content

            soup = BeautifulSoup(htmlCode, "html.parser")
            images = soup.find_all("img")
            img = images[1]
            page_src = img["src"]

            global_page_src = page_src


            get_page_url = "http://dukhrana.com/lexicon/Jastrow/" + page_src
            daf = requests.get(get_page_url)
            # info = daf.content.decode("utf-8")
            # print(daf.text)
            flash(get_page_url)

        elif request.form['submit'] == 'Next Page':
            try:
                pg = global_page_src.split("//")
                pg = pg[1].split(".")
                pgs = int(pg[0]) + 1

                if pgs < 100:
                    page_src = "pages//00" + str(pgs) + ".jpg"
                elif pgs < 1000:
                    page_src = "pages//0" + str(pgs) + ".jpg"

                else:
                    page_src = "pages//" + str(pgs) + ".jpg"
                global_page_src = page_src
                get_page_url = "http://dukhrana.com/lexicon/Jastrow/" + page_src
                flash(get_page_url)
            except:
                flash("Error: The Next page buttons only work after a search is made")


        elif request.form['submit'] == 'Previous Page':
            try:
                pg = global_page_src.split("//")
                pg = pg[1].split(".")
                pgs = int(pg[0]) - 1

                if pgs < 100:
                    page_src = "pages//00" + str(pgs) + ".jpg"
                elif pgs < 1000:
                    page_src = "pages//0" + str(pgs) + ".jpg"

                else:
                    page_src = "pages//" + str(pgs) + ".jpg"
                get_page_url = "http://dukhrana.com/lexicon/Jastrow/" + page_src
                flash(get_page_url)
            except:
                flash("Error: The Previous Page Button does not work until a search is made ")

        else:
            flash('Error: Fill in the box with Hebrew Letters.')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()