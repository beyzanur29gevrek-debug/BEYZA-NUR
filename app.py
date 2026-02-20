from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os

app = Flask(__name__)
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

# 🔥 ESP32 veri gönderme endpointi
@app.route('/api/veri', methods=['POST'])
def veri_al():
    data = request.get_json()

    # JSON gelmezse form destekle (test için)
    if not data:
        su = float(request.form.get('su'))
        toprak = float(request.form.get('toprak'))
        yagmur = float(request.form.get('yagmur'))
    else:
        su = float(data.get('su'))
        toprak = float(data.get('toprak'))
        yagmur = float(data.get('yagmur'))

    if su is None or toprak is None or yagmur is None:
        return jsonify({"error": "Eksik veri"}), 400

    veri = SensorData(
        su=su,
        toprak=toprak,
        yagmur=yagmur,
        tarih_saat=datetime.now(turkey)
    )

    db.session.add(veri)
    db.session.commit()

    return jsonify({'status': 'ok'}), 200

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