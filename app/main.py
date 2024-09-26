from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define la carpeta de subida
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica si la carpeta de subida existe, si no, la crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si hay un archivo en la solicitud
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    # Verifica si se seleccionó un archivo
    if file.filename == '':
        return redirect(request.url)
    
    # Guarda el archivo si es un PDF
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f'Archivo {file.filename} subido correctamente'
    else:
        return 'Solo se permiten archivos PDF', 400

if __name__ == '__main__':
    app.run(debug=True)


