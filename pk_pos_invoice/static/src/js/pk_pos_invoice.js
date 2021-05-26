odoo.define('pk_pos_invoice.pk_pos_invoice', function(require) {
"use strict";
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var _t = core._t;

    screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
            var self = this;
            var order = self.pos.get_order();
            console.log('issssss', order);
            if (! order.get_client()){
                self.gui.show_popup('error',{
                    title: _t('Customer not found'),
                    body:  _t('Please select customer before validating order !'),
                });
                return false;
            }
            self._super();
        },
    });
});