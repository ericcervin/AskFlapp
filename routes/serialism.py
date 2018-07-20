import pystache, random
from flask import request

serialism_root_template = '''
   <!DOCTYPE html>  
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
              <tr><th scope="col">Basic Rows</th><th scope="col">Square</th></tr>
            </thead>
            <tbody>
              <tr><td><a href="/serialism/rows/html">HTML</a></td>
                  <td><a href="/serialism/square/html">HTML</a></td>
              </tr>
            </tbody>
          </table>
        </div>
      </body>
    </html>

'''


serialism_row_template = '''
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

serialism_square_template = '''
  <!DOCTYPE html>
  <html lang="en">
    <head>  
      <style> table,th,td {
         border: 1px solid black;
         border-collapse: collapse;
         padding: 3px;
         text-align: center;}
         td {text-align: left;
             width: 20px}
      </style>
      <title>Serialism</title>
    </head>
    <body>
      <p>(t = ten. e = eleven.)</p>
      <table>
        <tbody>
          {{#sq}}
          <tr>
          {{#vl}}
          <td>{{.}}</td>
          {{/vl}}
          </tr>
          {{/sq}}
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
    if pc < 0: pc +=  12
    elif pc > 12: pc -= 12
    elif pc == 12: pc = 0
    return pc

def transpose(pc, i):
    return absolute_pitch_class(pc + i)

def transpose_row(rw,i):
    return [transpose(x,i) for x in rw]

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

def serial_square(rw):
    square = []
    for i in rw:
        transposed_row = transpose_row(rw,12 - i)
        square.append({"vl" : [add_e_and_t(n) for n in transposed_row]})
    return square
        
def serialism_dict():
    start = shift_to_zero(random_dodeca_row());
    
    p0 = []; p0.extend(start); p0 = [add_e_and_t(n) for n in p0] 

    r0 = []; r0.extend(start); r0.reverse(); r0 = [add_e_and_t(n) for n in r0]

    i0 = []; i0.extend(start); i0 = [invert(n) for n in i0]; i0 = [add_e_and_t(n) for n in i0]

    ri0 = []; ri0.extend(i0); ri0.reverse(); ri0 = [add_e_and_t(n) for n in ri0]

    sq = serial_square(start)
    
    return {"p0": p0,"r0" : r0, "i0" : i0, "ri0" : ri0, "sq" : sq}

def root():
    return pystache.render(serialism_root_template)
           
def res_row_html():
    return pystache.render(serialism_row_template,serialism_dict())

def res_square_html():
    return pystache.render(serialism_square_template,serialism_dict())
