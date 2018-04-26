import sqlite3,pystache
def root():
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

report_template = '''<html><head>
                     <style>table,th,td {
                               border: 1px solid black;
                               border-collapse: collapse;
                               padding: 3px;
                               text-align: center
                               }
                             td {text-align: left}</style>
                     </head><body><table>
                     {{#results}}
                     <tr>{{#result}}<td>{{.}}</td>{{/result}}</tr>
                     {{/results}}
                     </table></body></html>
                     '''
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
        conn = sqlite3.connect('./resources/destiny.db')
        c = conn.cursor()
        c.execute(report_dict[report])
        all_results = c.fetchall()
        print(type(c.fetchall()))
        all_results = list(map(lambda x: {"result": x}, all_results))
    else:
        all_results = "Invalid report name"
    all_results = {"results": all_results}
    return pystache.render(report_template,all_results)
