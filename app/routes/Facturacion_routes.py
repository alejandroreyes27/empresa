from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import current_user, login_required
from app.models import Factura, DetalleFactura  # Ahora se importan desde __init__.py
from app.models.Carrito import Carrito
from app.models.Productos import Productos
from app import db
import pdfkit
import io


# Crear Blueprint con mayúscula inicial
bp = Blueprint('Facturacion', __name__)

@bp.route('/procesar-compra', methods=['POST'])
@login_required  # Solo usuarios autenticados pueden comprar
def procesar_compra():
    # Verificar si el carrito está vacío
    if not current_user.carrito:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('carrito.ver_carrito'))
    
    try:
        # Calcular total
        total = sum(item.producto.precio * item.cantidad for item in current_user.carrito)
        
        # Crear factura
        nueva_factura = Factura(
            usuario_id=current_user.id,
            total=total,
            estado_pago='pagado'  # Puedes integrar pasarelas de pago aquí
        )
        db.session.add(nueva_factura)
        db.session.flush()  # Para obtener el ID de la factura
        
        # Crear detalles de la factura
        for item in current_user.carrito:
            detalle = DetalleFactura(
                factura_id=nueva_factura.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
                subtotal=item.producto.precio * item.cantidad
            )
            db.session.add(detalle)
        
        # Vaciar carrito
        Carrito.query.filter_by(usuario_id=current_user.id).delete()
        db.session.commit()
        
        flash('¡Compra realizada con éxito!', 'success')
        return redirect(url_for('facturacion.ver_factura', factura_id=nueva_factura.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al procesar la compra: {str(e)}', 'danger')
        return redirect(url_for('carrito.ver_carrito'))
    
@bp.route('/factura/<int:factura_id>')
@login_required
def ver_factura(factura_id):
    factura = Factura.query.filter_by(id=factura_id, usuario_id=current_user.id).first()
    if not factura:
        flash('Factura no encontrada', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('factura.html', factura=factura)

@bp.route('/factura/<int:factura_id>/pdf')
@login_required
def descargar_factura_pdf(factura_id):
    factura = Factura.query.filter_by(id=factura_id, usuario_id=current_user.id).first()
    if not factura:
        flash('Factura no encontrada', 'danger')
        return redirect(url_for('main.index'))
    
    html = render_template('factura_pdf.html', factura=factura)
    pdf = pdfkit.from_string(html, False)
    
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        download_name=f'factura_{factura.id}.pdf',
        as_attachment=True
    )