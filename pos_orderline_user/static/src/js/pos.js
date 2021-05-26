odoo.define('pos_orderline_user', function(require){
    
var models = require('point_of_sale.models');
var core = require('web.core');
var gui = require('point_of_sale.gui');
var screens = require('point_of_sale.screens');
var _t = core._t;
    
    var _super_Orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        init_from_JSON: function (json) {
            var res = _super_Orderline.init_from_JSON.apply(this, arguments);
            if (json.user_id) {
                var user = json.user_id;
                if (user) {
                    this.set_sale_person(user)
                }
            }
            return res;
        },
        set_sale_person: function (user) {
            this.user_id = user;
            this.trigger('change', this);
        },
        get_sale_person: function () {
            return this.user_id || null
        },
        export_as_JSON: function () {
            var json = _super_Orderline.export_as_JSON.apply(this, arguments);
            if (this.user_id) {
                json.user_id = this.user_id.id;
            }
            return json;
        },
    });
    screens.OrderWidget.include({
        render_orderline: function (orderline) {
            var self = this;
            var el_node = this._super(orderline);
            var el_sale_person = el_node.querySelector('.sale_person');
            if (el_sale_person) {
                el_sale_person.addEventListener('click', (function () {
                    var list = [];
                    for (var i = 0; i < self.pos.employees.length; i++) {
                        var user = self.pos.employees[i];
                        list.push({
                            'label': user.name,
                            'item':  user,
                        });
                    }
                    if (list.length > 0) {
                        return self.pos.gui.show_popup('selection', {
                            title: _t('Select Salesperson'),
                            list: list,
                            confirm: function (user) {
                                orderline.set_sale_person(user);
                            },
                        });
                    } 

                }.bind(this)));
            }
            return el_node;
        },
    });
    var SetAllSalespersonButton = screens.ActionButtonWidget.extend({
        template: 'SetAllSalespersonButton',
        button_click: function(){
            var list = [];
            var order = this.pos.get_order();
            for (var i = 0; i < this.pos.employees.length; i++) {
                var user = this.pos.employees[i];
                list.push({
                    'label': user.name,
                    'item':  user,
                });
            }
            if (list.length > 0) {
                return this.pos.gui.show_popup('selection', {
                    title: _t('Select Salesperson'),
                    list: list,
                    confirm: function (user) {
                        var orderlines = order.get_orderlines();
                        for(var i=0;i<orderlines.length;i++){
                            if(orderlines[i] != undefined){
                                orderlines[i].set_sale_person(user);
                            }
                        }
                    },
                });
            }
        },
    });

    screens.define_action_button({
        'name': 'SetAllSalespersonButton',
        'widget': SetAllSalespersonButton,
        'condition': function(){ 
            return this.pos.config.allow_orderline_user;
        },
    });
});
