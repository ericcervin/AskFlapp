import sqlite3,pystache
from flask import request

def root():
    report_list = list(map(lambda x : {"key" : x[0], "text" : x[1]["title"]}, report_dict.items()))
    report_list = sorted(report_list,key = lambda x: x["text"])
    return pystache.render(root_template, report_list)


root_template = '''<!DOCTYPE html>
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
          <tr>
            <th></th>
            <th></th>
            <th colspan="4">Affiliation</th>
          </tr>
          <tr>
            <th></th>
            <th></th>
           <th scope="col">All</th>
           <th scope="col">Villain</th>
           <th scope="col">Hero</th>
           <th scope="col">Neutral</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th rowspan="5">Faction</th>
            <th scope="row">All</th>
            <td><a href="/destiny/cards?">HTML</a></td>
            <td><a href="/destiny/cards?affil=Villain">HTML</a></td>
            <td><a href="/destiny/cards?affil=Hero">HTML</a></td>
            <td><a href="/destiny/cards?affil=Neutral">HTML</a></td>
          </tr>
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
        {{#.}}
        <tr><td>{{text}}</td><td><a href=\"/destiny/reports/{{key}}\">HTML</a></td></tr>
        {{/.}}
      </table>
    </div>
  </body>
</html>'''

report_template = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{{title}}</title>
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
  <body>
    <div id="report">
      <h3>{{title}}<h3>
      <table id = \"id_card_table\">
        <thead>
          <tr>{{#header}}<th>{{{.}}}</th>{{/header}}</tr>
        </thead>
        <tbody>
          {{#results}}
          <tr>{{#result}}<td>{{{.}}}</td>{{/result}}</tr>
          {{/results}}
        </tbody>
      </table>
    </div>  
  </body>
</html>'''

def html_for_http(cl):
  if isinstance(cl, str) == True:
   if "http" in cl:
       cl = "<A HREF = \"" + cl + "\">" + cl + "</A>"
  if cl is None:
      cl = ""
  return cl

def html_for_result(res):
    return list(map(html_for_http, res))

def qry_html(qry_dict):
        conn = sqlite3.connect('./resources/destiny.db')
        c = conn.cursor()
        c.execute(qry_dict["query"])
        all_results = c.fetchall()
        all_results = list(map(lambda x: {"result": html_for_result(x)}, all_results))
        header = qry_dict["header"]
        title = qry_dict["title"]
        all_results = {"title": title, "header":header, "results": all_results}
        return pystache.render(report_template,all_results)
    
def cards():
    affil = request.args.get("affil")
    fact =  request.args.get("fact")
    select_fields = "cardsetcode, position, name, typename, isunique, raritycode, affiliation, factioncode, cminpoints, cmaxpoints, chealth, ccost, csides,imgsrc"
    select_from_clauses = "Select " + select_fields + " from card"

    if      (affil is None) and (fact is None): qry_string = select_from_clauses
    elif    (affil is None) and (fact is not None): qry_string = select_from_clauses + " where faction = \"" + fact + "\""
    elif    (affil is not None) and (fact is None): qry_string = select_from_clauses + " where affiliation = \"" + affil + "\""
    else:    qry_string = select_from_clauses + " where affiliation = \"" + affil + "\" and faction = \"" + fact + "\""

    header = ["Set", "Pos", "Name", "Type", "Unique", "Rarity", "Affil", "Faction", 
              "Min<br>Points", "Max<br>Points", "Health", "Cost", "Sides", "Img Source"]

    title = "{} {} Cards".format((affil or ""), (fact or ""))
    
    return qry_html({"title" : title, "header":header,"query":qry_string})

report_dict = {
        
         "affiliation_faction_count" :
              {"title" : "Count by Affiliation/Faction",
               "header" : ["Affilliation", "Faction", "Count"],
               "query" : '''Select affiliation, faction, count(*) as count from card group by affiliation, faction'''},
         "high_cost" :
              {"title" : "Highest Cost Support/Event/Upgrade",
               "header" : ["Set", "Pos", "Name", "Type", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
               "query" : '''Select cardsetcode, position, name, typename, isunique, raritycode, ccost, csides, imgsrc
                                        from card where ccost is not null 
                                        order by ccost desc'''},
         "legendary" : 
           {"title" : "Rarity Legendary Cards",
            "header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
            "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, ccost, csides, imgsrc 
                                        from card where rarity = "Legendary"''' 
            },
         "odd_cost" :
            {"title" : "Odd Cost Support/Event/Upgrade",
             "header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"],
             "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, ccost, csides, imgsrc
                        from card where ccost IN (1,3,5)'''},
         "rare" : 
           {"title" : "Rarity Rare Cards",
            "header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
            "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, ccost, csides, imgsrc 
                                        from card where rarity = "Rare"'''
           },
         "rarity_count":
              {"title" : "Count by Rarity",
               "header": ["Rarity", "Count"],
               "query" : '''Select rarity, count(*) as count from card group by rarity'''},
         "set_affiliation_faction_dice_count":
                {"title" : "Count by Set/Affiliation/Faction (cards with dice)",
                 "header": ["Set", "Affilliation", "Faction", "Dice Count"], 
                 "query":  '''Select cardset, affiliation, faction, count(*) as count 
                              from card
                              where csides IS NOT NULL
                              group by cardset, affiliation, faction'''},
         "set_count": 
                {"title" : "Count by Set",
                 "header": ["Set", "Count"], 
                 "query":  '''Select cardset, count(*) as count from card group by cardset'''},
         "type_character":
                {"title" : "Type Character Cards",
                 "header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "MinPoints", "MaxPoints", "Health", "Sides", "Image"], 
                 "query" : '''Select cardsetcode, position, name, typename, affiliation, factioncode, isunique, raritycode, cminpoints, cmaxpoints, chealth, csides,
                              imgsrc from card where typename = "Character"'''},
         "type_upgrade":
                {"title" : "Type Upgrade Cards",
                 "header" : ["Set", "Pos", "Name", "Type", "Affilliation", "Faction", "Is Unique", "Rarity", "Cost", "Sides", "Image"], 
                 "query" : '''Select cardsetcode, position, name, typename, affiliation, faction, isunique, raritycode, ccost, csides, imgsrc 
                  from card where typename = "Upgrade"'''},
         "villain_command_compatible" :
              {"title" : "Compatible with Villains, Command",
               "header": ["Set","Pos","Name","Type","Affilliation","Faction","Is Unique","Rarity","Cost","Sides","Image"],
               "query" : '''Select cardsetcode, position, name, typename, affiliation,
                            factioncode, isunique, raritycode, ccost, csides, imgsrc
                            from card
                            where (affiliation = "Villain" or affiliation = "Neutral" )
                            and (faction = "Command" or faction = "General")'''}
        
        }


def reports(report):
    
    if report in report_dict:
        return qry_html(report_dict[report])
    else:
        return "<HTML><HEAD></HEAD><BODY>Invalid report name</BODY>"
        
    
    
