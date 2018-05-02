import sqlite3,pystache
from flask import request
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
              <div id="cards">
              <table>
              <thead>
              <tr><th><th><th colspan="4">Affiliation</th></tr>
              <tr><th></th><th></th><th scope="col">All</th><th scope="col">Villain</th><th scope="col">Hero</th><th scope="col">Neutral</th></tr></thead>
              <tbody>
              <tr><th rowspan="5">Faction</th><th scope="row">All</th><td><a href="/destiny/cards?">HTML</a></td><td><a href="/destiny/cards?affil=Villain">HTML</a></td><td><a href="/destiny/cards?affil=Hero">HTML</a></td><td><a href="/destiny/cards?affil=Neutral">HTML</a></td></tr>
              <tr>

              <th scope="row">Command</th>
              <td><a href="/destiny/cards?fact=Command">HTML</a></td>
              <td><a href="/destiny/cards?affil=Villain&fact=Command">HTML</a></td>
              <td><a href="/destiny/cards?affil=Hero&fact=Command">HTML</a></td>
              <td><a href="/destiny/cards?affil=Neutral&fact=Command">HTML</a></td>
              </tr>
              <tr>

              <th scope="row">Force</th>
              <td><a href="/destiny/cards?fact=Force">HTML</a></td>
              <td><a href="/destiny/cards?affil=Villain&fact=Force">HTML</a></td>
              <td><a href="/destiny/cards?affil=Hero&fact=Force">HTML</a></td>
              <td><a href="/destiny/cards?affil=Neutral&fact=Force">HTML</a></td>
              </tr>
              <tr>

              <th scope="row">Rogue</th>
              <td><a href="/destiny/cards?fact=Rogue">HTML</a></td>
              <td><a href="/destiny/cards?affil=Villain&fact=Rogue">HTML</a></td>
              <td><a href="/destiny/cards?affil=Hero&fact=Rogue">HTML</a></td>
              <td><a href="/destiny/cards?affil=Neutral&fact=Rogue">HTML</a></td>
              </tr>
              <tr>

              <th scope="row">General</th>
              <td><a href="/destiny/cards?fact=General">HTML</a></td>
              <td><a href="/destiny/cards?affil=Villain&fact=General">HTML</a></td>
              <td><a href="/destiny/cards?affil=Hero&fact=General">HTML</a></td>
              <td><a href="/destiny/cards?affil=Neutral&fact=General">HTML</a></td>
              </tr>
              </tbody>
              </table>
              </div>
              <div id="reports">
              <h4>Reports</h4>
              <table>
              <tr><td>Compatible with Villains, Command</td><td><a href="/destiny/reports/villain_command_compatible">HTML</a></td></tr>   
              <tr><td>Count by Affiliation/Faction</td><td><a href="/destiny/reports/affiliation_faction_count">HTML</a></td></tr>
              <tr><td>Count by Rarity</td><td><a href="/destiny/reports/rarity_count">HTML</a></td></tr>
              <tr><td>Count by Set</td><td><a href="/destiny/reports/set_count">HTML</a></td></tr>
              <tr><td>Highest Cost Support/Event/Upgrade</td><td><a href="/destiny/reports/high_cost">HTML</a></td></tr>
              <tr><td>Rarity Legendary Cards</td><td><a href="/destiny/reports/legendary">HTML</a></td></tr>
              <tr><td>Rarity Rare Cards</td><td><a href="/destiny/reports/rare">HTML</a></td></tr>
              <tr><td>Type Character Cards</td><td><a href="/destiny/reports/type_character">HTML</a></td></tr>
              </table>
              </div>
              </body>
              </html>'''

report_template = '''<html><head>
                     <title>Destiny</title>
                     <style>
                     table,th,td {
                               border: 1px solid black;
                               border-collapse: collapse;
                               font-size: small;
                               padding: 3px;
                               text-align: center
                               }
                               td {text-align: left}
                     </style>
                     </head>
                     </head><body>
                     <div id="report">
                     <table id = \"id_card_table\">
                     <thead>
                     <tr>{{#header}}<th>{{.}}</th>{{/header}}</tr>
                     </thead>
                     <tbody>
                     {{#results}}
                     <tr>{{#result}}<td>{{.}}</td>{{/result}}</tr>
                     {{/results}}
                     </tbody>
                     </table></body></html>
                     '''

def qry_html(qry_dict):
        conn = sqlite3.connect('./resources/destiny.db')
        c = conn.cursor()
        c.execute(qry_dict["query"])
        all_results = c.fetchall()
        all_results = list(map(lambda x: {"result": x}, all_results))
        header = qry_dict["header"]
        all_results = {"header":header, "results": all_results}
        return pystache.render(report_template,all_results)
    
def cards():
    affil = request.args.get("affil")
    fact =  request.args.get("fact")
    select_fields = "cardsetcode, position, name, typename, isunique, raritycode, affiliation, factioncode, cminpoints, cmaxpoints, chealth, csides,imgsrc"
    select_from_clauses = "Select " + select_fields + " from card"

    if      (affil is None) and (fact is None): qry_string = select_from_clauses
    elif    (affil is None) and (fact is not None): qry_string = select_from_clauses + " where faction = \"" + fact + "\""
    elif    (affil is not None) and (fact is None): qry_string = select_from_clauses + " where affiliation = \"" + affil + "\""
    else:    qry_string = select_from_clauses + " where affiliation = \"" + affil + "\" and faction = \"" + fact + "\""

    header = ["Set", "Pos", "Name", "Type", "Unique", "Rarity", "Affil", "Faction", 
              "Min<br>Cost", "Max<br>Cost", "Health", "Sides", "Img Source"]
    
    return qry_html({"header":header,"query":qry_string})

def reports(report):
    
    report_dict = {
        
         "affiliation_faction_count" :
              {"header": ["Affilliation", "Faction", "Count"],
               "query" : '''Select affiliation, faction, count(*) as count from card group by affiliation, faction'''},
         "high_cost" :
              {"header": ["Set", "Pos", "Name", "Type", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
               "query": '''Select cardsetcode, position, name, typename, isunique, raritycode, ccost, csides, imgsrc
                                        from card where ccost is not null 
                                        order by ccost desc'''},
         "legendary": 
           {"header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
            "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, ccost, csides, imgsrc 
                                        from card where rarity = "Legendary"''' 
           },
         "rare": 
           {"header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
            "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, ccost, csides, imgsrc 
                                        from card where rarity = "Rare"'''
           },
         "rarity_count":
              {"header": ["Rarity", "Count"],
                "query" : '''Select rarity, count(*) as count from card group by rarity'''},
         "set_count": 
                {"header": ["Set", "Count"], 
                 "query":  '''Select cardset, count(*) as count from card group by cardset'''},
         "type_character":
                {"header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "MinPoints", "MaxPoints", "Health", "Sides", "Image"], 
                 "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, cminpoints, cmaxpoints, chealth, csides,
                              imgsrc from card where typename = "Character"'''},
         "villain_command_compatible" :
              {"header": ["Set","Pos","Name","Type","Affilliation","Faction","Is Unique","Rarity","Cost","Sides","Image"],
               "query" : '''Select cardsetcode, position, name, typename, affiliation,
                            factioncode, isunique, raritycode, ccost, csides, imgsrc
                            from card
                            where (affiliation = "Villain" or affiliation = "Neutral" )
                            and (faction = "Command" or faction = "General")'''}
        
        }
    if report in report_dict:
        return qry_html(report_dict[report])
    else:
        return "<HTML><HEAD></HEAD><BODY>Invalid report name</BODY>"
        
    
    
