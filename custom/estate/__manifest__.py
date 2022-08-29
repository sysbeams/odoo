{
    'name': 'ESTATE MANAGEMENT',
    'author': 'Sysbeams',
    'sequence': -100,
    'depends': [
        'base_setup'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_list_view.xml',
        'views/estate_property_type_list_view.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
