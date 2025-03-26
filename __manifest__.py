{
    'name': 'Limpieza de Datos',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Eliminar datos de prueba: ventas, compras y stock',
    'author': 'Tu Nombre o Empresa',
    'depends': ['base', 'sale', 'purchase', 'stock', 'point_of_sale', 'account'],
    'data': [
        'views/limpiar_base_wizard.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
