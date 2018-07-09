from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "hello"

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filebuf = request.files.get("file")
        if filebuf is None:
            return redirect(request.url)
        elif filebuf.filename.lower().endswith('.eml'):
            btxt = filebuf.read()
            txt = btxt.decode("iso2022_jp")
            return txt
        else:
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload></p>
    </form>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
