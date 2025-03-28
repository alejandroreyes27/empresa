from flask import Blueprint, render_template, request, redirect, url_for
from app.models.Departments import Departments
from app import db

bp = Blueprint('departments', __name__)

@bp.route('/Departments')
def index():
    data_department = Departments.query.all()   
    return render_template('departments/index.html', data_department=data_department)
    
@bp.route('/Departments/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nameDepartment = request.form['nameDepartment']
        
        new_departments = Departments(nameDepartment=nameDepartment)
        db.session.add(new_departments)
        db.session.commit()
        
        return redirect(url_for('departments.index'))

    return render_template('departments/add.html')

@bp.route('/Departments/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    departments = Departments.query.get_or_404(id)

    if request.method == 'POST':
        departments.nameDepartment = request.form['nameDepartment']
        db.session.commit()
        return redirect(url_for('departments.index'))

    return render_template('departments/edit.html', departments=departments)

@bp.route('/Departments/delete/<int:id>')
def delete(id):
    departments = Departments.query.get_or_404(id)
    db.session.delete(departments)
    db.session.commit()

    return redirect(url_for('departments.index'))

@bp.route('/Departments/list/<int:id>')
def list(id):
    departamentos = Departments.query.get_or_404(id)
    data_empleados = departamentos.employeesDepartment
    return render_template('departments/list.html',data_empleados=data_empleados)