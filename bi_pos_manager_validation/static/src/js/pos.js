odoo.define('bi_pos_manager_validation.pos', function (require) {
'use strict';
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var session = require('web.session');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var QWeb = core.qweb;
    var chrome = require('point_of_sale.chrome');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var payment_man = 0;
    var price_man = 0;
    var discount_man = 0;
    var order_del_man = 0;
    var order_line_del_man = 0;
    var qty_man = 0;
    var _t = core._t;

    models.load_fields('res.users',['pos_security_pin']);

    chrome.OrderSelectorWidget.include({
       deleteorder_click_handler: function(event, $el) {
        var self  = this;
        var order = this.pos.get_order(); 
        if (!order) {
            return;
        } else if ( !order.is_empty() ){

            if(this.pos.config.order_delete && this.pos.config.one_time_valid && order_del_man==0){
                    self.gui.show_popup('validation_popup_widget',{'mode':'order'});
                }else if(this.pos.config.order_delete && this.pos.config.one_time_valid == false){
                    this.gui.show_popup('validation_popup_widget',{
                        'state':this.state ,'mode':'order' 
                    });
                }else{
            this.gui.show_popup('confirm',{
                'title': _t('Destroy Current Order ?'),
                'body': _t('You will lose any data associated with the current order'),
                confirm: function(){
                     
                    // self.gui.show_popup('valid_qty_popup_widget', {});
                    self.pos.delete_current_order();
               
                    
                },
            });
             }
        } else {
                    // self.gui.show_popup('valid_qty_popup_widget', {});
                    this.pos.delete_current_order();
                
        }
            
    },
    });
// Popup start

    var ValidationPopupWidget = popups.extend({
        template: 'ValidationPopupWidget',
        // events: {
        //     'click .button.cancel.manager': 'click_cancel',
        // },
        click_cancel:function(options){
            this.gui.show_screen('products');
        },
        
        show: function(options){
            options = options || {};
            this._super(options);
            this.inputbuffer = '' + (options.value   || '');
            this.state = options.state || false;
            this.mode = options.mode || false;
            this.val = options.vals || false;
            this.decimal_separator = _t.database.parameters.decimal_point;
            // this.renderElement();
            this.firstinput = true;
        },
        click_numpad: function(event){
            var newbuf = this.gui.numpad_input(
                this.inputbuffer, 
                $(event.target).data('action'), 
                {'firstinput': this.firstinput});

            this.firstinput = (newbuf.length === 0);
            
            if (newbuf !== this.inputbuffer) {
                this.inputbuffer = newbuf;
                $('#entered_manager_password').val(this.inputbuffer);
            }
        },
        click_confirm: function(){

            var order = this.pos.get_order();
            var entered_charge = $("#entered_manager_password").val();
            var users = this.pos.config.user_id;
            // var pwd = self.$('.cashier_password').val()
            if(entered_charge){
                this.inputbuffer = entered_charge
            }else{
                this.inputbuffer = ''
            }
            var user_passd;
            var login_user = this.pos.get_cashier().id;
            for (var i = 0; i < this.pos.users.length; i++) {
                if (this.pos.users[i].id === users[0]) {
                    user_passd = this.pos.users[i].pos_security_pin;
                }
            }
            
            if (entered_charge == user_passd){
            if(this.mode==='payment'){
                this.gui.show_screen('payment');
                payment_man=1;

            }
            
            if(this.mode==='order'){
                this.pos.delete_current_order();
                order_del_man=1;
            }
            if(this.mode == 'order_line'){
                this.state.deleteLastChar();
                order_line_del_man=1;
                this.gui.close_popup();
            }

            if(this.mode == 'close_pos'){
                this.pos.push_order().then(function(){
        var url = "/web#action=point_of_sale.action_client_pos_menu";
        window.location = session.debug ? $.param.querystring(url, {debug: session.debug}) : url;
    });
            }

            if( this.mode === 'quantity'){
                if (order.get_selected_orderline()) {
                    order.get_selected_orderline().set_quantity(this.val);
                    qty_man=1
                    this.gui.close_popup();
                    }
                }
            if( this.mode === 'discount'){
                if (order.get_selected_orderline()) {
                    order.get_selected_orderline().set_discount(this.val);
                    discount_man=1;
                    this.gui.close_popup();
                }
                }
            if( this.mode === 'price'){
                if (order.get_selected_orderline()) {
                    var selected_orderline = order.get_selected_orderline();
                    selected_orderline.price_manually_set = true;
                    selected_orderline.set_unit_price(this.val);
                    price_man=1;
                    this.gui.close_popup();
                }
                }
                this.inputbuffer = '';
                }
            
            
            else{
                this.inputbuffer = '';
                self.$('.pos_screen_wrong_password').text('Wrong Password');
                
            }
            // this.gui.close_popup();
            if( this.options.confirm ){
                this.options.confirm.call(this,this.inputbuffer);
                // this.gui.show_screen('products');
            }
            this.inputbuffer = '';
        },     

    });
    gui.define_popup({
        name: 'validation_popup_widget',
        widget: ValidationPopupWidget
    });

    // End Popup start

// ActionpadWidget start
	screens.ActionpadWidget.include({
	renderElement: function() {
        var self = this;
        var users = this.pos.users;
        this._super();
        this.$('.pay').click(function(){
            var order = self.pos.get_order();
            var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                return line.has_valid_product_lot();
            });
            if(!has_valid_product_lot){
                self.gui.show_popup('confirm',{
                    'title': _t('Empty Serial/Lot Number'),
                    'body':  _t('One or more product(s) required serial/lot number.'),
                    confirm: function(){
                        self.gui.show_screen('payment');
                    },
                });
            }else{
                  
                if(self.pos.config.payment_perm && self.pos.config.one_time_valid && payment_man==0){
                    self.gui.show_popup('validation_popup_widget',{
                'mode':'payment'
                    });
                }else if(self.pos.config.payment_perm && self.pos.config.one_time_valid == false) {
                  self.gui.show_popup('validation_popup_widget',{
                'mode':'payment'
            });  
                }else{
                    // self.gui.show_popup('valid_qty_popup_widget', {});
                    self.gui.show_screen('payment');
                }
                
                
                
            }
        });
        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    }
	});

    screens.NumpadWidget.include({
         clickDeleteLastChar: function() {
                // var mode = this.numpad_state.get('mode');
                // var selector = this.$el.find('.numpad-backspace').selector;
                if(this.pos.config.order_line_delete && this.pos.config.one_time_valid && order_line_del_man==0 ){
                    this.gui.show_popup('validation_popup_widget',{
                        'state':this.state ,'mode':'order_line' 
                    });
                }else if(this.pos.config.order_line_delete && this.pos.config.one_time_valid == false ){
                    this.gui.show_popup('validation_popup_widget',{
                        'state':this.state ,'mode':'order_line' 
                    });
                }else{
                    return this.state.deleteLastChar();
                }
        
        },
    });

screens.OrderWidget.include({
    set_value: function(val) {
        var order = this.pos.get_order();
        if (order.get_selected_orderline()) {
            var mode = this.numpad_state.get('mode');
                if(this.pos.config.qty_detail && this.pos.config.one_time_valid && qty_man==0 && mode=='quantity'){
                        this.gui.show_popup('validation_popup_widget',{
                            'mode':mode ,'vals':val
                        });
                }else if(this.pos.config.discount_app && this.pos.config.one_time_valid && discount_man==0 && mode=='discount'){
                        this.gui.show_popup('validation_popup_widget',{
                            'mode':mode ,'vals':val
                        });
                }else if(this.pos.config.price_change && this.pos.config.one_time_valid && price_man==0 && mode=='price'){
                        this.gui.show_popup('validation_popup_widget',{
                            'mode':mode ,'vals':val
                        });
                }else if(this.pos.config.qty_detail && this.pos.config.one_time_valid == false && mode =='quantity'){
                    this.gui.show_popup('validation_popup_widget',{
                        'mode':mode ,'vals':val
                    });
                }else if( this.pos.config.discount_app && this.pos.config.one_time_valid == false && mode == "discount"){
                    this.gui.show_popup('validation_popup_widget',{
                        'mode':mode ,'vals':val
                    });
                }else if(this.pos.config.price_change && this.pos.config.one_time_valid == false && mode =='price'){
                    this.gui.show_popup('validation_popup_widget',{
                        'mode':mode ,'vals':val
                    });
                }else{

                    if( mode === 'quantity'){
                        order.get_selected_orderline().set_quantity(val);
                    }else if( mode === 'discount'){
                        order.get_selected_orderline().set_discount(val);
                    }else if( mode === 'price'){
                        var selected_orderline = order.get_selected_orderline();
                        selected_orderline.price_manually_set = true;
                        selected_orderline.set_unit_price(val);
                    }
                }
        }
    },
});

gui.Gui.include({
_close: function() {
        var self = this;
        this.chrome.loading_show();
        this.chrome.loading_message(_t('Closing ...'));

        if(self.pos.config.close_pos){
                    self.pos.gui.show_popup('validation_popup_widget',{
                        'mode':'close_pos'
                    });
                }else{
        this.pos.push_order().then(function(){
            var url = "/web#action=point_of_sale.action_client_pos_menu";
            window.location = session.debug ? $.param.querystring(url, {debug: session.debug}) : url;
        });
    }
    },
});
});
