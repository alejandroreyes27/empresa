from flask import Blueprint, render_template,request,redirect,url_for
from app.models.Employees import Employees
from app import db

bp = Blueprint('employees', __name__)

@bp.route('/Employees')
def index():
    data_employee = Employees.query.all()   
    return render_template('employees/index.html', data_employee=data_employee)

@bp.route('/Employees/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nameEmployee = request.form['nameEmployee']
        telefonoEmployee = request.form['telefonoEmployee']
        emailEmployee = request.form['emailEmployee']
        
        new_employee = Employees(nameEmployee=nameEmployee,telefonoEmployee=telefonoEmployee,emailEmployee=emailEmployee)
        db.session.add(new_employee)
        db.session.commit()
        
        return redirect(url_for('employees.index'))

    return render_template('employees/add.html')

@bp.route('/Employees/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    employees = Employees.query.get_or_404(id)

    if request.method == 'POST':
        employees.nameEmployee = request.form['nameEmployee']
        employees.telefonoEmployee = request.form['telefonoEmployee']
        employees.emailEmployee = request.form['emailEmployee']
        db.session.commit()
        return redirect(url_for('employees.index'))

    return render_template('employees/edit.html', employees=employees)

@bp.route('/Employees/delete/<int:id>')
def delete(id):
    employees = Employees.query.get_or_404(id)
    db.session.delete(employees)
    db.session.commit()

    return redirect(url_for('employees.index'))

@bp.route('/Employees/list/<int:id>')
def list(id):
    empleados = Employees.query.get_or_404(id)
    data_departamentos = empleados.departmentsEmployee
    print(data_departamentos)
    return render_template('employees/list.html', data_departments=data_departamentos)