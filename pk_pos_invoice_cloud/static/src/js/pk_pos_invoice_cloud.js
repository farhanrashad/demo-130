odoo.define('pk_pos_invoice_cloud.pk_pos_invoice_cloud', function(require) {
"use strict";
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');
    models.load_fields('pos.config', ['fbr_limit']);
    models.load_fields('pos.order', ['invoice_number']);
    models.load_fields('res.partner',['buyer_ntn', 'buyer_cnic']);

    screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
            var self = this;
            var order = self.pos.get_order();
            var customer = order.get_client();
            if (order.get_total_paid() >= self.pos.config.fbr_limit && self.pos.config.fbr_limit > 0 && !order.get_client() && order.orderlines.length){
                self.gui.show_popup('error',{
                    title: _t('Customer not found'),
                    body:  _t('Please select customer before validating order !'),
                });
                return false;
            }
            if (customer && customer.buyer_cnic === false && order.get_total_paid() >= self.pos.config.fbr_limit && self.pos.config.fbr_limit > 0) {
                self.gui.show_popup('error',{
                    title: _t('Customer CNIC Required'),
                    body:  _t('Please set CNIC in the customer !'),
                });
                return false;    
            }
            self._super(force_validation);
        },
    });

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
    _save_to_server: function(orders, options) {
        var self = this;
        return _super_posmodel._save_to_server.call(this, orders, options).then(function(new_orders) {4
            if (new_orders != null) {
                new_orders.forEach(function(order) {
                    rpc.query({
                        model: 'pos.order',
                        method: 'send_invoice_data',
                        args: [order['id']],
                        }).then(function(output) {
                            if (output['Code'] === '100'){
                                var invoice_number = output['InvoiceNumber'] || ''
                                $('#invoice_number').text(invoice_number);
                                jQuery("#qr-example").qrcode({
                                    width: 120,
                                    height: 120,
                                    text: invoice_number
                                });
                            }
                        });
                    });
                }
                return new_orders;
            });
        }
    });
    
    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function () {
            var res = _super_Order.export_for_printing.apply(this, arguments);
            var client  = this.get('client');
            res['buyer_ntn'] = client ? client.buyer_ntn : null
            res['buyer_cnic'] = client ? client.buyer_cnic : null
            res['client_phone'] = client ? client.phone : null
            return res;
        },
    });

/*screens.ClientListScreenWidget.include({
    save_client_details: function (partner) {
        var fields = {};
        var self = this;
        var phone_list = [];
        var email_list = [];
        var barcode_list = [];

        this.$('.client-details-contents .detail').each(function(idx,el){
            if (self.integer_client_details.includes(el.name)){
                var parsed_value = parseInt(el.value, 10);
                if (isNaN(parsed_value)){
                    fields[el.name] = false;
                }
                else{
                    fields[el.name] = parsed_value
                }
            }
            else{
                fields[el.name] = el.value || false;
            }
        });
        if (fields.buyer_cnic === false) {
            self.gui.show_popup('error',{
                title: _t('CNIC Required'),
                body:  _t('Customer CNIC is required!'),
            });
            return;
        }
        return this._super(partner);
    },
});*/
});
