from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>Flask App with requests and BeautifulSoup!</h1>
    <p>Your packages are installed and ready to use:</p>
    <ul>
        <li>✅ Flask - for web framework</li>
        <li>✅ requests - for HTTP requests</li>
        <li>✅ beautifulsoup4 - for HTML parsing</li>
    </ul>
    <p>Ready to build something amazing!</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)