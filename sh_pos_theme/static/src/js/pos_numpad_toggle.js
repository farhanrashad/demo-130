odoo.define('sh_pos_theme.pos_numpad_toggle', function (require) {
"use strict";

var screens = require('point_of_sale.screens');

screens.ProductScreenWidget.include({
    show: function() {
        this._super();
        var self = this;
        if (this.pos.config.button_layout === false) {
            self.$('.leftpane').find('.control-buttons').hide();
        }
        $('.hide_button').unbind('click').click(function(ev) {
            ev.preventDefault();
            self.$('.pads').toggle();
            self.$('#arrow').toggleClass('rotate-90');
        });
    },
});
});