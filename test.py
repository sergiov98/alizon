from flask import Flask
app = Flask(__name__)

@app.route('/result/<item>')
def getMatchingItem(item):
    #Daniil and Winson's code
    matchedItem = "url" + " price"
    return matchedItem



if __name__ == "__main__":
    app.run(port=5000)
