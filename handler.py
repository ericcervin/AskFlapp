from flask import Flask,Response
import sqlite3
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

@app.route('/destiny')
def destiny():
    return '''<!DOCTYPE html>
              <html lang="en">
              <head>
              <title>Destiny</title>
              <style>
              table,th,td {
                               border: 1px solid black;
                               border-collapse: collapse;
                               padding: 3px;
                               text-align: center
                               }
              td {text-align: left}
              </style>
              </head>
              <body>
              <div id="header">
              <h1>Star Wars Destiny</h1>
              <br>
              </div>
              <div id="reports">
              <h4>Reports</h4>
              <table>
              <tr><td>Compatible with Villains, Command</td><td><a href="/destiny/reports/villain_command_compatible">HTML</a></td></tr>   
              <tr><td>Count by Affiliation/Faction</td><td><a href="/destiny/reports/affiliation_faction_count">HTML</a></td></tr>
              </table>
              </div>
              </body>
              </html>'''

@app.route('/destiny/reports/<report>')
def reports(report):
    
    report_dict = {
        "villain_command_compatible" :
              '''Select cardsetcode, position, name, typename, affiliation,
                 factioncode, isunique, raritycode, ccost, csides,
                 imgsrc from card
                 where (affiliation = "Villain" or affiliation = "Neutral" )
                 and (faction = "Command" or faction = "General")''',
         "affiliation_faction_count" :
              '''Select affiliation, faction, count(*) as count from card group by affiliation, faction'''
        
        }
    if report in report_dict:
        conn = sqlite3.connect('./destiny.db')
        c = conn.cursor()
        c.execute(report_dict[report])
        result = c.fetchall()
    else:
        result = "Invalid report name"
    return str(result)

@app.route('/user/<name>')
def user(name):
    return "<h1>Hello, %s</h1>" % name

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
