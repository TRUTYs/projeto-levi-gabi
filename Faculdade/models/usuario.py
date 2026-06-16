from extensions import db
class Usuario(db.Model):
    __tablename__ = "usuario"
    id    = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(200), nullable=False)
    tipo  = db.Column(db.Enum("admin","vendedor"), nullable=False, default="vendedor")
