import sqlite3,pystache
from flask import request

def root():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Gematria</title>
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
    <h1>Gematria</h1>
    <p>See also:<a href="https://en.wikipedia.org/wiki/Gematria">Wikipedia</a></p>
    </div>
    <div id="word_form">
    <p>Calculate the numerical value of a word.</p>
    <form action="/gematria/word" method="get">
    <input id="id_word_input" name="word" type="text">
    <input type="submit" value="Calculate"></form>
    </div>
    <div id="value_form">
    <p>Search the 10,000 most common English words by numerical value.</p>
    <form action="/gematria/value" method="get">
    <input id="id_value_input" name="value" type="text">
    <input type="submit" value="Search">
    </form>
    </div>
    </body>
    </html>'''
