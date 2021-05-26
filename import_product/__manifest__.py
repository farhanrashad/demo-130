{
    'name': 'Product Import Script',
    'version': '13.0.1.0',
    'sequence': 4,
    'category': 'Product',
    'summary': 'This module is used to import product in product varients',
    'description': """ This module is used to import product in product varients and script contains all the fields and available fields to be import in Product varient form
    """,
    'price': 20,
    'currency': 'EUR',
    'author': 'Usman Farzand',
    'email': 'usman.farzand@dymaxcel.com',
    'license': 'AGPL-3',
    'depends': ['base','point_of_sale'],
    'data': [
        "security/product_security.xml",
        "product_upload.xml"
    ],
    'qweb': [
        ],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
