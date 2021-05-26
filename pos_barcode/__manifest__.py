# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "POS Return with barcode",
	"version" : "13.0",
	"category" : "Point of Sale",
	'summary': 'POS Return with barcode',
	"author": "BrowseInfo",
	"depends" : ['point_of_sale'],
	"data": [
		'views/pos_barcode.xml',
	],
	'qweb': [
		'static/src/xml/pos_barcode.xml',
	],
	"auto_install": False,
	"installable": True,
}
