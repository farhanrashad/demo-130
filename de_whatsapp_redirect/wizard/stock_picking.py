from odoo import models, api, fields

class Whatsappinventoryreciept(models.TransientModel):
    _name = 'whatsapp.message.wizard.stock'

    user_id_reciept = fields.Many2one('stock.picking', string="Recipient")
    mobile_reciept = fields.Char(related='user_id_reciept.mobile_reciept',
                                 required=True)  # related='user_id_reciept_s.mobile_reciept'
    origin_reciept = fields.Char(related='user_id_reciept.origin', required=True)
    partner_reciept = fields.Char(string='partner', required=True) #related='user_id_reciept.partner_id'
    picking_reciept = fields.Char(string='Picking', required=True) #related='user_id_reciept.picking_type_id'
    message_reciept = fields.Text(string="message", default='This is Test', required=True)

    def send_message(self):
        if self.message_reciept and self.mobile_reciept:
            # msg_test = ''
            # test = {
            #     'Sequence': self.origin_reciept,
            #     'partner': self.partner_reciept,
            #     'picking': self.picking_reciept
            # }
            # for r in test:
            #     msg_test = msg_test + r + '%20'
            # msg_test = msg_test[:(len(msg_test) - 3)]
            message_string = ''
            message_reciept = self.message_reciept.split(' ')
            for msg in message_reciept:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.user_id_reciept.mobile_reciept + "&text=" + message_string +
                       "Source Documents:"+ self.origin_reciept+
                       "Picking:" + self.picking_reciept+' '+
                       "Partner:"+ self.partner_reciept,
                'target': 'self',
                'res_id': self.id,
            }

    def get_info(self, decides):
        # docs=self.env['stock.picking'].search([])
        # sequence=docs.name
        sequence = "hello"
        mess = "here is sequence %s" % sequence
        return mess