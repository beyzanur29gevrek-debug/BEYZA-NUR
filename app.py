from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sel_verileri.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    su = db.Column(db.Float)
    toprak = db.Column(db.Float)
    yagmur = db.Column(db.Float)
    tarih_saat = db.Column(db.DateTime, default=datetime.utcnow)

# Application context içinde veritabanı oluştur
with app.app_context():
    db.create_all()

@app.route('/api/sel', methods=['POST'])
def veri_al():
    su = float(request.form['su'])
    toprak = float(request.form['toprak'])
    yagmur = float(request.form['yagmur'])
    veri = SensorData(su=su, toprak=toprak, yagmur=yagmur)
    db.session.add(veri)
    db.session.commit()
    return jsonify({'status':'ok'})

@app.route('/')
def index():
    veriler = SensorData.query.order_by(SensorData.tarih_saat.desc()).limit(10).all()
    return render_template('index.html', veriler=veriler)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Portu 5001 yapıyoruz, 5000 meşgul olmasın
    import os

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)