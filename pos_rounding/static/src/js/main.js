/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_rounding.pos_rounding', function(require) {
    "use strict";

    var pos_model = require('point_of_sale.models');
    var screen = require('point_of_sale.screens');

    pos_model.load_fields('pos.payment.method',['allow_rounding','decimal_rounding','used_for_rounding','visible_in_pos'])

    screen.PaymentScreenWidget.include({
        init: function(parent, options) {
            this.rounding_journal_id = null;
            this._super(parent, options);
        },
        show: function(){
            var self = this;
            self._super();
            self.$('.refresh-button').on('click',function(event){
                self.update_rounding_amount($(this).data('cid'));
            });
        },
        update_rounding_amount: function(cid){
            var self = this;
            self.click_paymentline(cid);
            var current_order =  self.pos.get_order();
            var total_amount = current_order.get_total_with_tax();
            var rounding_amount = self.get_rounding_amount(total_amount);
            current_order.previous_amount = current_order.get_total_with_tax();
            if (rounding_amount != null) {
                current_order.selected_paymentline.set_amount(rounding_amount);
                self.order_changes();
                self.render_paymentlines();
                self.$('.paymentline.selected .edit').text(self.chrome.screens.payment.format_currency_no_symbol(rounding_amount));
            }  
        },
        get_rounding_amount: function(total_amount){
            var self = this;
            var selected_paymentline = self.pos.get_order().selected_paymentline;
            var rounding_amount = null;
            if(selected_paymentline){
                var round_value = selected_paymentline.payment_method.decimal_rounding;
                var decimal_val = (total_amount - Math.floor(total_amount)).toFixed(2) * 100;;
                var remainder = decimal_val % round_value;
                if (round_value > 1) {
                    if (remainder >= (Math.ceil(round_value / 2))) {
                        rounding_amount = round_value - remainder;
                        rounding_amount *= -1;
                    } else {
                        rounding_amount = remainder;
                    }
                    rounding_amount = rounding_amount / 100
                }
            }
            return rounding_amount;
        },
        payment_input: function(input){
            var self = this;
            var order = this.pos.get_order();
            if (!(order.selected_paymentline && order.selected_paymentline.payment_method && order.selected_paymentline.payment_method.used_for_rounding))
                self._super(input);
        },
        render_paymentmethods: function() {
            var self = this;
            var cashregisters = self.pos.payment_methods;
            cashregisters.forEach(function(cashregister) {
                if (cashregister.used_for_rounding)
                    self.rounding_journal_id = cashregister.id;
            });
            return self._super();
        },

        click_paymentmethods: function(id) {
            var self = this;
            var cashregister = null;
            var current_order = self.pos.get_order();
            for (var i = 0; i < this.pos.payment_methods.length; i++) {
                if (this.pos.payment_methods[i].id === id) {
                    cashregister = this.pos.payment_methods[i];
                    break;
                }
            }
            
            if (cashregister.used_for_rounding) {
                var due = current_order.get_due()
                current_order.add_paymentline(cashregister);
                current_order.previous_amount = current_order.get_total_with_tax();
                var rounding_amount = self.get_rounding_amount(due);
                if (rounding_amount != null) {
                    self.reset_input();
                    self.render_paymentlines();
                    current_order.selected_paymentline.set_amount(rounding_amount);
                    self.order_changes();
                    self.render_paymentlines();
                    self.$('.paymentline.selected .edit').text(self.chrome.screens.payment.format_currency_no_symbol(rounding_amount));
                    self.$('.refresh-button').hide();                    
                }
            } else {
                if ((cashregister.allow_rounding) && self.rounding_journal_id && !self.check_rounding_paymentline()) {
                    self.click_paymentmethods(self.rounding_journal_id);
                }
                self._super(id);
            }
        },
        check_rounding_paymentline: function(){
            var self = this;
            var current_order = self.pos.get_order();
            var paymentlines = current_order.get_paymentlines();
            var is_rounding_paymentline = false;
            paymentlines.forEach(function(line){
                if(line.payment_method.id == self.rounding_journal_id){
                    is_rounding_paymentline = line;
                    return true;
                }
            });
            return is_rounding_paymentline;
        }
    });
});
