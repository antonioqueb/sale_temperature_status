## ./__init__.py
```py
from . import models```

## ./__manifest__.py
```py
{
    'name': 'Sale Temperature Status',
    'version': '1.0',
    'summary': 'Muestra un indicador de temperatura en órdenes de venta',
    'category': 'Sales',
    'author': 'Alphaqueb Consulting S.A.S.',
    'website': 'https://alphaqueb.com',
    'depends': ['sale_management'],
    'data': [
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
```

## ./models/__init__.py
```py
from . import sale_order```

## ./models/sale_order.py
```py
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
```

## ./views/sale_views.xml
```xml
<odoo>
    <record id="view_quotation_tree_inherit" model="ir.ui.view">
        <field name="name">sale.order.tree.inherit.quotation.entrega_en</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_quotation_tree"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='partner_id']" position="after">
                <field name="temperature_status" widget="badge"
                       decoration-danger="temperature_status == 'Incidencia'"
                       decoration-primary="temperature_status == 'Normal'" 
                       readonly="1"/>
                <field name="entrega_en" string="Entrega en" readonly="1"/>
                <field name="unique_product_codes" string="Productos" readonly="1"/>
            </xpath>
        </field>
    </record>

    <record id="view_order_tree_inherit" model="ir.ui.view">
        <field name="name">sale.order.tree.inherit.order.entrega_en</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_tree"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='partner_id']" position="after">
                <field name="temperature_status" widget="badge"
                       decoration-danger="temperature_status == 'Incidencia'"
                       decoration-primary="temperature_status == 'Normal'" 
                       readonly="1"/>
                <field name="entrega_en" string="Entrega en" readonly="1"/>
                <field name="unique_product_codes" string="Productos" readonly="1"/>
            </xpath>
        </field>
    </record>
</odoo>```

