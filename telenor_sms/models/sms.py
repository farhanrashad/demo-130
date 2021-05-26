# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import AccessError, UserError, ValidationError
import requests
from requests.exceptions import ConnectionError, HTTPError
import xml.etree.ElementTree as ET
import logging
_logger = logging.getLogger(__name__)

error_code = {
    '200': 'Failed login. Username and password do not match',
    '201': 'Unknown MSISDN, Please Check Format i.e. 92345xxxxxxx',
    '100': 'Out of credit.',
    '101': 'Field or input parameter missing',
    '102': 'Invalid session ID or the session has expired. Login again.',
    '103': 'Invalid Mask',
    '104': 'Invalid operator ID',
    '204': 'Sub user permission not allowed',
    '211': 'Unknown Message ID',
    '300': 'Account has been blocked/suspended',
    '400': 'Duplicate list name.',
    '401': 'List name is missing.',
    '411': 'Invalid MSISDN in the list.',
    '412': 'List ID is missing.',
    '413': 'No MSISDNs in the list.',
    '414': 'List could not be updated. Unknown error.',
    '415': 'Invalid List ID.',
    '500': 'Duplicate campaign name.',
    '501': 'Campaign name is missing.',
    '502': 'SMS text is missing.',
    '503': 'No list selected or one of the list IDs is invalid.',
    '504': 'Invalid schedule time for campaign.',
    '506': 'Cannot send message at the specified time. Please specify a different time.',
    '507': 'Campaign could not be saved. Unknown Error.',
    '600': 'Campaign ID is missing',
    '700': 'File ID is missing',
    '701': 'File not available or not ready',
    '702': 'Invalid value for max retries',
    '703': 'Invalid value for Call ID',
    '704': 'Invalid Mask for IVR',
    '301': 'Incoming SMS feature is not available for current user',
    '302': 'In valid action attribute value',
    '303': 'User has entered date and is not valid date',
    '304': 'API throughput limit reached for TPS Control mode',
    '305': 'User SMS/recipients exceeds than allowed throughput',
}

class TelenorSms(models.Model):
    _name = "telenor.sms"
    _rec_name = 'mobile'

    session_id = fields.Many2one('sms.session', 'Session ID')
    res_model = fields.Char('Model')
    res_id = fields.Char('Res ID')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    date = fields.Datetime('Date')
    partner_id = fields.Many2one('res.partner', string='Partner')
    mobile = fields.Char(related='partner_id.mobile')
    message = fields.Text()
    message_id = fields.Char('Message ID')
    error_code = fields.Char('Error Code')
    state = fields.Selection([('draft', 'Draft'), ('send', 'Send'), ('fail', 'Failed')], default='draft')

    def _get_auth_data(self):
        return {
            'msisdn': self.env.company.msisdn,
            'password': self.env.company.password,
        }

    def _get_last_session(self):
        return self.env['sms.session'].search([], limit=1).session_id

    def _get_new_session(self):
        data = self._get_auth_data()
        msisdn = data.get('msisdn')
        password = data.get('password')
        try:
            get_session_link = 'https://telenorcsms.com.pk:27677/corporate_sms2/api/auth.jsp?msisdn=%s&password=%s' % (msisdn, password)
            response = requests.request("GET", url=get_session_link).text
            tree = ET.fromstring(response)
            lst = tree.findall('corpsms')
            session_data = ''
            for item in tree:
                if item.tag == 'data' and item.text != 'Error':
                    session_data = item.text
            if session_data == 'Error 200':
                raise ValidationError(_('Something went wrong with SMS Configuration !'))
            else:
                session_id = self.env['sms.session'].search([('name', '=', session_data)])
                if not session_id:
                    session_id = self.env['sms.session'].create({'name': session_data})
                return session_id
        except (ConnectionError, HTTPError, exceptions.AccessError, exceptions.UserError) as exception:
            _logger.error('Autocomplete API error: %s' % str(exception))
            return False

    def send(self, data):
        mask = self.env.company.mask
        session = self._get_new_session()
        mobile = data.get('mobile')
        message = data.get('message')
        status = ''
        if not mobile:
            return False
        if session and mobile:
            url = "https://telenorcsms.com.pk:27677/corporate_sms2/api/sendsms.jsp?session_id=" + session.name + "&to=" + mobile + "&text=" + message + "&mask=" + mask
            response = requests.request("GET", url=url).text
            tree = ET.fromstring(response)
            lst = tree.findall('corpsms')
            session_data = ''
            for item in tree:
                if item.tag == 'data':
                    status = item.text

        self.create({
            'session_id': session and session.id or False,
            'date': fields.Datetime.now(),
            'partner_id': data.get('partner_id'),
            'mobile': mobile,
            'res_model': data.get('res_model'),
            'res_id': data.get('res_id'),
            'message': message,
            'message_id': '' if 'Error' in status else status,
            'error_code': status +': '+ error_code[status.split(' ')[1]] if 'Error' in status else '',
            'state': 'fail' if 'Error' in status or not session else 'send'
        })

class PhoneValidationMixin(models.AbstractModel):
    _inherit = 'phone.validation.mixin'

    def phone_format(self, number, country=None, company=None):
        return number

class PosOrder(models.Model):
    _name = "pos.order"
    _inherit = ['pos.order', 'mail.thread']
