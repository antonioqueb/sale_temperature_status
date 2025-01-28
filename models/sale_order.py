from odoo import models, fields, api
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temperature_status = fields.Char(
        string='Temperatura',
        compute='_compute_temperature_status',
        store=False
    )

    @api.depends('create_date', 'commitment_date')
    def _compute_temperature_status(self):
        for order in self:
            if not order.create_date or not order.commitment_date:
                order.temperature_status = False
                continue
            
            # Convertir ambos a date
            create_date = order.create_date.date()
            delivery_date = order.commitment_date.date()  # Conversión añadida
            delta = (delivery_date - create_date).days
            
            order.temperature_status = 'green' if delta >= 15 else 'red'