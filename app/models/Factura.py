from app import db
from datetime import datetime

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estado_pago = db.Column(db.String(50), default='pendiente')  # 'pagado', 'pendiente', 'cancelado'

    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)

    def __repr__(self):
        return f'<Factura {self.id}>'