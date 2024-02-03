{
    'name': 'Time Off Portal',
    'version': '1.0',
    'summary': 'Manage employee vacations & absence from the portal',
    'description': 'This module allows users to manage their employee vacations & absence through the portal.',
    'author': 'Gautam kumar',
    'depends': ['base', 'portal', 'web', 'website', 'hr_holidays'],
    'data': [
        'views/timeoff_template.xml',
    ],
    'installable': True,
    'application': True,
}
