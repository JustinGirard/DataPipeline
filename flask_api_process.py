from flask import Flask,request
app = Flask(__name__)
import sys
sys.path.append('../')

@app.route("/", methods=['GET', 'POST'])
def handle():
    if request.method == 'POST': #this block is only entered when the form is submitted
        try:
            language = request.form.get('language')
            req = dict(request.form)
            import APIRequest
            import json
            return APIRequest.APIRequest.submit_remote(req)
        except:
            import traceback as tb
            return json.dumps({'error':tb.format_exc()})
        
        
        
    return "APIQueries works"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host ='0.0.0.0') #run ap