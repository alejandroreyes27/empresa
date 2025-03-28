from app import db

class Departments(db.Model):
   __tablename__ = 'department'
   idDepartment = db.Column(db.Integer, primary_key=True)
   nameDepartment = db.Column(db.String(255), nullable=False)
   
   employeesDepartment = db.relationship('Employees', secondary='department_employee')