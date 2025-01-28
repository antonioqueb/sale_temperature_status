from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temperature_status = fields.Char(
        string='Temperatura',
        compute='_compute_temperature_status',
        store=False
    )
    temperature_class = fields.Char(
        string='Class Color',
        compute='_compute_temperature_status',
        store=False
    )

    @api.depends('create_date', 'commitment_date')
    def _compute_temperature_status(self):
        for order in self:
            if not order.create_date or not order.commitment_date:
                order.temperature_status = False
                order.temperature_class = ''
                continue
            
            create_date = order.create_date.date()
            delivery_date = order.commitment_date.date()
            delta = (delivery_date - create_date).days
            
            # Lógica de asignación
            if delta < 15:
                order.temperature_status = 'Alta'
                order.temperature_class = 'badge-danger'
            else:
                order.temperature_status = 'Baja'
                order.temperature_class = 'badge-success'
