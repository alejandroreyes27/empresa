from flask import Blueprint, render_template, request, redirect, url_for
from app.models.DepartmentsEmployees import DepartmentsEmployees
from app.models.Departments import Departments
from app.models.Employees import Employees
from app import db

bp = Blueprint('departmentsEmployees', __name__)

@bp.route('/departmentsEmployees')
def index():
    data = DepartmentsEmployees.query.all()
    return render_template('departmentsEmployees/index.html', data=data)

@bp.route('/departmentsEmployees/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        idEmployee = request.form['idEmployee']
        idDepartment = request.form['idDepartment']
        
        new_employee_departments = DepartmentsEmployees(department_id=idDepartment,employee_id=idEmployee)
        db.session.add(new_employee_departments)
        db.session.commit()
        
        return redirect(url_for('departmentsEmployees.index'))
    
    data_department = Departments.query.all()
    data_employee = Employees.query.all()
    return render_template('departmentsEmployees/add.html',data_department=data_department,data_employee=data_employee)

@bp.route('/departmentsEmployees/edit/<int:eid>/<int:did>', methods=['GET', 'POST'])
def edit(eid,did):

    edata =Employees.query.get_or_404(eid)
    ddata = Departments.query.get_or_404(did)
    empleados= Employees.query.all() 
    departamentos= Departments.query.all() 
    if request.method == 'POST':
        
        departmentEmployee = DepartmentsEmployees.query.filter_by(department_id=did,employee_id=eid).first()
        departmentEmployee.employee_id = request.form['idempleado']
        departmentEmployee.department_id = request.form['iddepartamento']
        try:
            db.session.commit()
        except:
            print("Error en la base de datos")
        return redirect(url_for('departmentsEmployees.index'))

    return render_template('departmentsEmployees/edit.html',empleadosdata=empleados, departamentosdata=departamentos,edata=edata,ddata=ddata )


@bp.route('/departmentsEmployees/delete/<int:did>/<int:eid>')
def delete(did,eid):

    departmentEmployee = DepartmentsEmployees.query.filter_by(department_id=did, employee_id=eid).first()

    if departmentEmployee:
        print(f"Por eliminar: {departmentEmployee} {departmentEmployee.department_id}") 
        db.session.delete(departmentEmployee)
        db.session.commit()
        print(f"Record with department_id={did} and employee_id={eid} deleted.")
    else:
        print(f"No record found with department_id={did} and employee_id={eid}.")
    return redirect(url_for('departmentsEmployees.index')) 