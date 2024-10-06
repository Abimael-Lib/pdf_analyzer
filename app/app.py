from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader
import logging
from collections import Counter
import re  # Para limpiar el texto

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Define la carpeta de subida
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Definir archivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal para subir el pdf
@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # Verificar si se envió el archivo
        if 'file' not in request.files:
            return 'No hay archivo'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No se ha seleccionado un pdf'
        
        # Verifica que sea un archivo pdf
        if file and allowed_file(file.filename):
            try:
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                app.logger.info(f"Archivo guardado en: {filename}")
                return redirect(url_for('extract_text_from_pdf', filename=file.filename))
            except Exception as e:
                app.logger.error(f"Error al guardar el archivo: {str(e)}")
                return f"Error al guardar el archivo: {str(e)}"
        else:
            return "Tipo de archivo no permitido"
    
    return render_template('upload.html')

# Función para analizar el pdf y contar palabras
@app.route('/analyze/<filename>')
def extract_text_from_pdf(filename):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Limpiar el texto y contar las palabras
        words = re.findall(r'\b\w+\b', text.lower())  # Encontrar palabras ignorando mayúsculas
        
        # Filtrar números y letras sueltas (a, i, etc.)
        filtered_words = [word for word in words if len(word) > 1 and not word.isdigit()]
        
        word_count = Counter(filtered_words)

        return render_template('analyze.html', text=text, word_count=word_count.most_common())
    except Exception as e:
        app.logger.error(f"Error al analizar el PDF: {str(e)}")
        return f"Error al analizar el PDF: {str(e)}"

# Inicializar la app
if __name__ == '__main__':
    app.run(debug=True)

