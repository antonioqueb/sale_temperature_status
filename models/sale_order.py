from odoo import models, fields, api
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temperature_status = fields.Selection(
        [('Incidencia', 'Incidencia'), ('Normal', 'Normal')],
        string='Estatus',
        compute='_compute_temperature_status',
        store=True,
        readonly=True,
    )

    entrega_en = fields.Integer(
        string='Entrega en',
        compute='_compute_entrega_en',
        store=True,
        readonly=True,
    )

    pending_delivery_line_count = fields.Integer(
        string='Entregas Pendientes',
        compute='_compute_pending_delivery_line_count',
        store=True,
        readonly=True,
    )

    @api.depends('commitment_date')
    def _compute_entrega_en(self):
        today = date.today()
        for order in self:
            if not order.commitment_date:
                order.entrega_en = 0
                continue

            delivery_date = order.commitment_date.date()
            days_remaining = (delivery_date - today).days
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

            order.temperature_status = 'Incidencia' if delta < 15 else 'Normal'

    @api.depends('order_line.product_uom_qty', 'order_line.qty_delivered', 'order_line.display_type')
    def _compute_pending_delivery_line_count(self):
        for order in self:
            count = 0
            for line in order.order_line:
                if line.display_type:
                    continue
                if line.product_uom_qty > line.qty_delivered:
                    count += 1
            order.pending_delivery_line_count = count