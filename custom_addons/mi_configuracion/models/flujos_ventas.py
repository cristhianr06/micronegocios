from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Campos adicionales
    facturacion_automatica = fields.Boolean(string='Facturación Automática', default=True)
    fecha_ultima_factura = fields.Datetime(string='Última Facturación')
    
    def action_confirm_and_invoice(self):
        """Confirmar venta y crear factura automáticamente - MÉTODO QUE FALTA"""
        # Primero confirmar la venta
        self.action_confirm()
        
        # Crear factura automáticamente
        if self.facturacion_automatica:
            invoice_ids = self._create_invoices()
            
            # Validar factura automáticamente
            for invoice in invoice_ids:
                invoice.action_post()
            
            # Actualizar fecha
            self.fecha_ultima_factura = fields.Datetime.now()
            
            # Retornar a la factura creada
            if invoice_ids:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Factura Creada',
                    'res_model': 'account.move',
                    'res_id': invoice_ids[0].id,
                    'view_mode': 'form',
                    'target': 'current',
                }
        return True