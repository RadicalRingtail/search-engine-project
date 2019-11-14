from flask import Flask, render_template, request
import scraper

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search' , methods=['POST'])
def search():
    term = request.form['search_bar']
    return render_template('search.html', term=term, info=scraper.search(term), wiki=scraper.wikipedia_sraper(term))

if __name__ == '__main__':
    app.run()



    