import pystache, random
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
            <title>Serialism</title>
            </head>
            <body>
            <div id="header">
            <h3>Serialism</h3>
            <p>Rows and rows of numbers</p>
            </div>
            <div id="numbers">
            <table>
            <thead>
            <tr><th scope="col">Numbers</th></tr>
            </thead>
            <tbody>
            <tr><td><a href="/serialism/html">HTML</a></td></tr>
            </tbody>
            </table>
            </div>
            </body>
            </html>'''

