from sqlalchemy.orm import joinedload
from flask import request, jsonify
from app import app, db
from models import Fakultas, Prodi, Mahasiswa

# Route GET untuk Fakultas
@app.route('/api/fakultas', methods=['GET'])
def get_fakultas():
    fakultas = Fakultas.query.all()
    output = []
    for fac in fakultas:
        prodi_list = [{'id': prodi.id, 'nama': prodi.nama} for prodi in fac.prodis]
        output.append({
            'id': fac.id,
            'nama': fac.nama,
            'prodi': prodi_list
        })
    return jsonify(output)

# Route POST untuk Fakultas
@app.route('/api/fakultas', methods=['POST'])
def add_fakultas():
    data = request.get_json()
    if 'nama' not in data:
        return jsonify({'message': 'Nama fakultas diperlukan'}), 400
    fakultas = Fakultas(nama=data['nama'])
    db.session.add(fakultas)
    db.session.commit()
    return jsonify({'message': 'Fakultas berhasil ditambahkan'}), 201

# Route PUT untuk Fakultas
@app.route('/api/fakultas/<int:id>', methods=['PUT'])
def update_fakultas(id):
    fakultas = Fakultas.query.get(id)
    if not fakultas:
        return jsonify({'message': 'Fakultas tidak ditemukan'}), 404
    data = request.get_json()
    if 'nama' in data:
        fakultas.nama = data['nama']
    db.session.commit()
    return jsonify({'message': 'Fakultas berhasil diperbarui'}), 200

# Route DELETE untuk Fakultas
@app.route('/api/fakultas/<int:id>', methods=['DELETE'])
def delete_fakultas(id):
    fakultas = Fakultas.query.get(id)
    if not fakultas:
        return jsonify({'message': 'Fakultas tidak ditemukan'}), 404
    if fakultas.prodis:
        return jsonify({'message': 'Fakultas tidak bisa dihapus karena masih memiliki Prodi terkait'}), 400
    db.session.delete(fakultas)
    db.session.commit()
    return jsonify({'message': 'Fakultas berhasil dihapus'}), 200

# Route GET untuk Prodi
@app.route('/api/prodi', methods=['GET'])
def get_prodi():
    prodis = Prodi.query.options(joinedload(Prodi.fakultas)).all()
    output = []
    for prodi in prodis:
        output.append({
            'id': prodi.id,
            'nama': prodi.nama,
            'fakultas_id': prodi.fakultas_id,
            'fakultas_nama': prodi.fakultas.nama
        })
    return jsonify(output)

# Route POST untuk Prodi
@app.route('/api/prodi', methods=['POST'])
def add_prodi():
    data = request.get_json()
    if 'nama' not in data or 'fakultas_id' not in data:
        return jsonify({'message': 'Nama prodi dan fakultas_id diperlukan'}), 400
    fakultas = Fakultas.query.get(data['fakultas_id'])
    if not fakultas:
        return jsonify({'message': 'Fakultas tidak ditemukan'}), 404
    prodi = Prodi(nama=data['nama'], fakultas_id=data['fakultas_id'])
    db.session.add(prodi)
    db.session.commit()
    return jsonify({'message': 'Prodi berhasil ditambahkan'}), 201

# Route PUT untuk Prodi
@app.route('/api/prodi/<int:id>', methods=['PUT'])
def update_prodi(id):
    prodi = Prodi.query.get(id)
    if not prodi:
        return jsonify({'message': 'Prodi tidak ditemukan'}), 404
    data = request.get_json()
    if 'nama' in data:
        prodi.nama = data['nama']
    if 'fakultas_id' in data:
        fakultas = Fakultas.query.get(data['fakultas_id'])
        if not fakultas:
            return jsonify({'message': 'Fakultas tidak ditemukan'}), 404
        prodi.fakultas_id = data['fakultas_id']
    db.session.commit()
    return jsonify({'message': 'Prodi berhasil diperbarui'}), 200

# Route DELETE untuk Prodi
@app.route('/api/prodi/<int:id>', methods=['DELETE'])
def delete_prodi(id):
    prodi = Prodi.query.get(id)
    if not prodi:
        return jsonify({'message': 'Prodi tidak ditemukan'}), 404
    if prodi.mahasiswas:
        return jsonify({'message': 'Prodi tidak bisa dihapus karena masih memiliki Mahasiswa terkait'}), 400
    db.session.delete(prodi)
    db.session.commit()
    return jsonify({'message': 'Prodi berhasil dihapus'}), 200

# Route GET untuk Mahasiswa
@app.route('/api/mahasiswa', methods=['GET'])
def get_mahasiswa():
    mahasiswas = Mahasiswa.query.options(joinedload(Mahasiswa.prodi).joinedload(Prodi.fakultas)).all()
    output = []
    for mhs in mahasiswas:
        output.append({
            'id': mhs.id,
            'nama': mhs.nama,
            'nim': mhs.nim,
            'prodi_id': mhs.prodi_id,
            'prodi_nama': mhs.prodi.nama,
            'fakultas_id': mhs.prodi.fakultas_id,
            'fakultas_nama': mhs.prodi.fakultas.nama
        })
    return jsonify(output)

# Route POST untuk Mahasiswa
@app.route('/api/mahasiswa', methods=['POST'])
def add_mahasiswa():
    data = request.get_json()
    if 'nama' not in data or 'nim' not in data or 'prodi_id' not in data:
        return jsonify({'message': 'Nama, NIM, dan prodi_id diperlukan'}), 400
    prodi = Prodi.query.get(data['prodi_id'])
    if not prodi:
        return jsonify({'message': 'Prodi tidak ditemukan'}), 404
    mahasiswa = Mahasiswa(
        nama=data['nama'],
        nim=data['nim'],
        prodi_id=data['prodi_id']
    )
    db.session.add(mahasiswa)
    db.session.commit()
    return jsonify({'message': 'Mahasiswa berhasil ditambahkan'}), 201

# Route PUT untuk Mahasiswa
@app.route('/api/mahasiswa/<int:id>', methods=['PUT'])
def update_mahasiswa(id):
    mahasiswa = Mahasiswa.query.get(id)
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa tidak ditemukan'}), 404
    data = request.get_json()
    if 'nama' in data:
        mahasiswa.nama = data['nama']
    if 'nim' in data:
        mahasiswa.nim = data['nim']
    if 'prodi_id' in data:
        prodi = Prodi.query.get(data['prodi_id'])
        if not prodi:
            return jsonify({'message': 'Prodi tidak ditemukan'}), 404
        mahasiswa.prodi_id = data['prodi_id']
    db.session.commit()
    return jsonify({'message': 'Mahasiswa berhasil diperbarui'}), 200

# Route DELETE untuk Mahasiswa
@app.route('/api/mahasiswa/<int:id>', methods=['DELETE'])
def delete_mahasiswa(id):
    mahasiswa = Mahasiswa.query.get(id)
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa tidak ditemukan'}), 404
    db.session.delete(mahasiswa)
    db.session.commit()
    return jsonify({'message': 'Mahasiswa berhasil dihapus'}), 200
