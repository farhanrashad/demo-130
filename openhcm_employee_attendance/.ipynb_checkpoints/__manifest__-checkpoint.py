# -*- coding: utf-8 -*-
{
    'name': "Openhcm employee Attendance",
    'version': '0.1',
    'category': 'Employee',
    'summary': 'Openhcm Employee Attendance ',
    'sequence': 3,
    'description': """"  """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
#     'license': 'LGPL-3',
    'depends': ['base','hr_attendance','report_xlsx'],
    
    'data': [
        'security/ir.model.access.csv',
        'views/employee_checkin_checkout.xml',
        'views/employee_attendance_menu.xml',
        'wizards/employee_attendance.xml',
        'report/attendance_report.xml',
        
        'report/employee_att_report.xml',
        
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}
