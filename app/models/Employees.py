from app import db

class Employees(db.Model):
    __tablename__ = 'employee'
    idEmployee = db.Column(db.Integer, primary_key=True)
    nameEmployee = db.Column(db.String(255), nullable=False)
    telefonoEmployee = db.Column(db.String(255), nullable=False)
    emailEmployee = db.Column(db.String(255), nullable=False)
   
    departmentsEmployee = db.relationship('Departments', secondary='department_employee')