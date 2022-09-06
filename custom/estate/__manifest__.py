{
    'name': 'ESTATE MANAGEMENT',
    'author': 'Sysbeams',
    'category': 'Real Estate Brokerage',
    'sequence': -100,
    'depends': [
        'base_setup'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_security.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_list_view.xml',
        'views/estate_property_type_list_view.xml',
        'views/estate_property_offer_list_view.xml',
        'views/res_users_views.xml'

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
