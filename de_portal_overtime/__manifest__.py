# -*- coding: utf-8 -*-
{
    'name': "Portal Overtime",

    'summary': """
        Portal Overtime 
        1- Portal overtime approval.
        """,

    'description': """
        Portal Overtime 
        1- Portal overtime approval.
        2- Attendance lock.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Payroll',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'de_employee_overtime','hr_attendance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/approval_request_views.xml',
        'views/hr_overtime_approval_views.xml',
        'views/hr_overtime_template_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
