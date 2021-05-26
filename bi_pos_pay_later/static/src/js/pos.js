odoo.define('bi_pos_pay_later.pos', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var rpc = require('web.rpc');
	var session = require('web.session');
	var chrome = require('point_of_sale.chrome');
	var field_utils = require('web.field_utils');
	var QWeb = core.qweb;
	var _t = core._t;
	var PosDB = require('point_of_sale.DB');
	var utils = require('web.utils');
	var round_di = utils.round_decimals;
	var round_pr = utils.round_precision;
	var import_pos_orders_list = require('pos_orders_list.pos_orders_list');

	PosDB.include({
		get_unpaid_orders: function(){
			var saved = this.load('unpaid_orders',[]);
			var orders = [];
			for (var i = 0; i < saved.length; i++) {
				if('barcode' in saved[i].data)
				{
					orders.push(saved[i].data);
				}
			}
			return orders;
		},
	});


	var posorder_super = models.Order.prototype;
	models.Order = models.Order.extend({

		initialize: function(attr,options) {
			var self = this;
			this.is_partial    = false;
			this.is_paying_partial    = false;
			this.amount_due    = 0;
			this.amount_paid    = 0;
			this.is_draft_order = false;
			this.set_is_partial();
			posorder_super.initialize.call(this,attr,options);
		},


		init: function(parent, options) {
			var self = this;
			this._super(parent,options);
			this.set_is_partial();
		},
		
		set_is_partial: function(set_partial){
			this.is_partial = set_partial || false;
			this.trigger('change',this);
		},

		generate_unique_id: function() {
			return Math.floor(1000000000 + Math.random() * 9000000000)
		},

		export_as_JSON: function(){
			var loaded = posorder_super.export_as_JSON.apply(this, arguments);
			loaded.is_partial = this.is_partial || false;
			loaded.amount_due = this.get_partial_due();
			loaded.is_paying_partial = this.is_paying_partial;
			loaded.is_draft_order = this.is_draft_order || false;
			return loaded;
		},

		get_partial_due: function () {
			return this.amount_due;
		},

	});

	screens.OrderWidget.include({
		rerender_orderline: function(order_line){
			if(order_line.order.is_paying_partial == false)
			{
				var node = order_line.node;
				var replacement_line = this.render_orderline(order_line);
				node.parentNode.replaceChild(replacement_line,node);
			}
		},
	});


	import_pos_orders_list.include({

		init: function(parent, options) {
			this._super(parent, options);
			//this.options = {};
		},
		
		get_orders_fields: function () {
			var self = this;
			this._super();
			var fields = ['is_partial','amount_due','amount_paid','name', 'id', 'date_order', 'partner_id', 'pos_reference', 'lines', 'amount_total', 'session_id', 'state', 'company_id','pos_order_date','barcode','barcode_img'];
			return fields;
		},

		render_list_orders: function(orders, search_input){
			var self = this;
			this._super(orders,search_input);
			if(orders == undefined)
			{
				orders = self.pos.get('all_orders_list');
			}
			var selected_partner_id = this.get_selected_partner();
			var selected_client_orders = [];
			if (selected_partner_id != undefined) {
				for (var i = 0; i < orders.length; i++) {
					if (orders[i].partner_id[0] == selected_partner_id)
						selected_client_orders = selected_client_orders.concat(orders[i]);
				}
				orders = selected_client_orders;
			}
			
			if (search_input != undefined && search_input != '') {
				var selected_search_orders = [];
				var search_text = search_input.toLowerCase()
				for (var i = 0; i < orders.length; i++) {
					if (orders[i].partner_id == '') {
						orders[i].partner_id = [0, '-'];
					}
					if(orders[i].partner_id[1] == false)
					{
						if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].state.toLowerCase()).indexOf(search_text) != -1)  || ((orders[i].pos_reference.toLowerCase()).indexOf(search_text) != -1)) {
						selected_search_orders = selected_search_orders.concat(orders[i]);
						}
					}
					else
					{
						if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].state.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].pos_reference.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1)) {
						selected_search_orders = selected_search_orders.concat(orders[i]);
						}
					}
				}
				orders = selected_search_orders;
			}
			
			var content = this.$el[0].querySelector('.orders-list-contents');
			content.innerHTML = "";
			var orders = orders;
			var current_date = null;
			if(orders){
				for(var i = 0, len = Math.min(orders.length,1000); i < len; i++){
					var order    = orders[i];
					current_date =  field_utils.format.datetime(moment(order.date_order), {type: 'datetime'});
					var ordersline_html = QWeb.render('OrderLines',{widget: this, order:orders[i], selected_partner_id: orders[i].partner_id[0],current_date:current_date});
					var ordersline = document.createElement('tbody');
					ordersline.innerHTML = ordersline_html;
					ordersline = ordersline.childNodes[1];
					content.appendChild(ordersline);
				}
			}
		},
		
		show: function(options){
			var self = this;
			this._super(options);
			var selectedOrder;
			var client = false;
			var state = null;
			
			$('#filter_order').html('');
			$('#filter_state').html('');

			$('.refresh-order').on('click',function () {
				$('.search-order input').val('');
				var params = self.pos.get_order().get_screen_data('params');
				if(params && params['selected_partner_id'])
				{
					params['selected_partner_id'] = undefined;
				}
				self.get_pos_orders();
				$('#filter_order').html('');
				$('#filter_state').html('');
			});

			$('.state').each(function(){
				$(this).on('click',function () {
					state = $(this).attr('id');
					$('#filter_order').html('Filter By:');
					$('#filter_state').html($(this).text());
					self.render_list_orders(self.pos.get('all_orders_list'),state);
				});
			});

			this.$('.orders-list-contents').delegate('.pay-order','click',function(event){
				var old_order = self.pos.get_order();
				var order_id = parseInt(this.id);
				var new_order = [];
				var orders =  self.pos.get('all_orders_list');
				var orders_lines =  self.pos.get('all_orders_line_list');

				self.remove_current_orderlines(old_order);
				rpc.query({
					model: 'pos.order',
					method: 'search_read',
					domain: [['id', '=', order_id]],
				}, {async: false}).then(function(output) {
					if(output && output[0])
					{
						new_order = output[0];
					}
					if(new_order)
					{
						self.remove_current_orderlines(old_order);
						old_order.finalized = false;
						old_order.name = new_order.pos_reference;
						old_order.is_partial = new_order.is_partial;
						old_order.amount_due = new_order.amount_due;
						old_order.barcode = new_order.barcode;
						old_order.barcode_img = new_order.barcode_img;
						old_order.is_paying_partial = true;
						old_order.amount_paid  = new_order.amount_paid;

						if (new_order.partner_id) {
							var client = self.pos.db.get_partner_by_id(new_order.partner_id[0]);
							old_order.set_client(client);
						}
						for (var i = 0; i < new_order.lines.length; i++) {
							for(var n=0; n < orders_lines.length; n++){
								if (orders_lines[n]['id'] == new_order.lines[i]){
									var product = self.pos.db.get_product_by_id(orders_lines[n].product_id[0]);
									old_order.add_product(product, {
										quantity: parseFloat(orders_lines[n].qty),
										price: orders_lines[n].price_unit,
										discount: orders_lines[n].discount
									});
								}
							}
						}
						if(new_order.amount_due > 0)
						{
							rpc.query({
								model: 'product.product',
								method: 'search_read',
								domain: [['default_code', '=', 'DUEA001']],
								fields: ['id'],
								limit: 1,
							}, {async: false}).then(function(output) {
								if(output)
								{
									var is_added = false
									if (old_order !== null) {
										for(var i = 0; i < old_order.orderlines.models.length; i++){
											if (old_order.orderlines.models[i].product.default_code === "DUEA001"){
												is_added = true;
												break;
											}
										}
									}
									var product_for_due = self.pos.db.get_product_by_id(output[0]['id']);
									if (!is_added) {
										old_order.add_product(product_for_due,{
											quantity: 1.0,
											price: -new_order.amount_paid,
											discount: 0
										});
									}
								}
							});
						}
						self.gui.show_screen('payment');
					}
				});
			});
		},

		remove_current_orderlines: function(old_order){
			var orderlines = old_order.get_orderlines();
			if(orderlines.length > 0){
				old_order.remove_orderline(orderlines);
			}
		},
	});

	screens.PaymentScreenWidget.include({
		show: function() {
			var self = this;
			this._super();
			var order = this.pos.get_order();
			var orderlines = order.get_orderlines();
			
			this.$('.pay-partial').click(function(){
				if(order.is_paying_partial == false)
				{
					self.partial_order();
				}
			});
		},
		order_changes: function(){
			var self = this;
			this._super();
			var order = this.pos.get_order();
			if(!order){
				return
			} else if(order.get_due() == 0 || order.get_due() == order.get_total_with_tax() || order.get_total_paid() >= order.get_total_with_tax() ){
				self.$('.pay-partial').removeClass('highlight');
			} else {
				if(order.is_paying_partial == false)
				{
					self.$('.pay-partial').addClass('highlight');
				}
			}
		},
		// click_back: function(){
		// 	var self  = this;
		// 	var order = this.pos.get_order(); 
		// 	if(order.is_paying_partial)
		// 	{
		// 		self.payment_deleteorder();
		// 	}
		// 	else{
		// 		this.gui.show_screen('products');
		// 	}
		// },

		click_set_customer: function(){
			var order = this.pos.get_order(); 
			if (order.is_paying_partial){
				this.gui.show_popup('error',{
					'title': _t('Not Allowed'),
					'body': _t("You cannot change customer of draft order"),
				});
			} else {
				this.gui.show_screen('clientlist');
			}
		},

		payment_deleteorder: function() {
			var self  = this;
			var order = this.pos.get_order(); 
			if (!order) {
				return;
			} else if ( !order.is_empty() ){
				this.gui.show_popup('confirm',{
					'title': _t('Cancel Payment ?'),
					'body': _t("Are you sure,You want to Cancel this payment?"),
					confirm: function(){
						self.pos.delete_current_order();
					},
				});
			} else {
				this.pos.delete_current_order();
			}
		},
		partial_order: function () {
			var self = this;
			var order = this.pos.get_order();
			var orderlines = order.get_orderlines();
			var partner_id = order.get_client();
			if (!partner_id){
				self.gui.show_popup('error',{
					'title': _t('Unknown customer'),
					'body': _t('You cannot perform partial payment. Select customer first.'),
				});
				return;
			}
			else if(orderlines.length === 0){
				self.gui.show_popup('error',{
					'title': _t('Empty Order'),
					'body': _t('There must be at least one product in your order before it can be validated.'),
				});
				return;
			}
			else{
				if(order.get_total_with_tax() !== order.get_total_paid() && order.get_total_paid() != 0){
					order.is_partial = true;
					order.amount_due = order.get_due();
					order.set_is_partial(true);
					order.to_invoice = false;
					order.finalized = false;
					self.pos.push_order(order);
					self.gui.show_screen('receipt');					
				}
			}
		},
	});


	var CreatePOSDraftButtonWidget = screens.ActionButtonWidget.extend({
		template: 'CreatePOSDraftButtonWidget',

		button_click: function() {
			var self = this;
			var order = this.pos.get_order();
			var orderlines = order.get_orderlines();
			var partner_id = order.get_client();
			if (!partner_id){
				self.gui.show_popup('error',{
					'title': _t('Unknown customer'),
					'body': _t('Select customer first.'),
				});
				return;
			}
			else if(orderlines.length === 0){
				self.gui.show_popup('error',{
					'title': _t('Empty Order'),
					'body': _t('There must be at least one product in your order before it can be validated.'),
				});
				return;
			}
			else{
				if(order.get_total_with_tax() !== order.get_total_paid()){
					order.amount_due = order.get_due();
					order.is_draft_order = true;
					order.is_partial = true;
					self.pos.push_order(order);
					self.gui.show_screen('receipt');					
				}
			}
		},
		
	});

	screens.define_action_button({
		'name': 'Creat Darft Order Button Widget',
		'widget': CreatePOSDraftButtonWidget,
		'condition': function() {
			return true;
		},
	});

});
