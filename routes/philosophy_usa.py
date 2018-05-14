import sqlite3,pystache
from flask import request

def root():
    return '''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <title>Philosophy USA</title>
        <style>table,th,td {
               border: 1px solid black;
               border-collapse: collapse;
               padding: 3px;
               text-align: center }
          td {text-align: left}
        </style>
      </head>
      <body>
        <div id="header">
          <h1>Philosophy USA</h1>
            <p>Philosophy and religious studies degrees completed during the 2014-2015 academic year.</p>
            <p>Data taken from the Integrated Postsecondary Education Data System (IPEDS)</p>
            <p><a href="https://nces.ed.gov/ipeds/Home/UseTheData">https://nces.ed.gov/ipeds/Home/UseTheData</a></p>
        </div>
        <div id=\"reports\">
          <h4>Reports</h4>
          <table>
            <thead>
              <tr>
                <th scope=\"col\">Report</th>
                <th scope=\"col\">Format</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Philosophy Degrees Completed by Award Level</td><td><a href="/philosophy/reports?rpt=awlevel_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by Institution</td><td><a href="/philosophy/reports?rpt=inst_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by State</td><td><a href="/philosophy/reports?rpt=state_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by Subject Classification</td><td><a href="/philosophy/reports?rpt=cip_count">HTML</a></td></tr>
            </tbody>
          </table>
        </div>
      </body>
    </html>
           '''
