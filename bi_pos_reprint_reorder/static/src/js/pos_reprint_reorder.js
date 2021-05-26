// pos_reprint_reorder js
//console.log("custom callleddddddddddddddddddddd")
odoo.define('pos_reprint_reorder.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var ActionManagerBrowseinfo = require('web.ActionManager');
	var PaymentScreenWidget = screens.PaymentScreenWidget;
	var QWeb = core.qweb;
	var rpc = require('web.rpc');
	var pos_orders_list = require('pos_orders_list.pos_orders_list');

	var _t = core._t;


 var ReceiptScreenWidgetNew = screens.ScreenWidget.extend({
	   template: 'ReceiptScreenWidgetNew',
		show: function() {
			var self = this;
			self._super();
			$('.button.back').on("click", function() {
				self.gui.show_screen('see_orders_screen_widget');
			});
			$('.button.print').click(function() {
				var test = self.chrome.screens.receipt;
				setTimeout(function() { self.chrome.screens.receipt.lock_screen(false); }, 1000);
				if (!test['_locked']) {
					self.chrome.screens.receipt.print_web();
					self.chrome.screens.receipt.lock_screen(true);
				}
			});
		}
	});
	gui.define_screen({ name: 'ReceiptScreenWidgetNew', widget: ReceiptScreenWidgetNew });


	// pos_orders_list start

	pos_orders_list.include({
	
		show: function(options) {
			var self = this;
			this._super(options);

			this.details_visible = false;
			var ordr = this.pos.get_order();
			
			// Re-Order Code
			this.$('.orders-list-contents').delegate('.re-order', 'click', function(result) {
				
				var order_id = parseInt(this.id);
				var orders =  self.pos.get('all_orders_list');
				var selectedOrder = null;
				for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
					if (orders[i] && orders[i].id == order_id) {
						selectedOrder = orders[i];
					}
				}
				var orderlines = [];
				var order_line_data = self.pos.get('all_orders_line_list');

				selectedOrder.lines.forEach(function(line_id) {
					for(var y=0; y<order_line_data.length; y++){
						if(order_line_data[y]['id'] == line_id){
						   orderlines.push(order_line_data[y]); 
						}
					}
					
				});

				self.gui.show_popup('pos_re_order_popup_widget', { 'orderlines': orderlines, 'order': selectedOrder });
			});

			self.$('.orders-list-contents').delegate('.print-order2', 'click', function(result) {
				result.stopImmediatePropagation();
				var order_id = parseInt(this.id);
				var orderlines = [];
				var paymentlines = [];
				var discount = 0;
				var subtotal = 0;
				var tax = 0;
				var barcode_img;
				var orders =  self.pos.get('all_orders_list');

				var selectedOrder = null;
				for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
					if (orders[i] && orders[i].id == order_id) {
						selectedOrder = orders[i];
					}
				}
				rpc.query({
					model: 'pos.order',
					method: 'print_pos_receipt',
					args: [order_id],
				
				}).then(function(output) {
					orderlines = output[0];
					paymentlines = output[2];
					discount = output[1];
					subtotal = output[4];
					tax = output[5];
					barcode_img = output[6];
					self.gui.show_screen('ReceiptScreenWidgetNew');
					$('.pos-receipt-container').html(QWeb.render('OrderReceipt2',{
						widget:self,
						order: selectedOrder,
						paymentlines: paymentlines,
						orderlines: orderlines,
						discount_total: discount,
						change: output[3],
						subtotal: subtotal,
						tax: tax,
						barcode_img:barcode_img,
					}));
					if (self.should_auto_print()) {
						// window.print();
						setTimeout(function(){
							window.print();
							return;
						}, 500);
					}
				});
				return;
			});

		},
		
		should_auto_print: function() {
			return this.pos.config.iface_print_auto && !this.pos.get_order()._printed;
		},
	});

	// End pos_orders_list



	// PosReOrderPopupWidget Popup start

	var PosReOrderPopupWidget = popups.extend({
		template: 'PosReOrderPopupWidget',
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
				
			var reorder_products = {};

			this.$('#apply_reorder').click(function() {
				var entered_code = $("#entered_item_qty").val();
				var list_of_qty = $('.entered_item_qty');

				$.each(list_of_qty, function(index, value) {
					var entered_item_qty = $(value).find('input');
					var qty_id = parseFloat(entered_item_qty.attr('qty-id'));
					var line_id = parseFloat(entered_item_qty.attr('line-id'));
					var entered_qty = parseFloat(entered_item_qty.val());
					reorder_products[line_id] = entered_qty;
				});
				//return reorder_products;


				Object.keys(reorder_products).forEach(function(line_id) {
					
					//#########################################################################################
					
					var orders_lines = self.pos.get('all_orders_line_list');
					var orderline = [];
					
						for(var n=0; n < orders_lines.length; n++){
						if (orders_lines[n]['id'] == line_id){
							if(reorder_products[line_id]>0)
							{
								var product = self.pos.db.get_product_by_id(orders_lines[n].product_id[0]);
								selectedOrder.add_product(product, {
									quantity: parseFloat(reorder_products[line_id]),
									price: orders_lines[n].price_unit,
									discount: orders_lines[n].discount
								});
								selectedOrder.selected_orderline.original_line_id = orders_lines[n].id;
							}
						}
					}
				  
					
				});
				selectedOrder.set_client(client);
				self.pos.set_order(selectedOrder);
				self.gui.show_screen('products');

			   });
		},

	});
	gui.define_popup({
		name: 'pos_re_order_popup_widget',
		widget: PosReOrderPopupWidget
	});

	// End PosReOrderPopupWidget Popup start



});
