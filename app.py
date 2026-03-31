from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pytz
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sel_verileri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Türkiye saat dilimi
turkey = pytz.timezone("Europe/Istanbul")

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    su = db.Column(db.Float)
    toprak = db.Column(db.Float)
    yagmur = db.Column(db.Float)
    tarih_saat = db.Column(db.DateTime, default=lambda: datetime.now(turkey))

# Veritabanı oluştur
with app.app_context():
    db.create_all()

# Veri alma endpointi
@app.route('/api/veri', methods=['GET', 'POST'])
def veri_al():
    if request.method == 'GET':
        return jsonify({"mesaj": "API çalışıyor"}), 200

    data = request.get_json(silent=True)

    try:
        if not data:
            su = request.form.get('su')
            toprak = request.form.get('toprak')
            yagmur = request.form.get('yagmur')
        else:
            su = data.get('su')
            toprak = data.get('toprak')
            yagmur = data.get('yagmur')

        if su is None or toprak is None or yagmur is None:
            return jsonify({"error": "Eksik veri"}), 400

        veri = SensorData(
            su=float(su),
            toprak=float(toprak),
            yagmur=float(yagmur),
            tarih_saat=datetime.now(turkey)
        )

        db.session.add(veri)
        db.session.commit()

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Son veriyi getiren endpoint
@app.route('/api/son-veri', methods=['GET'])
def son_veri():
    veri = SensorData.query.order_by(SensorData.tarih_saat.desc()).first()

    if not veri:
        return jsonify({"mesaj": "Henüz veri yok"}), 404

    return jsonify({
        "su": veri.su,
        "toprak": veri.toprak,
        "yagmur": veri.yagmur,
        "tarih_saat": veri.tarih_saat.strftime("%d.%m.%Y %H:%M:%S")
    })

# Ana sayfa
@app.route('/')
def index():
    veriler = SensorData.query.order_by(
        SensorData.tarih_saat.desc()
    ).limit(10).all()

    return render_template('index.html', veriler=veriler)

# Render için
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)