{
    'name': 'Mi Configuracion',
    'version': '1.0',
    'summary': 'Personalizaciones para CRM y Facturacion',
    'category': 'Customization',
    'depends': ['crm', 'account', 'sale_management'],
    'data': [
        'views/crm_personalizado.xml',
        'views/ventas_personalizado.xml',

    ],
    'installable': True,
    'application': True
}