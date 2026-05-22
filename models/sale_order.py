# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temperature_status = fields.Selection(
        selection=[
            ('Incidencia', 'Incidencia'),
            ('Normal', 'Normal'),
        ],
        string='Estatus',
        compute='_compute_temperature_status',
        store=True,
        readonly=True,
    )

    entrega_en = fields.Integer(
        string='Entrega en',
        compute='_compute_entrega_en',
        store=False,
        readonly=True,
        help='Días restantes para la fecha compromiso de entrega.',
    )

    pending_delivery_line_count = fields.Integer(
        string='Entregas Pendientes',
        compute='_compute_pending_delivery_line_count',
        store=True,
        readonly=True,
    )

    unique_product_codes = fields.Char(
        string='Códigos únicos',
        compute='_compute_unique_product_codes',
        store=False,
        readonly=True,
        help='Resumen de códigos internos únicos de los productos incluidos en la orden de venta.',
    )

    @api.depends('commitment_date')
    def _compute_entrega_en(self):
        today = fields.Date.context_today(self)
        for order in self:
            if not order.commitment_date:
                order.entrega_en = 0
                continue

            delivery_date = fields.Date.to_date(order.commitment_date)
            days_remaining = (delivery_date - today).days
            order.entrega_en = max(days_remaining, 0)

    @api.depends('create_date', 'commitment_date')
    def _compute_temperature_status(self):
        for order in self:
            if not order.create_date or not order.commitment_date:
                order.temperature_status = False
                continue

            create_date = fields.Date.to_date(order.create_date)
            delivery_date = fields.Date.to_date(order.commitment_date)
            delta = (delivery_date - create_date).days

            order.temperature_status = 'Incidencia' if delta < 15 else 'Normal'

    @api.depends(
        'order_line.product_uom_qty',
        'order_line.qty_delivered',
        'order_line.display_type',
    )
    def _compute_pending_delivery_line_count(self):
        for order in self:
            count = 0
            for line in order.order_line:
                if line.display_type:
                    continue
                if line.product_uom_qty > line.qty_delivered:
                    count += 1
            order.pending_delivery_line_count = count

    @api.depends(
        'order_line.product_id',
        'order_line.product_id.default_code',
        'order_line.display_type',
    )
    def _compute_unique_product_codes(self):
        for order in self:
            codes = []

            for line in order.order_line:
                if line.display_type or not line.product_id:
                    continue

                code = line.product_id.default_code or line.product_id.display_name

                if code and code not in codes:
                    codes.append(code)

            order.unique_product_codes = ', '.join(codes)