from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return "Yes"	
	
if __name__ == '__main__':
    app.run(debug=True)
