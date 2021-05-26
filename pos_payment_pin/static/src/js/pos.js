odoo.define('pos_payment_pin.pos_payment_pin', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var rpc = require('web.rpc');
var core = require('web.core');
var popups = require('point_of_sale.popups');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var QWeb = core.qweb;

models.load_fields('pos.order',['cc_pin']);

	var PaymentPinWidget = popups.extend({
		template: 'PaymentPinWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		show: function(options){
			var self = this;
            options = options || {};            
            this._super(options);  
                       
            this.renderElement();   
            $("#cc_pin").focus(function() {
                $('body').off('keypress', self.keyboard_handler);
                $('body').off('keydown', self.keyboard_keydown_handler);
            });
            $("#cc_pin").focusout(function() {
                $('body').keypress(self.keyboard_handler);
                $('body').keydown(self.keyboard_keydown_handler);
            });
            $("#cc_pin").keypress(function (e) {
                if ($('#cc_pin').val().length >= 16){
                    $("#errmsg").html("More than 16 digits are not allowed!").show().delay(5000).fadeOut("slow");
                    return false;
                }
                if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
                    //display error message
                    $("#errmsg").html("Digits Only").show().delay(5000).fadeOut("slow");
                    return false;
                }
            });
            $('.confirm').click(function () {
                if ($('#cc_pin').val().length > 16){
                    $("#errmsg").html("Please enter 16 digits of the Credit Card Number!").show().delay(5000).fadeOut("slow");
                    return false;   
                }
            });
		},
/*		click_confirm: function () {
            var value = this.$('#cc_pin').val();
            this.gui.close_popup();
            if (this.options.confirm) {
                this.options.confirm.call(this, value);
            }
        }*/
	});
	gui.define_popup({
		name: 'payment_pin_widget',
		widget: PaymentPinWidget
	});
var posorder_super = models.Order.prototype;
models.Order = models.Order.extend({
    export_as_JSON: function(){
        var loaded = posorder_super.export_as_JSON.apply(this, arguments);
        loaded.cc_pin = this.cc_pin || false;
        return loaded;
    },
})

models.load_fields('pos.payment.method', ['is_credit_card']);
	screens.PaymentScreenWidget.include({
    render_paymentmethods: function() {
        var self = this;
        var order = this.pos.get_order();
        var methods = $(QWeb.render('PaymentScreen-Paymentmethods', { widget:this }));
            methods.on('click','.paymentmethod',function(){
                var payment_method = self.pos.payment_methods_by_id[$(this).data('id')];
                if (payment_method.is_credit_card) {
                    self.gui.show_popup('payment_pin_widget', {
                    confirm: function () {
                        var cc_pin = $('#cc_pin').val();
                        if (cc_pin.length <= 16){
                            order['cc_pin'] = cc_pin;
                            self.click_paymentmethods(payment_method.id);
                        }
                    }});
                }
                else{
                    self.click_paymentmethods(payment_method.id);
                }
            });
        return methods;
    },
	});
});
