odoo.define('pos_barcode.pos_barcode', function(require) {
	"use strict";
	var screens = require('point_of_sale.screens');
	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var core = require('web.core');
	var popups = require('point_of_sale.popups');
	var rpc = require('web.rpc');
	
	var _t = core._t;

	models.load_models({
		model: 'pos.order',
		fields: ['name', 'id', 'return_id', 'date_order', 'partner_id', 'pos_reference', 'lines', 'amount_total','amount_tax','session_id', 'state', 'company_id','barcode'],
		loaded: function(self, orders){
			self.db.all_orders_list = orders;
			self.db.get_orders_by_id = {};
			orders.forEach(function(order) {
				self.db.get_orders_by_id[order.id] = order;
			});
			self.orders = orders;
		},
	});
	//
	models.load_models({
		model: 'pos.order.line',
		fields: ['order_id', 'product_id', 'discount', 'qty', 'return_qty', 'price_unit'],
		domain: function(self) {
			var order_lines = []
			var orders = self.db.all_orders_list;
			for (var i = 0; i < orders.length; i++) {
				order_lines = order_lines.concat(orders[i]['lines']);
			}
			return [
				['id', 'in', order_lines]
			];
		},
		loaded: function(self, pos_order_line) {
			self.db.all_orders_line_list = pos_order_line;
			self.db.get_lines_by_id = {};
			pos_order_line.forEach(function(line) {
				self.db.get_lines_by_id[line.id] = line;
			});

			self.pos_order_line = pos_order_line;
		},
	});
	//
	var _super_order = models.Order.prototype;
	models.Order = models.Order.extend({
		initialize: function(attr, options) {
			this.barcode = this.barcode || "";
			this.set_barcode();
			_super_order.initialize.call(this,attr,options);
		},
		set_barcode: function(){
			var self = this;
			rpc.query({
					model: 'pos.order',
					method: 'get_barcode',
					args: [1,this['uid']],
				}, {async: false}).then(function(output) {
					if(output)
					{
						self.barcode = output[0];
					}
			});
		},
		export_as_JSON: function() {
			var json = _super_order.export_as_JSON.apply(this,arguments);
			json.barcode = this.barcode;
			json.return_id = this.return_id;
			return json;
		},
	});
	//
	var PosBarcodePopupWidget = popups.extend({
		template: 'PosBarcodePopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		show: function(options) {
			options = options || {};
			var self = this;
			this._super(options);
		},
		events: {
			'click .button.cancel': 'click_cancel',
		},
		renderElement: function() {
			var self = this;
			this._super();
			var self = this;   
			var selectedOrder = this.pos.get_order();
			var orderlines = self.options.orderlines;
			var order = self.options.order;
			var return_products = {};
			var exact_return_qty = {};
			var exact_entered_qty = {};
			var orders = self.pos.db.all_orders_list;
			
			this.$('#apply_barcode_return_order').click(function() {
					var entered_barcode = $("#entered_item_barcode").val();
					var order_id = parseInt(this.id);
					var selectedOrder = null;
					for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
						if (orders[i] && orders[i].barcode == entered_barcode) {
							selectedOrder = orders[i];
						}
					}
					if(selectedOrder){
						var orderlines = [];
						var order_list = self.pos.db.all_orders_list;
						var order_line_data = self.pos.db.all_orders_line_list;

						selectedOrder.lines.forEach(function(line_id) {
					
						for(var y=0; y<order_line_data.length; y++){
							if(order_line_data[y]['id'] == line_id){
							   orderlines.push(order_line_data[y]);
							}
						}
						});
						self.gui.show_popup('pos_return_order_popup_widget', { 'orderlines': orderlines, 'order': selectedOrder });
					}
					else{
						self.pos.gui.show_popup('error', {
							'title': _t('Invalid Barcode'),
							'body': _t("The Barcode You are Entering is Invalid"),
						});
					}
			});
		},

	});
	//
	screens.PaymentScreenWidget.include({
		// Include auto_check_invoice boolean condition in watch_order_changes method
		validate_order: function(force_validation) {
        	this._super();
			var self = this;
        	var order = this.pos.get_order();
        	var current_order_lines = order.orderlines.models;
			var order_lines = this.pos.db.all_orders_line_list;
			if (order.return_id !== undefined) {
				_.each(order_lines, function(line){
					if (line.order_id[0] == order.return_id) {
						for(var i = 0 ; i<current_order_lines.length ; i++){
							if (current_order_lines[i].product.id === line.product_id[0]) {
								if (line['return_qty'] === undefined) {
						   			line.return_qty = 0;
					   			}
					   			line.return_qty += -parseFloat(current_order_lines[i].quantity);
							}
						}
					}
				})
			}
		},
	
	});
	//
	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		_save_to_server: function(orders, options) {
			var self = this;
			return _super_posmodel._save_to_server.call(this, orders, options).then(function(new_orders) {
				if (new_orders != null) {
					new_orders.forEach(function(order) {
						if (order) {
							rpc.query({
								model: 'pos.order',
								method: 'return_new_order',
								args: [order['id']],
								}).then(function(output) {
									self.db.all_orders_list.unshift(output);
									self.db.get_orders_by_id[order['id']] = order;
									var lines = output['order_lines'];
									for(var i=0; i < lines.length; i++){
										self.db.all_orders_line_list.unshift(lines[i]);
									}
							});
						}
					});
				}
				return new_orders;
			});
		}
		
	});
	//
	var PosReturnOrderPopupWidget = popups.extend({
		template: 'PosReturnOrderPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		//
		show: function(options) {
			options = options || {};
			var self = this;
			this._super(options);
			this.orderlines = options.orderlines || [];

		},
		//
		renderElement: function() {
			var self = this;
			this._super();
			var selectedOrder = this.pos.get_order();
			var orderlines = self.options.orderlines;
			var order = self.options.order;

			// When you click on apply button, Customer is selected automatically in that order 
			var partner_id = false
			var client = false
			if (order && order.partner_id != null)
				partner_id = order.partner_id[0];
				client = this.pos.db.get_partner_by_id(partner_id);
				
			var return_products = {};
			this.$('#apply_select_all').click(function(e) {
				var select_all = false;
				$.each($('.entered_item_qty'), function(index, value) {
					var line = $(value).find('input');
					if (parseFloat(line.val()) && select_all === false) {
						select_all = true;
					}
					var purchased_qty = parseFloat(line.attr('qty-id'));
					var return_qty = parseFloat(line.attr('return-qty')) || 0;
					if (select_all === true) {
						line.val('');	
					} else {
						line.val(purchased_qty - return_qty);
					}
				});
			});
			this.$('#apply_return_order').click(function() {
				var entered_code = $("#entered_item_qty").val();
				var list_of_qty = $('.entered_item_qty');
				var return_possible = true;

				$.each(list_of_qty, function(index, value) {
					var entered_item_qty = $(value).find('input');
					var exact_return_qty = parseFloat(entered_item_qty.attr('qty-id'));
					var return_qty = parseFloat(entered_item_qty.attr('return-qty')) || 0;
					var line_id = parseFloat(entered_item_qty.attr('line-id'));
					var exact_entered_qty = parseFloat(entered_item_qty.val()) || 0;
					
					if(!exact_entered_qty){
						return;
					}
					else if (exact_entered_qty % 1){
					    return_possible = false;
					    alert("Invalid Return quantity!");
					    return false;
					}
					else if (exact_return_qty >= (return_qty + exact_entered_qty)){
					  return_products[line_id] = exact_entered_qty;
					}
					else{
						return_possible = false;
						alert("Cannot Return More quantity than purchased");
						return false;
					}

				});
				//return return_products;
				if (return_possible) {
					Object.keys(return_products).forEach(function(line_id) {
						var orders_lines = self.pos.db.all_orders_line_list;
						var orderline = [];
					   	for(var n=0; n < orders_lines.length; n++){
						   	if (orders_lines[n]['id'] == line_id){
								var product = self.pos.db.get_product_by_id(orders_lines[n].product_id[0]);
								selectedOrder.add_product(product, {
									quantity: - parseFloat(return_products[line_id]),
									price: orders_lines[n].price_unit,
									discount: orders_lines[n].discount
								});
								selectedOrder.selected_orderline.original_line_id = orders_lines[n].id;
						   }
					   	}
					});
					if (Object.keys(return_products).length > 0) {
						selectedOrder.set_client(client);
						self.pos.set_order(selectedOrder);
						selectedOrder['return_id'] = order.id;
						self.gui.show_screen('products');
					}
				}
				else {
					self.gui.show_screen('products');
				}
		   });
		},

	});
	//
	gui.define_popup({
		name: 'pos_return_order_popup_widget',
		widget: PosReturnOrderPopupWidget
	});
	//
	var POSBarcodeReturnWidget = screens.ActionButtonWidget.extend({
		template: 'POSBarcodeReturnWidget',

		button_click: function() {
			var self = this;
			this.gui.show_popup('pos_barcode_popup_widget', {});
		},
	});
	//
	screens.define_action_button({
		'name': 'POS Return Order with Barcode',
		'widget': POSBarcodeReturnWidget,
		'condition': function() {
			return true;
		},
	});
	//
	gui.define_popup({
		name: 'pos_barcode_popup_widget',
		widget: PosBarcodePopupWidget
	});
});
