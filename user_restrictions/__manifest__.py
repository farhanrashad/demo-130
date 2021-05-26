# -*- coding: utf-8 -*-
{
	"name" : "User Restrictions",
	"version" : "13.0.4.0",
	"category" : "Purchase",
	'summary': 'User Restrictions',
	"depends" : ['purchase','stock_account'],
	"data": [
		'security/ir.model.access.csv',
		'security/user_security.xml',
		'views/user_restrictions.xml',
	],
	"auto_install": False,
	"installable": True,
}
