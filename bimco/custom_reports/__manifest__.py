# -*- coding: utf-8 -*-
{
    'name': "custom_reports",
    'description': """
        Prime Invoice Custom Reports
    """,
    'author': "Prime Minds Pvt.LTD",
    'website': "Prime Minds Pvt.LTD",
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'account','l10n_in_edi','l10n_in_tcs_tds'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/account_inherited.xml',
        'reports/invoice_report.xml',
        'reports/pro_invoice_report.xml',
        'reports/purchase_order_report.xml'
    ],
    'installable': True,
    'auto_install': False,
}
