# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright © 2016 Preciseways IT Solutions. (<http://preciseways.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Department Restrictions",
    'summary': """
         Department Restriction on Users.""",
    'description': """
        This module restrict user for deparment purchase order and product .
    """,
    'author': "Preciseways IT Solutions",
    'website': "http://www.preciseways.com",
    'category': 'Warehouse',
    'version': '13.0.5.0',
    'images': ['static/description/WarehouseRestrictions.jpg'],
    'depends': ['base', 'stock', 'purchase'],
    'data': [
        'views/users_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    
    
}
