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
    'assets': {
    'web.assets_frontend': [
        'sale_temperature_status/static/src/css/*.css',
    ],
},

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}