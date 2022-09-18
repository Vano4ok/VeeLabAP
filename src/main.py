from flask import Flask
from waitress import serve

app = Flask('__name__')


@app.route('/api/v1/hello-world-19')
def hello_world():
    return "Hello World 19"


if __name__ == '__main__':
    app.run(debug=True)

serve(app)
