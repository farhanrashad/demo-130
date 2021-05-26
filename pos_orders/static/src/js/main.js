/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_orders.pos_orders',function(require){
    "use strict"
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var QWeb = core.qweb;
    var SuperPosModel = models.PosModel.prototype;

    models.load_models([{
            model: 'pos.order',
            fields: ['id', 'name', 'date_order', 'partner_id', 'lines', 'pos_reference','account_move'],
            domain: function(self) {
                var domain_list = [];
                if(self.config.order_loading_options == 'n_days'){
                    var today = new Date();
                    var validation_date = new Date(today.setDate(today.getDate()-self.config.number_of_days)).toISOString();
                    domain_list = [['date_order','>',validation_date],['state', 'not in', ['draft', 'cancel']]];
                }
                else if(self.config.order_loading_options == 'current_session')
                    domain_list = [['session_id', '=', self.pos_session.name], ['state', 'not in', ['draft', 'cancel']]];
                else
                    domain_list = [['state', 'not in', ['draft', 'cancel']]];
                return domain_list;
            },
            loaded: function(self, wk_order) {
                self.db.pos_all_orders = wk_order;
                self.db.order_by_id = {};
                wk_order.forEach(function(order){
                    var order_date = new Date(order['date_order']);
                    var utc = order_date.getTime() - (order_date.getTimezoneOffset() * 60000);
                    order['date_order'] = new Date(utc).toLocaleString();
                    self.db.order_by_id[order.id] = order;
                });
            },
        }, {
            model: 'pos.order.line',
            fields: ['product_id', 'order_id', 'qty','discount','price_unit','price_subtotal_incl','price_subtotal'],
            domain: function(self) {
                var order_lines = []
                var orders = self.db.pos_all_orders;
                for (var i = 0; i < orders.length; i++) {
                    order_lines = order_lines.concat(orders[i]['lines']);
                }
                return [
                    ['id', 'in', order_lines]
                ];
            },
            loaded: function(self, wk_order_lines) {
                self.db.pos_all_order_lines = wk_order_lines;
                self.db.line_by_id = {};
                wk_order_lines.forEach(function(line){
                    self.db.line_by_id[line.id] = line;
                });
            },
        }, ], {
        'after': 'product.product'
    });

    models.PosModel = models.PosModel.extend({
        _save_to_server: function (orders, options) {
            var self = this;
            return SuperPosModel._save_to_server.call(this,orders,options).then(function(return_dict){
                if(return_dict){
                    _.forEach(return_dict, function(data){
                        if(data.orders != null){
                            data.orders.forEach(function(order){
                                if(order.existing)
                                {
                                    self.db.pos_all_orders.forEach(function(order_from_list){
                                        if(order_from_list.id == order.original_order_id)
                                            order_from_list.return_status = order.return_status
                                    });
                                }
                                else{
                                    var order_date = new Date(order['date_order'])
                                    var utc = order_date.getTime() - (order_date.getTimezoneOffset() * 60000);
                                    order['date_order'] = new Date(utc).toLocaleString()
                                    self.db.pos_all_orders.unshift(order);
                                    self.db.order_by_id[order.id] = order;
                                }
                            });

                            data.orderlines.forEach(function(orderline){
                                if(orderline.existing){
                                    var target_line = self.db.line_by_id[orderline.id];
                                    target_line.line_qty_returned = orderline.line_qty_returned;
                                }
                                else{
                                    self.db.pos_all_order_lines.unshift(orderline);
                                    self.db.line_by_id[orderline.id] = orderline;
                                }
                            });
                        
                            if(self.db.all_payments)
                                data.payments.forEach(function(payment) {
                                    self.db.all_payments.unshift(payment);
                                    self.db.payment_by_id[payment.id] = payment;
                            });

                            delete data.orders;
                            delete data.orderlines;
                            delete data.payments;
                        }
                    })
                }
                return return_dict
            });
        }
    });

    var OrdersScreenWidget = screens.ScreenWidget.extend({
        template: 'OrdersScreenWidget',

        init: function(parent, options) {
            this._super(parent, options);
        },
        get_customer: function(customer_id){
            var self = this;
            if(self.gui)
                return self.gui.get_current_screen_param('customer_id');
            else
                return undefined;
        },
        render_list: function(order, input_txt) {
            var self = this;
            var customer_id = this.get_customer();
            var new_order_data = [];
            if(customer_id != undefined){
                for(var i=0; i<order.length; i++){
                    if(order[i].partner_id[0] == customer_id)
                        new_order_data = new_order_data.concat(order[i]);
                }
                order = new_order_data;
            }
            if (input_txt != undefined && input_txt != '') {
                var new_order_data = [];
                var search_text = input_txt.toLowerCase()
                for (var i = 0; i < order.length; i++) {
                    if (order[i].partner_id == '') {
                        order[i].partner_id = [0, '-'];
                    }
                    if (((order[i].name.toLowerCase()).indexOf(search_text) != -1) || ((order[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1)) {
                        new_order_data = new_order_data.concat(order[i]);
                    }
                }
                order = new_order_data;
            }
            var contents = this.$el[0].querySelector('.wk-order-list-contents');
            contents.innerHTML = "";
            var wk_orders = order;
            for (var i = 0, len = Math.min(wk_orders.length, 1000); i < len; i++) {
                var wk_order = wk_orders[i];
                var orderline_html = QWeb.render('WkOrderLine', {
                    widget: this,
                    order: wk_orders[i],
                    customer_id:wk_orders[i].partner_id[0],
                });
                var orderline = document.createElement('tbody');
                orderline.innerHTML = orderline_html;
                orderline = orderline.childNodes[1];
                contents.appendChild(orderline);
            }
        },
        show: function() {
            var self = this;
            this._super();
            var orders = self.pos.db.pos_all_orders;
            this.render_list(orders, undefined);
            this.$('.order_search').keyup(function() {
                self.render_list(orders, this.value);
            });
            this.$('.back').on('click',function() {
                self.gui.show_screen('products');
            });
        },
        close: function() {
            this._super();
            this.$('.wk-order-list-contents').undelegate();
        },
    });
    gui.define_screen({name: 'wk_order',widget:OrdersScreenWidget});

    screens.ClientListScreenWidget.include({
        show: function() {
            var self = this;
            self._super();
            $('.view_all_order').on('click',function() {
                self.gui.show_screen('wk_order',{
                    'customer_id':this.id
                });
            });
        }
    });
    var button_all_order = screens.ActionButtonWidget.extend({
        template: 'button_all_order',
        init: function (parent, options) {
            this._super(parent, options);
        },
        button_click: function () {
            this.gui.show_screen('wk_order',{});
        }
    });
    screens.define_action_button({
        'name': 'button_all_order',
        'widget': button_all_order,
        'condition': function () {
            return true/*this.pos.config.orderline_note*/;
        }
    });  
    return OrdersScreenWidget;
});
