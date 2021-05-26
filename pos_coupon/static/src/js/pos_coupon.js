odoo.define('pos_coupon.pos_coupon', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var QWeb = core.qweb;
	var rpc = require('web.rpc');
	
	var _t = core._t;

	models.load_models({
		model: 'pos.gift.coupon',
		fields: ['name','apply_coupon_on', 'c_barcode', 'user_id', 'issue_date', 'expiry_date', 'partner_id', 'order_ids', 'active', 'amount', 'description','used','coupon_count', 'coupon_apply_times','expiry_date','partner_true','partner_id'],
		domain: null,
		loaded: function(self, pos_gift_coupon) { 
			self.pos_gift_coupon = pos_gift_coupon;    
		},
	});
	
	models.load_models({
		model: 'pos.coupons.setting',
		fields: ['name', 'product_id', 'min_coupan_value', 'max_coupan_value', 'max_exp_date', 'default_name', 'default_value', 'default_availability', 'active'],
		domain: null,
		loaded: function(self, pos_coupons_setting) { 
			self.pos_coupons_setting = pos_coupons_setting;
		},
	});
	var PrintCouponButtonScreen = screens.ScreenWidget.extend({
		template: 'PrintCouponButtonScreen',
		
		init: function(parent,options){
			var self = this;
			this._super(parent,options);
		},
		

		get_coupon: function(){
			return this.gui.get_current_screen_param('data');
		},

		show: function(options){
			this._super();
			var self = this;
			this.coupon_render();
		},

		coupon_render_env: function() {
			// var order = this.pos.get_order();
			var data = this.pos.get('coupon_print_data');
			return {
				widget: this,
				pos: this.pos,
				summery: this.get_coupon(),
			};
		},

		coupon_render: function(){
			this.$('.print-coupon-receipt').html(QWeb.render('CouponPrint',this.coupon_render_env()));
		},
		print_xml_coupon: function() {
			var receipt = QWeb.render('CouponPrint', this.coupon_render_env());
			this.pos.proxy.print_receipt(receipt);
		},
		print_web_payment: function() {
			window.print();
		},
		print_coupon: function() {
			var self = this;
			if (!this.pos.config.iface_print_via_proxy) { 

				this.print_web_payment();
			} else {    
				this.print_xml_coupon();
			}
		},


		renderElement: function() {
			var self = this;
			this._super();
			
			this.$('.next').click(function(){
				// location.reload();
				self.gui.back();
			});
			
			this.$('.button.print-coupon').click(function(){
				self.print_coupon();
			});
			
		},

	});
	gui.define_screen({name:'coupon_print', widget: PrintCouponButtonScreen});
	var SelectExistingPopupWidget = popups.extend({
		template: 'SelectExistingPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		//
		renderElement: function() {
			var self = this;
			this._super();
			var order = this.pos.get_order();
			var selectedOrder = self.pos.get('selectedOrder');
			this.$('#apply_coupon_code').click(function() {
				var entered_code = $("#existing_coupon_code").val();
				var partner_id = false;
				var coupon_applied = true;
				var used = false;
				if (order.get_client() != null)
					partner_id = order.get_client();
				rpc.query({
					model: 'pos.gift.coupon',
					method: 'existing_coupon',
					args: [partner_id, entered_code],
				
				}).then(function(output) {
					var orderlines = order.orderlines;
					// Popup Occurs when no Customer is selected...
					if (!partner_id) {
						self.gui.show_popup('error', {
							'title': _t('Unknown customer'),
							'body': _t('You cannot use Coupons/Gift Voucher. Select customer first.'),
						});
						return;
					}

					// Popup Occurs when not a single product in orderline...
					if (orderlines.length === 0) {
						self.gui.show_popup('error', {
							'title': _t('Empty Order'),
							'body': _t('There must be at least one product in your order before it can be apply for voucher code.'),
						});
						return;
					}

					// Goes inside when atleast product in orderline...     
					if (orderlines.length) {                    
						if (output == true) {
							var selectedOrder = self.pos.get('selectedOrder');
							selectedOrder.coupon_id = entered_code;
							var total_amount = selectedOrder.get_total_without_tax();
							rpc.query({
								model: 'pos.gift.coupon',
								method: 'search_coupon',
								args: [partner_id, entered_code],
							
							}).then(function(output) {
								if(!(self.pos.pos_coupons_setting)){
									self.gui.show_popup('error', {
										'title': _t('Error'),
										'body': _t('There is no gift coupon.'),
									});
									return;
								}

								order.coupon_id = output[0];
								var amount = output[1];
								used = output[2];
								var coupon_count = output[3];
								var coupon_times = output[4];
								var expiry = output[5];
								var partner_true = output[6];
								var gift_partner_id = output[7];
								var amount_type = output[8]
								var exp_dt_true = output[9];
								var max_amount = output[10];
								var apply_coupon_on = output[11];
								var current_date = new Date().toUTCString();
								var d = new Date();
								var month = '0' + (d.getMonth() + 1);
								var day = '0' + d.getDate();
								var year = d.getFullYear();
								var product_id = self.pos.pos_coupons_setting[0].product_id[0];
								
								expiry = new Date(expiry)
								var date = new Date(year,month,day);
								if(amount_type == 'per'){
									if(apply_coupon_on == 'taxed')
									{
										total_amount = self.pos.get_order().get_total_with_tax();
									}
									amount = (total_amount * output[1])/100
								}else{
									amount = amount
								}

								for (var i = 0; i < orderlines.models.length; i++) {
									if (orderlines.models[i].product.id == product_id){
										coupon_applied = false;
									}
								}
								if (exp_dt_true && d > expiry){
									self.gui.show_popup('error', {
										'title': _t('Expired'),
										'body': _t("The Coupon You are trying to apply is Expired"),
									});	
								}
								
								else if (coupon_applied == false) {
									self.gui.show_popup('error', {
										'title': _t('Coupon Already Applied'),
										'body': _t("The Coupon You are trying to apply is already applied in the OrderLines"),
									});
								}
								
								else if (coupon_count > coupon_times){ // maximum limit
									self.gui.show_popup('error', {
										'title': _t('Maximum Limit Exceeded !!!'),
										'body': _t("You already exceed the maximum number of limit for this Coupon code"),
									});
								}
								
								else if (partner_true == true && gift_partner_id != partner_id.id){
									self.gui.show_popup('error', {
										'title': _t('Invalid Customer !!!'),
										'body': _t("This Gift Coupon is not applicable for this Customer"),
									});
								}

								else if(order.get_total_with_tax() < amount){
									self.gui.show_popup('error', {
										'title': _t('Invalid Amount !!!'),
										'body': _t("Coupon Amount is greater than order amount"),
									});
								}
								
								else { // if coupon is not used
									if(max_amount >= amount){
										var update_coupon_amount = max_amount - amount
										order.coup_maxamount = update_coupon_amount;

										var total_val = total_amount - amount;
										var product_id = self.pos.pos_coupons_setting[0].product_id[0];
										var product = self.pos.db.get_product_by_id(product_id);
										var selectedOrder = self.pos.get('selectedOrder');
										selectedOrder.add_product(product, {
											price: -amount,
											quantity: 1.0,
										});
									}else{
										self.gui.show_popup('error', {
											'title': _t('Maximum Limit Exceeded !!!'),
											'body': _t("You already exceed the maximum limit for this Coupon code."),
										});
									}
									
								}

							});
							self.gui.show_screen('products');
						} else { //Invalid Coupon Code
							self.gui.show_popup('error', {
								'title': _t('Invalid Code !!!'),
								'body': _t("Voucher Code Entered by you is Invalid. Enter Valid Code..."),
							});
						}
					} else { // Popup Shows, you can't use more than one Voucher Code in single order.
						self.gui.show_popup('error', {
							'title': _t('Already Used !!!'),
							'body': _t("You have already use this Coupon code, at a time you can use one coupon in a Single Order"),
						});
					}


				});
			});


		},

	});
	var _super_order = models.Order.prototype;
	models.Order = models.Order.extend({
		export_as_JSON: function() {
			var json = _super_order.export_as_JSON.apply(this,arguments);
			json.coupon_id = this.coupon_id;
			json.coup_maxamount = this.coup_maxamount;
			return json;
		},
	});

	gui.define_popup({
		name: 'select_existing_popup_widget',
		widget: SelectExistingPopupWidget
	});

	var GiftButtonWidget = screens.ActionButtonWidget.extend({
		template: 'GiftButtonWidget',
		button_click: function() {
			var order = this.pos.get_order();
			var self = this;
			this.gui.show_popup('open_coupon_popup_widget', {});
		},
	});
	var CouponConfigPopupWidget = popups.extend({
		template: 'CouponConfigPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		show: function(options) {
			var self = this;
			this._super(options);

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
				$('input[type="date"]').datepicker();
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
		name: 'open_coupon_popup_widget',
		widget: CouponConfigPopupWidget
	});
	screens.define_action_button({
		'name': 'POS Coupens Gift Voucher',
		'widget': GiftButtonWidget,
		'condition': function() {
			return true;
		},
	});
	var CreateCouponPopupWidget = popups.extend({
		template: 'CreateCouponPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},

		renderElement: function() {
			var self = this;
			this._super();
			var order = this.pos.get_order();
			var selectedOrder = self.pos.get('selectedOrder');
			$('#coupon_exp_dt').hide();
			$('#coupon_customer').hide();
			$('#alertcustomer').hide();
			$('#alertamount').hide();
			$('#alertdate').hide();
			$('#alertamt').hide();
			$('#alertamtmax').hide();

			this.$('#coupon_cust_box').click(function() {
				if ($('#coupon_cust_box').is(':checked')) {
					$('#coupon_customer').show();
				} else {
					$('#coupon_customer').hide();
				}
			});

			this.$('#coupon_expdt_box').click(function() {
				if ($('#coupon_expdt_box').is(':checked')) {
					$('#coupon_exp_dt').show();
				} else {
					$('#coupon_exp_dt').hide();
				}
			});
			this.$("#coup_amount_type").change(function() {
				if( $(this).val() == 'Percentage'){
					$('#apply_coupon_type').show();
				}
				else{
					$('#apply_coupon_type').hide();
				}
			});

			this.$('#create_coupon').click(function(ev) {
				
				if(self.pos.pos_coupons_setting.length < 1){
					ev.stopPropagation();
					ev.preventDefault(); 
					ev.stopImmediatePropagation();
					self.gui.show_popup('custom_error', {
						'title': _t('No gift coupon configuration'),
						'body': _t('Please configure product gift coupons .'),
					});
					return;
				}
				else{
					var c_name = $("#coupon_name").val();
					var c_limit = $("#coupon_limit").val();
					var c_amount = $("#coupon_amount").val();
					var c_am_type = $("#coup_amount_type").val();
					var c_customer = $("#coupon_customer").val();
					var c_issue_dt = $("#coupon_issue_dt").val();
					var c_exp_dt = $("#coupon_exp_dt").val();
					var c_max_amount = $("#coupon_max_amount").val();
					var c_expdt_box = $('#coupon_expdt_box').is(':checked');
					var c_cust_box = $("#coupon_cust_box").is(':checked');
					var apply_coupon_on = $('#apply_coupon_on').val();

					var exp_dt = new Date(c_exp_dt)
					var issu_dt = new Date(c_issue_dt)
					var max_exp_dt = false;
					if(self.pos.pos_coupons_setting[0].max_exp_date)
					{
						var max_exp_dt = new Date(self.pos.pos_coupons_setting[0].max_exp_date)
					}
					var max_coupan_value = self.pos.pos_coupons_setting[0].max_coupan_value
					var min_coupan_value = self.pos.pos_coupons_setting[0].min_coupan_value

					if(!(c_name && c_issue_dt)){
						self.gui.show_popup('create_coupon_popup_widget',{});
						$('#alertcustomer').show()
					}
					else if((c_max_amount) && (c_max_amount > max_coupan_value)){
						self.gui.show_popup('create_coupon_popup_widget',{});
						$('#alertamtmax').show()
					}
					else if(!(c_amount)){
						self.gui.show_popup('create_coupon_popup_widget',{});
						$('#alertamt').show()
					}
					else if((min_coupan_value > parseInt(c_amount) || parseInt(c_amount) > max_coupan_value) && (c_am_type != 'Percentage')){
						self.gui.show_popup('create_coupon_popup_widget',{});
						$('#alertamount').show()
					}
					else if(c_expdt_box && !max_exp_dt)
					{
						self.gui.show_popup('create_coupon_popup_widget',{});
						$('#alertdate').text('Please add expiry date in coupon configuration first.');
						$('#alertdate').show();
					}
					else if(max_exp_dt)
					{
						if(max_exp_dt.getTime() < issu_dt.getTime()){
							self.gui.show_popup('create_coupon_popup_widget',{});
							$('#alertdate').show()
						}
						else if(exp_dt.getTime() > max_exp_dt.getTime()){
							self.gui.show_popup('create_coupon_popup_widget',{});
							$('#alertdate').show()
						}
						else{
							self.gui.close_popup();
							var dict ={
								'c_name':c_name,
								'c_limit': c_limit,
								'c_amount':c_amount,
								'c_am_type':c_am_type,
								'c_customer':c_customer,
								'c_issue_dt':c_issue_dt,
								'c_exp_dt':c_exp_dt,
								'user_id':self.pos.get_cashier(),
								'coupon_max_amount':c_max_amount,
								'c_expdt_box':c_expdt_box,
								'c_cust_box':c_cust_box,
								'apply_coupon_on':apply_coupon_on,
							}
							rpc.query({
								model: 'pos.gift.coupon',
								method: 'create_coupon_from_ui',
								args: [dict],
							}).then(function(output) {
								self.gui.close_popup();
								self.gui.show_popup('After_create_coupon_popup_widget',output)
							})
						} 
					}
					else{
						self.gui.close_popup();
						var dict ={
							'c_name':c_name,
							'c_limit': c_limit,
							'c_amount':c_amount,
							'c_am_type':c_am_type,
							'c_customer':c_customer,
							'c_issue_dt':c_issue_dt,
							'c_exp_dt':c_exp_dt,
							'user_id':self.pos.get_cashier(),
							'coupon_max_amount':c_max_amount,
							'c_expdt_box':c_expdt_box,
							'c_cust_box':c_cust_box,
							'apply_coupon_on':apply_coupon_on,
						}
						rpc.query({
							model: 'pos.gift.coupon',
							method: 'create_coupon_from_ui',
							args: [dict],
						}).then(function(output) {
							self.gui.close_popup();
							self.gui.show_popup('After_create_coupon_popup_widget',output)
						})
					}
				}
			});
		},
	})

	gui.define_popup({
		name: 'create_coupon_popup_widget',
		widget: CreateCouponPopupWidget
	});
	var AfterCreateCouponPopup = screens.ScreenWidget.extend({
		template: 'AfterCreateCouponPopup',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
			this.coupon_data = {};
		},
		show: function(options) {
			var self = this;
			this._super(options);
			self.render_coupon(options)

			$(".close").click(function(){
				self.gui.close_popup();
			}) 
		},

		events: {
			"click .print_coupon": "print_gift_coupon",
		},

		print_gift_coupon: function (ev) {
			var self = this;
			ev.stopPropagation();
			ev.preventDefault();   
			self.pos.set('coupon_print_data', this.coupon_data);
			self.gui.show_screen('coupon_print',{'data' : this.coupon_data});
		},

		render_coupon: function(options) {
			var self = this;
			var partner_id = false;
			var order = this.pos.get_order();

			var coupon_datails = false;
			if (order.get_client() != null){
				partner_id = order.get_client();
			}

			coupon_datails =  options;
			var coup_id = options[0];
			var coup_name = options[1];
			var coup_exp_dt = false;
			if(options[2])
			{
				coup_exp_dt = options[2].split(" ")[0];
			}
			var coup_issue_dt = options[4];
			coup_issue_dt = coup_issue_dt.split(" ")[0];

			var coup_amount = options[3];
			var coup_img = options[7];
			var am_type = options[6];
			var coup_code = options[5];
			
			var coup_dict = {coup_id,coup_name,coup_exp_dt,coup_issue_dt,coup_amount,coup_img,am_type,coup_code}
			if(coup_dict){
				this.coupon_data = coup_dict
			}
		},

		print_web: function() {
			window.print();
		},

		renderElement: function() {
			var self = this;
			this._super();
		},
		
	})

	gui.define_popup({
		name: 'After_create_coupon_popup_widget',
		widget: AfterCreateCouponPopup
	});
});
