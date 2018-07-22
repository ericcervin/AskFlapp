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
    <form action="/gematria/search" method="get">
    <input id="id_word_input" name="word" type="text">
    <input type="submit" value="Calculate"></form>
    </div>
    <div id="value_form">
    <p>Search the 10,000 most common English words by numerical value.</p>
    <form action="/gematria/search" method="get">
    <input id="id_value_input" name="value" type="text">
    <input type="submit" value="Search">
    </form>
    </div>
    </body>
    </html>'''

gematria_word_template = '''
 
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
                 td {text-align: left}
      </style></head>
      <body>
      <div id="header">
      <table id = 'id_word_value_table'>
      <tr>{{#wrd_list}}<th>{{.}}</th>{{/wrd_list}}</tr>
      <tr>{{#wrd_result}}<td>{{.}}</td>{{/wrd_result}}</tr></table>
  </div>
  <br><br>
  <div id="etc">
  <p>Others with same value</p>
  <br>
  <table id = 'id_other_word_table'>
  <tr><th>Word</th><th>Value</th></tr>
   {{#other_results}}
   <tr>{{#result}}<td>{{.}}</td>{{/result}}</tr>
   {{/other_results}}
  </table>
  </div>
  </body>
  </html>
'''

gematria_value_template = '''
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
                 td {text-align: left}
      </style>
      </head>
      <body>
      <table id = 'id_word_value_table'>
      <tr>
      <th>Word</th><th>Value</th></tr>
      {{#results}}
      <tr>{{#result}}<td>{{.}}</td>{{/result}}</tr>
      {{/results}}
      </table>
      </body>
      </html>'''


def calculate_word_value(wrd):
    values = [ord(i) - 96 for i in wrd.lower()]
    value_pairs = [[i,ord(i)-96] for i in wrd.lower()]
    total_value = 0
    for i in values:
        total_value += i
    value_map = {"word" : wrd,
                 "values" : values,
                 "value_pairs" : value_pairs,
                 "total_value" : total_value}
    return value_map

def query_table(query):
    conn = sqlite3.connect('./resources/gematria.db')
    c = conn.cursor()
    c.execute(query)
    all_results = c.fetchall()
    all_results = list(map(lambda x: {"result": x}, all_results))
    return all_results

def search():
    if "word" in request.args:
        return words()
    elif "value" in request.args:
        return values()
    else: return ""

def words():
    word = request.args.get("word")
    word = word.lower()
    
    wrd_map = calculate_word_value(word)


    word_result = wrd_map["values"]
    word_result.append(wrd_map["total_value"])


    word_list = list(word)
    word_list.append("total")

    query = "Select word, wordvalue from gematria where wordvalue = \"" + str(wrd_map["total_value"]) + "\" and word != \"" + str(wrd_map["word"]) + "\" order by word"
    other_results = query_table(query)
    
    output_map = {"wrd_list" : word_list,

                  "wrd_result" : word_result,
                  "other_results" : other_results}


    return pystache.render(gematria_word_template,output_map)
    
def values():
    value = request.args.get("value")

    query = "Select word, wordvalue from gematria where wordvalue = \"" + str(value) + "\" order by word"
    results = query_table(query)
    output_map = {"results" : results} 

    return pystache.render(gematria_value_template,output_map)
