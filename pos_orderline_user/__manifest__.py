# -*- coding: utf-8 -*-

{
    'name': 'Pos Orderline User',
    'version': '13.0.3.5',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'Allows you to select salesperson from Pos orderline.',
    'description': "Allows you to select salesperson from Pos orderline. ",
    'depends': ['point_of_sale'],
    'data': ['views/views.xml',],
    'qweb': ['static/src/xml/pos.xml',],
    'images': ['static/description/salesperson.jpg',],
    'installable': True,
}
