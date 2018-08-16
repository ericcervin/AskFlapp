import sqlite3,pystache
from flask import request

def root():
    report_list = list(map(lambda x : {"key" : x[0], "text" : x[1]["title"]}, report_dict.items()))
    report_list = sorted(report_list,key = lambda x: x["text"])
    return pystache.render(root_template, report_list)

root_template = '''
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
       {{#.}}
       <tr><td>{{text}}</td><td><a href=\"/discogs/reports/{{key}}\">HTML</a></td></tr>
        {{/.}}
        </table></div></body></html>'''

discogs_report_template = '''
      <!DOCTYPE html>
      <html lang="en">
        <head>
        <title>{{title}}</title>
          <style> table,th,td {
                  border: 1px solid black;
                  border-collapse: collapse;
                  padding: 3px;
                  text-align: center;}
                  td {text-align: left}
          </style>
       </head>
       <body>
         <div id="report">
         <h3>{{title}}</h3>
         <table id="id_release_table">
           <thead><tr>{{#header}}<th>{{.}}</th>{{/header}}</tr></thead>
           <tbody>
           {{#results}}
            <tr>{{#result}}<td>{{.}}</td>{{/result}}</tr>
            {{/results}}
           </tbody>
         </table>
       </body>
     </html>'''

def qry_html(qry_dict):
        conn = sqlite3.connect('./resources/discogs.db')
        c = conn.cursor()
        c.execute(qry_dict["query"])
        all_results = c.fetchall()
        all_results = list(map(lambda x: {"result": x}, all_results))
        title = qry_dict["title"]
        header = qry_dict["header"]
        all_results = {"title": title, "header":header, "results": all_results}
        return pystache.render(discogs_report_template,all_results)
   
def releases():
    sort = request.args.get("sort","artist")
    select_fields = "title, artist, label, year"
    select_from_clauses = "Select " + select_fields + " from release"

    if (sort is None) : qry_string = select_from_clauses
    else:    qry_string = select_from_clauses + " order by \"" + sort + "\""

    header = ["Title", "Artist", "Label", "Release Year"]
    title = "Releases by {}".format(sort.title()) 
    return qry_html({"title": title, "header":header,"query":qry_string})

report_dict =  {
          "artist_count" : 
             {"title" : "Count by Artist",
              "header" : ["Artist", "Count"], 
              "query" : "Select artist, count(*) as count from release group by artist order by count(*) DESC"},
          "label_count" :
             {"title" : "Count by Label",
              "header" : ["Label", "Count"], 
              "query" : "Select label, count(*) as count from release group by label order by count(*) DESC"},
          "year_count" :
             {"title" : "Count by Release Year",
              "header" : ["Year Released", "Count"], 
              "query"  : "Select year, count(*) as count from release group by year order by count(*) DESC"},
          "year_month_added" :
             {"title" : "Count by Year/Month Added",
              "header" : ["Year Added", "Month Added", "Count"],
              "query" :  '''Select substr(dateadded,0,5), substr(dateadded,6,2), Count(*) 
                            from release group by substr(dateadded,0,5), substr(dateadded,6,2)
                            order by substr(dateadded,0,5) DESC, substr(dateadded,6,2) DESC'''}
                  }


def reports(report):
     if report in report_dict:
        return qry_html(report_dict[report])
     else:
        return "<HTML><HEAD></HEAD><BODY>Invalid report name</BODY>"
