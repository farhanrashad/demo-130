odoo.define('pos_check_stock.pos_check_stock', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var QWeb = core.qweb;
	var rpc = require('web.rpc');
	
	var _t = core._t;

	var CheckStockWidget = screens.ActionButtonWidget.extend({
		template: 'CheckStockWidget',
		button_click: function() {
			var order = this.pos.get_order();
			var self = this;
			var order = this.pos.get_order();
			if (!order.get_orderlines().length) {
                this.pos.gui.show_popup('error',{
					'title': _t('Empty Order'),
					'body': _t('Product cart is empty.'),
				});
				return;
			}
			var product_id = order.get_selected_orderline().product.id;
			var config_id = this.pos.config.id;
			rpc.query({
					model: 'product.product',
					method: 'get_stock_data',
					args: [product_id, config_id],
				}, {async: false}).then(function(output) {
					self.gui.show_popup('open_stock_popup_widget', {'stock_lines': output});
			});
		},
	});
	screens.define_action_button({
		'name': 'POS check stock inventory',
		'widget': CheckStockWidget,
		'condition': function() {
			return this.pos.config.check_stock;
		},
	});
	var StockPopupWidget = popups.extend({
		template: 'StockPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		show: function(options) {
			var self = this;
			this._super(options);
			this.stock_lines = options.stock_lines || [];
		},
		check_access_rights: function() {
			var user_id = this.pos.get_cashier().user_id[0]
			var self = this;
			rpc.query({
				model: 'res.users',
				method: 'check_coupon_rights',
				args: [user_id],
			}).then(function(output) {
				if (!output){
					self.gui.show_popup('error', {
						'title': _t('Access Denied'),
						'body': _t("You have not enough access to create coupon!"),
					});
					return false
				}
				self.gui.close_popup();
				self.gui.show_popup('create_coupon_popup_widget',{});
			})
		},
		renderElement: function() {
			var self = this;
			this._super();
			var order = this.pos.get_order();
			var selectedOrder = self.pos.get('selectedOrder');
			this.$('.creat_coupon').click(function() {
				self.check_access_rights()
			})
			this.$('.select_coupon').click(function() {
				self.gui.close_popup();
				self.gui.show_popup('select_existing_popup_widget', {});
			})
		}
	})
	gui.define_popup({
		name: 'open_stock_popup_widget',
		widget: StockPopupWidget
	});
});
