from flask import Flask,Response
import sqlite3, pystache
from routes import destiny, powerball, serialism
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
              <p>There is a (twin) sister site written in Clojure: <a href = "http://ericervin.org">http://ericervin.org</a>
              <br>
              </div>
              <div id="resources">
              <table>
              <thead><tr><th scope="col">Resource</th><th scope="col">Description</th><th scope="col">Data Updated</th></tr></thead>
              <tbody>
              <tr><td><a href="/destiny">Destiny</a></td><td>Star Wars Destiny card game data</td><td>04/16/2018</td></tr>
              <tr><td><a href="/powerball">Powerball</a></td><td>A source for Powerball numbers to play</td><td>N/A</td></tr>
              <tr><td><a href="/serialism">Serialism</a></td><td>Toying with set theory</td><td>N/A</td></tr>
              </tbody>
              </table>
              </div>
              </html>
              '''

app.add_url_rule('/destiny','destiny_root',destiny.root)
app.add_url_rule('/destiny/reports/<report>','destiny_reports',destiny.reports)
app.add_url_rule('/destiny/cards','destiny_cards',destiny.cards) 

app.add_url_rule('/powerball','powerball_root',powerball.root)
app.add_url_rule('/powerball/html','powerball_res_html',powerball.res_html)

app.add_url_rule('/serialism','serialism_root',serialism.root)

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
