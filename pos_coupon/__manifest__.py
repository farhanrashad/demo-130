# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "POS Gift Voucher",
	"version" : "13.0.6.1",
	"category" : "Point of Sale",
	'summary': 'POS Gift Voucher',
	"author": "BrowseInfo",
	"depends" : ['account','point_of_sale'],
	"data": [
		'security/coupon_security.xml',
		'security/ir.model.access.csv',
		'views/pos_assets.xml',
		'views/pos_gift_coupon.xml',
		'views/gift_coupon_report.xml',
		'views/report_pos_gift_coupon.xml',
		'views/pos_gift_voucher_setting.xml',
	],
	'qweb': [
		'static/src/xml/pos_coupon.xml',
	],
	"auto_install": False,
	"installable": True,
}
