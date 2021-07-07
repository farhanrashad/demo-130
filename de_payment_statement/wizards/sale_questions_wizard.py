from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleQuestionsWizard(models.TransientModel):
    _name = "sale.questions.wizard"
    _description = "Sale Questions Wizard"

    sale_questions_line = fields.One2many('sale.questions.line.wizard', 'sale_questions_id')
    check_box = fields.Boolean(string='Get All Question Groups')
    type = fields.Selection([('mtm', 'MTM'), ('bespoke', 'BESPOKE')], string='Select Service Type', default='mtm')

    @api.onchange('check_box')
    def onchange_checkbox(self):
        data = []
        record = self.env['forced.question.group'].search([])
        for rec in record:
            line_data = []
            for question in rec.questions:
                line_data.append(question.id)

            data.append((0, 0, {
                'question_groups': rec.id,
                'value': line_data
            }))
        self.sale_questions_line = data

    def action_add(self):
        self.model = self.env.context.get('active_model')
        rec = self.env[self.model].browse(self.env.context.get('active_id'))
        description = ''
        for i in self.sale_questions_line:
            names = ''
            for val in i.value:
                names += val.name + ' '
            description = description + ',' + i.question_groups.name + ' = ' + names
            rec.name = description.lstrip(',')
            selected_type = self.type
            rec.service_type = selected_type.upper()


class SaleQuestionsLinesWizard(models.TransientModel):
    _name = "sale.questions.line.wizard"
    _description = "Sale Questions Line Wizard"

    sale_questions_id = fields.Many2one('sale.questions.wizard', string='Sale Questions')
    question_groups = fields.Many2one('forced.question.group', string='Available Question Groups')
    value = fields.Many2many('pos.forced.question',string='Value')