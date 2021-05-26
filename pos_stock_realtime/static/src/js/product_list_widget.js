odoo.define('pos_stock_realtime.product_list_widget', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var task;
    var core = require('web.core');
    var _t = core._t;

    screens.ProductListWidget.include({
        init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.click_product_handler = function(){
                var product = self.pos.db.get_product_by_id(this.dataset.productId);
                var product_qty = parseInt(self.pos.db.qty_by_product_id[product.id]);
                if (self.pos.config.allow_out_of_stock && (product_qty <= 0) || !product_qty) {
                    self.gui.show_popup('error',{
                        'title': _t('Warning'),
                        'body': _t('You have selected an item which has Zero or Negative Stock On Hand'),
                    });
                }
                options.click_product_action(product);
            }
        },
        render_product: function (product) {
            if (this.pos.config.show_qty_available && product.type !== 'product') {
                this.pos.db.qty_by_product_id[product.id] = false;
            }
            return this._super(product);
        },
        renderElement: function () {
            this._super();
            var self = this;
            var done = $.Deferred();
            clearInterval(task);
            task = setTimeout(function () {
                if (self.pos.config.show_qty_available) {
                    self.pos.refresh_qty();
                } else {
                    $(self.el).find('.qty-tag').hide();
                }
                done.resolve();
            }, 100);
            return done;
        }
    });
});