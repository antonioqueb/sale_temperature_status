from odoo import models, fields, api
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temperature_status = fields.Selection(
        [('Incidencia', 'Incidencia'), ('Normal', 'Normal')],
        string='Estatus',
        compute='_compute_temperature_status',
        store=True,  # Almacenar el valor en la base de datos
        readonly=True
    )
    
    entrega_en = fields.Integer(
        string='Entrega en',
        compute='_compute_entrega_en',
        store=True,  # Almacenar el valor en la base de datos
        readonly=True
    )

    @api.depends('commitment_date')
    def _compute_entrega_en(self):
        for order in self:
            if not order.commitment_date:
                order.entrega_en = 0
                continue

            today = date.today()
            delivery_date = order.commitment_date.date()
            days_remaining = (delivery_date - today).days

            # No mostrar valores negativos
            order.entrega_en = max(days_remaining, 0)

    @api.depends('create_date', 'commitment_date')
    def _compute_temperature_status(self):
        for order in self:
            if not order.create_date or not order.commitment_date:
                order.temperature_status = False
                continue
            
            create_date = order.create_date.date()
            delivery_date = order.commitment_date.date()
            delta = (delivery_date - create_date).days
            
            # Asignar valores según el delta de días
            if delta < 15:
                order.temperature_status = 'Incidencia'
            else:
                order.temperature_status = 'Normal'
