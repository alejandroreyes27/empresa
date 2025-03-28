from app import db

class DepartmentsEmployees(db.Model):
   __tablename__ = 'department_employee'
   department_id = db.Column(db.Integer, db.ForeignKey('department.idDepartment'), primary_key=True)
   employee_id = db.Column(db.Integer, db.ForeignKey('employee.idEmployee'), primary_key=True)