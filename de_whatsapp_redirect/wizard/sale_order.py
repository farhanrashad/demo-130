from odoo import models, api, fields

class WhatsappSaleOrder(models.TransientModel):
    _name = 'whatsapp.message.wizard.sale'

    sale_order_id = fields.Many2one('sale.order', string="Recipient")
    mobile_sale = fields.Char(related='sale_order_id.mobile_sale',
                                 required=True)  # related='user_id_reciept_s.mobile_reciept'
    sale_partner_id = fields.Many2one('res.partner', string='Customer')
    # partner_reciept = fields.Char(string='partner', required=True) #related='user_id_reciept.partner_id'
    # picking_reciept = fields.Char(string='Picking', required=True) #related='user_id_reciept.picking_type_id'
    message_sale = fields.Text(string="message", default='This is Test', required=True)

    def send_message(self):
        if self.message_sale and self.mobile_sale:
            message_string = ''
            message_sale = self.message_sale.split(' ')
            for msg in message_sale:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.sale_order_id.mobile_sale + "&text=" + message_string +
                       "Sale Id:"+'  ' +str(self.sale_order_id) +
                       "Customer:"+'  ' +str(self.sale_partner_id),
                       # "Picking:" + self.picking_reciept+' '+
                       # "Partner:"+ self.partner_reciept,
                'target': 'self',
                'res_id': self.id,
            }

