import sqlite3,pystache
from flask import request

def root():
    types = ["Unit", "Champion", "Spell", "Blessing", "Ability"]
    return pystache.render(root_template, {"types" : types})

root_template = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Warhammer Champions</title>
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
      <h1>Warhammer Champions</h1>
      <br>
    </div>
    <div id="cards">

      <h4>Cards</h4>

      <table>

        <thead>

          <tr>

            <th></th>

            <th></th>

            <th colspan="6">Alliance</th>

          </tr>

          <tr>

            <th></th>

            <th></th>

            <th scope="col">All</th>

            <th scope="col">Any</th>

            <th scope="col">Chaos</th>

            <th scope="col">Death</th>

            <th scope="col">Destruction</th>

            <th scope="col">Order</th>

          </tr>

        </thead>

        <tbody>

          <tr>

            <th rowspan="6">Type</th>

            <th scope="row">All</th>

            <td><a href="/wh_champions/cards?">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Any">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Chaos">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Death">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Destruction">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Order">HTML</a></td>

          </tr>

          {{#types}}

          <tr>

            <th scope="row">{{.}}</th>

            <td><a href="/wh_champions/cards?type={{.}}">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Any&amp;type={{.}}">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Chaos&amp;type={{.}}">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Death&amp;type={{.}}">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Destruction&amp;type={{.}}">HTML</a></td>

            <td><a href="/wh_champions/cards?ally=Order&amp;type={{.}}">HTML</a></td>

          </tr>

          {{/types}}

        </tbody>

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
      <h3>{{title}}</h3>
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
        conn = sqlite3.connect('./resources/wh_champions.db')
        c = conn.cursor()
        c.execute(qry_dict["query"])
        all_results = c.fetchall()
        all_results = list(map(lambda x: {"result": html_for_result(x)}, all_results))
        header = qry_dict["header"]
        title = qry_dict["title"]
        all_results = {"title": title, "header":header, "results": all_results}
        return pystache.render(report_template,all_results)

def cards():
    ally = request.args.get("ally")
    ctype =  request.args.get("type")
    select_fields = "setName, cardNumber, alliance, category,class, name, rarity"
    select_from_clauses = "Select " + select_fields + " from card"
    order_by_clause = " order by setNum, cardNumber"
    if      (ally is None) and (ctype is None): qry_string = select_from_clauses + order_by_clause
    elif    (ally is None) and (ctype is not None): qry_string = select_from_clauses + " where category = \"" + ctype + "\"" + order_by_clause
    elif    (ally is not None) and (ctype is None): qry_string = select_from_clauses + " where alliance = \"" + ally + "\"" + order_by_clause
    else:    qry_string = select_from_clauses + " where alliance = \"" + ally + "\" and category = \"" + ctype + "\"" + order_by_clause

    header = ["Set", "Number", "Alliance", "Type","Class", "Name", "Rarity"]

    title = "{} {} Cards".format((ally or ""), (ctype or ""))
    
    return qry_html({"title" : title, "header":header,"query":qry_string})
