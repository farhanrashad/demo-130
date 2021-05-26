odoo.define('sh_pos_receipt.pos_receipt_invoice_number', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var rpc = require('web.rpc');
var core = require('web.core');
var models = require('point_of_sale.models');
var QWeb = core.qweb;
var chrome = require('point_of_sale.chrome');
models.load_fields('product.product', ['variant_name']);
models.load_fields('res.company', ['pos_logo']);

chrome.Chrome.include({
    build_chrome: function() { 
        var self = this;
        this._super();
        if (this.pos.company.pos_logo !== false) {
            var url = window.location.origin + '/web/image?model=res.company&field=pos_logo&id='+self.pos.company.id;
            $('.pos-logo').attr("src", url);
        }
    },
});

screens.ReceiptScreenWidget.include({
    handle_auto_print: function() {
        var self = this;
        setTimeout(function(){
            if (self.should_auto_print() && !self.pos.get_order().is_to_email()) {
                self.print();
                if (self.should_close_immediately()){
                    self.click_next();
                }
            } else {
                self.lock_screen(false);
            }
        },3000);
    },
});
var _super_Order_line = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
    export_for_printing: function () {
        var res = _super_Order_line.export_for_printing.apply(this, arguments);
        if (this.get_product().default_code !== false) {
            res['default_code'] = this.get_product().default_code || ''
        }
        var taxes = this.get_taxes();
        var tax_amount_total = 0;
        _.each(taxes, function(tax){
            tax_amount_total += tax.amount;
        })
        res['variant_name'] = this.get_product().variant_name;
        res['tax_amount_total'] = tax_amount_total;
        var line_discount = this.get_unit_price() * (this.get_discount()/100) * 1;
        res['line_discount'] = line_discount
        return res;
    },
})
var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        /*get_total_disc: function() {
            var total_disc = 0;
            this.orderlines.each(function(line){
                if (line.price > 0) {
                    total_disc += line.price;
                }
            });
            return total_disc
        },*/
        get_total_qty: function() {
            var total_qty = 0;
            this.orderlines.each(function(line){
                total_qty += line.quantity;
            });
            return total_qty
        },
        export_for_printing: function () {
            var res = _super_Order.export_for_printing.apply(this, arguments);
            var client  = this.get('client');
            var self = this;
            var canvas = document.createElement('canvas');
            JsBarcode(canvas, res['name']);
            res['barcode'] = canvas.toDataURL("image/png");
            var shop_address = {}
            if (this.pos.pos_shops) {
                _.each(this.pos.pos_shops, function(shop){
                    if (self.pos.config.shop_id[0] === shop.id){
                        shop_address['name'] = shop.name;
                        shop_address['street'] = shop.street;
                        shop_address['street2'] = shop.street2;
                        shop_address['city'] = shop.city;
                        shop_address['zip'] = shop.zip;
                        shop_address['state'] = shop.state_id[1];
                        shop_address['country'] = shop.country_id[1];
                        shop_address['website'] = shop.website;
                        shop_address['phone'] = shop.phone;
                        shop_address['email'] = shop.email;
                    }
                })
            }
            res['shop_image'] = 'data:image/png;base64,'+this.pos.company.pos_logo;
            res['total_qty'] = this.get_total_qty();
            res['shop_address'] = shop_address;
            /*res['total_disc'] = this.get_total_disc() - res['total_without_tax'];*/
            /*res['total_disc'] = this.get_total_discount();*/
            /*res['barcode_url'] = "/report/barcode/?type=EAN13&value='"+res['name']+"'&width=250&height=50";*/
            res['client_phone'] = client ? client.phone : null
            return res;
        },
    });
});