from app import db
class Fakultas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    prodis = db.relationship('Prodi', backref='fakultas', lazy=True)
    def __repr__(self):
        return f"Fakultas('{self.id}', '{self.nama}')"
    
class Prodi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    fakultas_id = db.Column(db.Integer, db.ForeignKey('fakultas.id'), nullable=False)
    mahasiswas = db.relationship('Mahasiswa', back_populates='prodi', lazy=True)
    def __repr__(self):
        return f"Prodi('{self.id}', '{self.nama}', '{self.fakultas_id}')"
    
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    prodi_id = db.Column(db.Integer, db.ForeignKey('prodi.id'), nullable=False)
    prodi = db.relationship('Prodi', back_populates='mahasiswas')
    def __repr__(self):
        return f"Mahasiswa('{self.id}', '{self.nama}', '{self.nim}')"
