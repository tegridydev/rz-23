from app import db

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    compressed_data = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    reward = db.Column(db.Float, nullable=False)
