import pystache, random
from flask import request

def root():
    return '''<!DOCTYPE html>
            <html lang="en">
            <head>
            <style>
            table,th,td {
              border: 1px solid black;
              border-collapse: collapse;
              padding: 3px;
              text-align: center
            }
              td {text-align: left}
            </style>
            <title>Serialism</title>
            </head>
            <body>
            <div id="header">
            <h1>Serialism</h1>
            <p>Rows and rows of pitch classes</p>
            </div>
            <div id="pcs">
            <table>
            <thead>
            <tr><th scope="col">Basic Rows</th></tr>
            </thead>
            <tbody>
            <tr><td><a href="/serialism/html">HTML</a></td></tr>
            </tbody>
            </table>
            </div>
            </body>
            </html>'''

serialism_result_template = '''
  <!DOCTYPE html>
  <html lang="en">
    <head>  
      <style> table,th,td {
         border: 1px solid black;
         border-collapse: collapse;
         padding: 3px;
         text-align: center;}
         td {text-align: left}
      </style>
      <title>Serialism</title>
    </head>
    <body>
      <p>(t = ten. e = eleven.)</p>
      <table>
        <tbody>
          <tr><th>P0</th>{{#p0}}<td>{{.}}</td>{{/p0}}</tr>
          <tr><th>R0</th>{{#r0}}<td>{{.}}</td>{{/r0}}</tr>
          <tr><th>I0</th>{{#i0}}<td>{{.}}</td>{{/i0}}</tr>
          <tr><th>RI0</th>{{#ri0}}<td>{{.}}</td>{{/ri0}}</tr>
        </tbody>
      </table>
    </body>
  </html>
  '''

def random_dodeca_row():
    rw = list(range(12))
    random.shuffle(rw)
    return rw

def absolute_pitch_class(pc):
    if pc < 0:
        pc +=  12
    return pc

def shift_to_zero(rw):

     or0 = rw[0]

     rw =  [num - or0 for num in rw]
     rw =  [absolute_pitch_class(num) for num in rw]
     return rw

def invert(n):
    if n != 0:
        n = 12 - n
    return n

def add_e_and_t(n):
    if n == 10:
        return "t"
    elif n == 11:
        return "e"
    else:
        return n
    
           
def res_html():
    start = shift_to_zero(random_dodeca_row());
    
    p0 = []; p0.extend(start); p0 = [add_e_and_t(n) for n in p0] 

    r0 = []; r0.extend(start); r0.reverse(); r0 = [add_e_and_t(n) for n in r0]

    i0 = []; i0.extend(start); i0 = [invert(n) for n in i0]; i0 = [add_e_and_t(n) for n in i0]

    ri0 = []; ri0.extend(i0); ri0.reverse(); ri0 = [add_e_and_t(n) for n in ri0]
    
    return pystache.render(serialism_result_template,{"p0": p0,"r0" : r0, "i0" : i0, "ri0" : ri0})
