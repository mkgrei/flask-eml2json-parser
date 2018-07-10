from flask import Flask, jsonify, request, redirect, session, url_for
import process
app = Flask(__name__)
app.secret_key = b'not_so_secret.predictable'

@app.route("/")
def hello():
    return "hello"

@app.route("/show")
def show():
    if 'content' not in session:
        redirect(url_for('upload'))
    else:
        txt = session['content']
        ret = process.to_json(txt)
        print(ret)
        return "<pre>" + ret + "</pre>"

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filebuf = request.files.to_dict(flat=False)
        if filebuf is None:
            return redirect(request.url)
        else:
            filename = list(filebuf.keys())[0]
            filebuf = filebuf[filename][0]
            if filebuf.filename.lower().endswith('.eml'):
                btxt = filebuf.read()
                txt = btxt.decode("iso2022_jp")
                session['content'] = txt
                return redirect(url_for('show'), code=303)
            return redirect(request.url)
    return '''
    <!doctype html>
    <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload></p>
    </form>
    <style>
    .droparea {
        width: 200px;
        height: 200px;
        border-style: solid;
        border-width: 3px;
        border-color: red;
        float: left;
        line-height: 200px;
        text-align: center;
    }
    </style>
    <div class="container">
        <div class="droparea">Drop Here</div>
        <div class="tablearea" id="tablearea"></div>
    </div>
    <div class="result" id="result">
    </div>
    <script>
    var dragHandler = function(evt){
        evt.preventDefault();
    };

    var dropHandler = function(evt){
        evt.preventDefault();
        var files = evt.originalEvent.dataTransfer.files;
        var file = files[0];
        var formData = new FormData();
        formData.append('file', file);
        var postData = {
            url : "/upload",
            type : "POST",
            dataType : "file",
            data : formData,
            contentType : false,
            processData : false,
        };
        $.ajax(
            postData
        ).done(function(text) {
            console.log(text);
        });
        <!--
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload/', true);
        xhr.onload = function (e) {  };
        xhr.send(formData);
        -->
    };

    var dropHandlerSet = {
        dragover: dragHandler,
        drop: dropHandler
    };

    $(".droparea").on(dropHandlerSet);
    </script>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
