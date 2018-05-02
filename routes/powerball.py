import pystache
from flask import request
def root():
    return '''<!DOCTYPE html>
            <html lang="en">
            <head>
            <style>
            table,th,td {
              border: 1px solid black;
              border-collapse: collapse;
              padding: 3px;
              text-align: center
            }
              td {text-align: left}
            </style>
            <title>Powerball</title>
            </head>
            <body>
            <div id="header">
            <h3>Powerball</h3>
            <p>Two sets of Powerball numbers</p>
            </div>
            <div id="numbers">
            <table>
            <thead>
            <tr><th scope="col">Numbers</th></tr>
            </thead>
            <tbody>
            <tr><td><a href="/powerball/html">HTML</a></td></tr>
            </tbody>
            </table>
            </div>
            </body>
            </html>'''
