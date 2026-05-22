# -*- coding: utf-8 -*-

{
    'name': 'Sale Temperature Status',
    'version': '1.0.1',
    'summary': 'Muestra indicadores de temperatura, entrega y códigos únicos en órdenes de venta',
    'category': 'Sales',
    'author': 'Alphaqueb Consulting S.A.S.',
    'website': 'https://alphaqueb.com',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}