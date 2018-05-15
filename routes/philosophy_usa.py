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
              <tr><td>Philosophy Degrees Completed by Award Level</td><td><a href="/philosophy/reports/awlevel_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by Institution</td><td><a href="/philosophy/reports/inst_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by State</td><td><a href="/philosophy/reports/state_count">HTML</a></td></tr>
              <tr><td>Philosophy Degrees Completed by Subject Classification</td><td><a href="/philosophy/reports/cip_count">HTML</a></td></tr>
            </tbody>
          </table>
        </div>
      </body>
    </html>
           '''

report_template = '''
<!DOCTYPE html>
<html lang="en">
  <head>
  <title>Philosophy USA</title>
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
  <table id = 'id_result_table'>
    <thead>
      <tr>{{#header}}<th>{{{.}}}</th>{{/header}}</tr>
    </thead>
    <tbody>
      {{#results}}
      <tr>{{#result}}<td>{{{.}}}</td>{{/result}}</tr>
      {{/results}}
    </tbody>
  </table>
</body>
</html>
'''

def qry_html(qry_dict):
        conn = sqlite3.connect('./resources/philosophy-usa.db')
        c = conn.cursor()
        c.execute(qry_dict["query"])
        all_results = c.fetchall()
        all_results = list(map(lambda x: {"result": x}, all_results))
        header = qry_dict["header"]
        all_results = {"header":header, "results": all_results}
        return pystache.render(report_template,all_results)

def reports(report):
    
    report_dict = {
        
         "state_count" :
              {"header": ["State", "Count"],
               "query" : '''Select stabbr, count(*) as count 
                            from completion cmp 
                            join institution ins on cmp.inst = ins.unitid
                            group by stabbr
                            order by count(*) DESC'''},
         "inst_count" :
              {"header": ["Institution", "Count"], 
               "query": '''Select instnm, count(*) as count 
                           from completion cmp 
                           join institution ins on cmp.inst = ins.unitid
                           group by instnm
                           order by count(*) DESC'''},
         "cip_count": 
           {"header" : ["CIP Code", "CIP Title", "Count"], 
            "query" : '''Select cipcode, ciptitle, count(*) as count 
                         from completion cmp 
                         join cipcode chp on cmp.cip = chp.cipcode
                         group by cipcode, ciptitle
                         order by count(*) DESC''' 
           },
         "awlevel_count": 
           {"header" : ["Code", "Level", "Count"], 
            "query" : '''Select alcode, alvalue, Count(*) 
                         from alcode join completion
                         on alcode.alcode = completion.awlevel
                         group by alcode, alvalue'''
           }
         }
    if report in report_dict:
        return qry_html(report_dict[report])
    else:
        return "<HTML><HEAD></HEAD><BODY>Invalid report name</BODY>"
