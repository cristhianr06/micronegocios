from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Campos adicionales para seguimiento
    facturacion_automatica = fields.Boolean(string='Facturación Automática', default=True)
    fecha_ultima_factura = fields.Datetime(string='Última Facturación')
    
    def action_confirm_and_invoice(self):
        """Confirmar venta y crear factura automáticamente"""
        self.action_confirm()
        
        if self.facturacion_automatica:
            # Crear factura
            invoice = self._create_invoices()
            # Validar factura automáticamente
            invoice.action_post()
            
            self.write({
                'fecha_ultima_factura': fields.Datetime.now(),
                'invoice_status': 'invoiced'
            })
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Factura Creada',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
            }

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        """Extender validación de factura para notificar venta"""
        res = super(AccountMove, self).action_post()
        
        # Notificar a la venta relacionada
        if self.move_type == 'out_invoice':
            sale_orders = self.invoice_line_ids.sale_line_ids.order_id
            for sale in sale_orders:
                sale.message_post(
                    body=f"Factura {self.name} validada automáticamente",
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
        
        return res