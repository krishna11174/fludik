{
    'name': 'Expenses Portal',
    'version': '1.0',
    'summary': 'Manage expenses from the portal',
    'description': 'This module allows users to manage their expenses through the portal.',
    'author': 'Gautam kumar',
    'depends': ['base', 'portal', 'web', 'website', 'hr_expense'],
    'data': [
        'views/expense_view.xml',
        'views/expense_template.xml',
    ],
    'installable': True,
    'application': True,
}
