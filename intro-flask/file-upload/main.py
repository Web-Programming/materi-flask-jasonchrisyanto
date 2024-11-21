from flask import Flask, jsonify,request 
import os # Diperlukan untuk menyimpan file
import time # Diperlukan untuk membuat timestamp

UPLOAD_FOLDER = 'static/uploads'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return 'File Upload Demo'

@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        # Cek jika ada file yang diunggah
        foto = request.files['foto']
        if foto:
            # Mengambil timestamp saat ini untuk menambahkan ke nama file
            timestamp = str(int(time.time()))
            # Mengambil ekstensi file asli
            ext = foto.filename.split('.')[-1]
            # Menambahkan ekstensi ke nama file unik
            unique_filename = f"{timestamp}.{ext}"
            # Menyimpan file dengan nama unik
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            foto.save(foto_path)
            # Menyimpan path relatif
            foto_path = f'uploads/{unique_filename}' 
            data = { 
                "status" : "success", 
                "message" : "File Uploaded", 
            } 
            return jsonify(data) 
        else:
            foto_path = None
            data = { 
                "status" : "failed", 
                "message" : "File upload failed", 
            } 
            return jsonify(data) 
    
    # JSON empty
    data = { 
        "status" : "success", 
        "message" : "Pick a foto to upload", 
    } 
    return jsonify(data) 

#tambahkan dependensi Flask-RESTful
#pip install Flask-RESTful
    
# keep this as is
if __name__ == '__main__':
    app.run(debug=True)