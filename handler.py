from flask import Flask,Response
import sqlite3, pystache
from routes import destiny
app = Flask(__name__)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
              <html lang="en">
              <head>
              <title>Eric Ervin Dot Com</title>
              <style>table,th,td {
                               border: 1px solid black;
                               border-collapse: collapse;
                               padding: 3px;
                               text-align: center
                               }
                             td {text-align: left}</style>
              </head>
              <body>
              <div id="header">
              <h1>Eric Ervin Dot Com</h1>
              <p>A toy website to release some Python into the world.</p>
  
              <p><a href="https://github.com/ericcervin/AskFlapp">https://github.com/ericcervin/AskFlapp</a></p>
              <br>
              </div>'''

app.add_url_rule('/destiny','destiny_root',destiny.root)
app.add_url_rule('/destiny/reports/<report>','destiny_reports',destiny.reports)
app.add_url_rule('/destiny/cards','destiny_cards',destiny.cards) 

@app.route('/robots.txt')
def robots():
    return Response('User-agent: *\nDisallow: /',mimetype='text/plain')

@app.errorhandler(404)
def error404(error):
    return '''<!DOCTYPE html>
              <html lang="en">
              <head>
              <title>Error 404 Not Found</title>
              </head>
              <body>404 - Not Found</body>
              </html>'''

if __name__ == '__main__':
    app.run(debug=True)
