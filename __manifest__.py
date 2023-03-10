
{
    'name': 'Automated Sale Order',
    'sequence': 1,
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/automated_sale_order.xml',
        'wizard/automatic_sale_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
