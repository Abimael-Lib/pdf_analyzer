from flask import Flask, render_template, request, redirect, url_for
import os
import pdfplumber

app = Flask(__name__)

# Define la carpeta de subida
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


# Definir archivo permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal para subir el pdf
@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # Veficar si se envio el archivo
        if 'file' in request.files:    
            return 'No hay archivo'
    
        file = request.files['file']
    
        if file.filename == '':
            return 'No se ha seleccionado un pdf'
    
        
        # Verifica que sea un archivo pdf
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return redirect(url_for('analyze_pdf', filename = file.filename))
    
    return render_template('upload.html')
    


# Funcion para analizar el pdf
@app.route('analyze/filename')
def analyze_pdf(filename):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
            
    return render_template('analyze.html', text = text)


    

# Inicializar la app
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config('UPLOAD_FOLDER'))

    app.run(debug=True)





















