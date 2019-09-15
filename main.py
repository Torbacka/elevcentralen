from flask import Flask

app = Flask(__name__)


def get():
    print("hej")


@app.route('/', methods=['GET'])
def local_get():
    get()
    return ''


if __name__ == '__main__':
    app.run('127.0.0.1', port=8087, debug=True)
