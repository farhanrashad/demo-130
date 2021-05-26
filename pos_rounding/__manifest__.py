# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Rounding Off Amount",
  "summary"              :  """The module allows you to round the amount in the POS order manually or set it for automatic to make the payments faster and easier for customers.""",
  "category"             :  "Point of Sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Rounding-Off-Amount.html",
  "description"          :  """Odoo POS Rounding Off Amount
Sale order amount round off
Round-off amount in sale order
POS cash rounding off
POS invoice round off
Invoice amount round-off
Round Off Invoice Amount
POS invoice round off
POS order amount round off
Odoo round off figure
POS Rounding Off Payment
Round Off Payment""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_rounding&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_payment_method_views.xml',
                             'views/template.xml',
                            ],
  "demo"                 :  ['data/pos_rounding_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos_rounding.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}