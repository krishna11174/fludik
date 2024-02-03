# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Fields Addition',
    'version': '0.6',
    'summary': 'IAdding custom fields for importing master data',
    'sequence': 10,
    'description': """    """,
    'category': 'Contacts',
    'depends': ['base', 'stock','sale','account','contacts','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sequence_increase_wizard.xml',
        'wizard/bom_sequence_wizard.xml',
        # 'data/server_action_description.xml',
        'views/contact_addition_views.xml',
        'views/contact_approval_view.xml',
        'views/product_approval_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}