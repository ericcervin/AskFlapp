from flask import Flask,Response
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

@app.route('/user/<name>')
def user(name):
    return "<h1>Hello, %s</h1>" % name

@app.route('/robots.txt')
def robots():
    return Response('User-agent: *\nDisallow: /',mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
