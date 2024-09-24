from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configura donde se guardara el pdf al subirlo
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    
    file.save(f"{app.config['UPLOAD_FOLDER']}/{file.filename}")

    return 'Archivo subido y cargado correctamente'


if __name__ == '__main__':
    app.run(debug=True)

