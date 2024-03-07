# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contact Leads Fields',
    'version': '17.0.1.0.0',
    'summary': 'Add fields to contact screen and leads screen',
    'description': 'Add fields to contact screen and leads screen',
    'author': 'Mohamed Salem',
    'license': 'LGPL-3',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
