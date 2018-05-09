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
            <title>Powerball</title>
            </head>
            <body>
            <div id="header">
            <h1>Powerball</h1>
            <p>Two sets of Powerball numbers</p>
            </div>
            <div id="numbers">
            <table>
            <thead>
            <tr><th scope="col">Numbers</th></tr>
            </thead>
            <tbody>
            <tr><td><a href="/powerball/html">HTML</a></td></tr>
            </tbody>
            </table>
            </div>
            </body>
            </html>'''

html_res_template = '''
                    <!DOCTYPE html>
                    <html lang=\"en\">
                    <head>
                    <style>table,th,td {
                    border: 1px solid black;
                    border-collapse: collapse;
                    padding: 3px;
                    text-align: center
                    }
                    td {text-align: left}
                   </style>
                   <title>Powerball</title>
                   </head>
                   <body>
                   <table>
                   <tr><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>pb</th></tr>
                   <tr><td>{{row_1.ball_1}}</td><td>{{row_1.ball_2}}</td><td>{{row_1.ball_3}}</td><td>{{row_1.ball_4}}</td><td>{{row_1.ball_5}}</td><td>{{row_1.pb}}</td></tr>
                   <tr><td>{{row_2.ball_1}}</td><td>{{row_2.ball_2}}</td><td>{{row_2.ball_3}}</td><td>{{row_2.ball_4}}</td><td>{{row_2.ball_5}}</td><td>{{row_2.pb}}</td></tr>
                   </table>
                   </body>
                   </html>
                    '''
def powerball_row_map():
    white_balls = list(range(1,70))
    random.shuffle(white_balls)
    row_dict = dict(zip(["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"], white_balls))
    row_dict["pb"] = random.randint(1,26)
    return row_dict

def res_html():
    output_map = {"row_1" : powerball_row_map(),"row_2" : powerball_row_map()}
    return pystache.render(html_res_template,output_map)
