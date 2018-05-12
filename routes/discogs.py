import pystache
from flask import request

def root():
    return '''
       <!DOCTYPE html>
       <html lang="en">
       <head>
         <title>Discogs</title>
         <style> table,th,td {
                 border: 1px solid black;
                 border-collapse: collapse;
                 padding: 3px;
                 text-align: center;}              
                 td {text-align: left}
         </style>
       </head>
       <body>
         <div id="header"><h1>My Record Collection</h1></div>
         <div id="releases">
         <h4>Releases</h4>
         <table>
           <thead>
            <tr>
            <th></th>
            <th scope="col">By Title</th>
            <th scope="col">By Artist</th>
            <th scope="col">By Label</th>
            <th scope="col">By Release Year</th></tr>
          </thead>
          <tbody>
            <tr>
            <th>All</th><td><a href="/discogs/releases?sort=title">HTML</a></td>
            <td><a href="/discogs/releases?sort=artist">HTML</a></td>
            <td><a href="/discogs/releases?sort=label">HTML</a></td>
            <td><a href="/discogs/releases?sort=year">HTML</a></td></tr>
          </tbody>
       </table>
       </div>
       <div id="reports"><h4>Reports</h4>
      <table>
        <thead><tr>
        <th scope="col">Report</th><th scope="col">Format</th></tr></thead>
        <tbody>
          <tr><td>Count by Artist</td><td><a href="/discogs/reports?rpt=artist_count\>HTML</a></td></tr>
          <tr><td>Count by Label</td><td><a href="/discogs/reports?rpt=label_count">HTML</a></td></tr>
          <tr><td>Count by Year Released</td><td><a href="/discogs/reports?rpt=year_count">HTML</a></td></tr>
        </tbody>
      </table></div></body></html>'''
