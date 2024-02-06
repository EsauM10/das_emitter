from flask import Flask, request

from api.controllers import GeneratePDFController

app = Flask(__name__)

@app.route('/pdf', methods=['POST'])
def generate_das_pdf():
    return GeneratePDFController().handle(request)
    

if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=8000, debug=False)
    