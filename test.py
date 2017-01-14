from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    consumer=input("What is your name? ")
    return "Hello " + consumer

if __name__ == "__main__":
    app.run(port=5000)
