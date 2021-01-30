# -*- coding: utf-8 -*-
{
    'name': "Employee Insurance",

    'summary': """
        Employee Insurance Management By Dynexcel""",

    'description': """
        Long description of module's purpose
    """,

    'author': "By Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'HR',
    'version': '0.1',
    "sequence": 7,
    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'views/employee_insurance_view.xml',
        'views/insurance_menu.xml',
        'reports/employee_insurance_report.xml',
        'reports/report.xml',

    ],
    # only loaded in demonstration mode

}
