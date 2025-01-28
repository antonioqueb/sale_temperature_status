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

        
    # Nuevo campo agregado
    unique_product_codes = fields.Char(
        string='Códigos Únicos',
        compute='_compute_unique_product_codes',
        store=True,
        readonly=True,
        help='Códigos únicos de productos concatenados de las líneas de la orden'
    )

    @api.depends('order_line.product_id.default_code')
    def _compute_unique_product_codes(self):
        for order in self:
            codes = set()
            for line in order.order_line:
                if line.product_id and line.product_id.default_code:
                    codes.add(line.product_id.default_code.strip())
            sorted_codes = sorted(codes)
            order.unique_product_codes = ', '.join(sorted_codes) if sorted_codes else ''

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
