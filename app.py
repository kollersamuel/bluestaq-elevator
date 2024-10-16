from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Elevator is Online"

if __name__ == '__main__':
    app.run(debug=True)