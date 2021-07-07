# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class moodle_class(models.TransientModel):
    _name = "moodle.config"

    moodle_token = fields.Char('Moodle Token', hepl="The token you've created with the specific user", required=True)
    moodle_username = fields.Char('Moodle Username', help="The User name to use to connect to Moodle from Odoo")
    moodle_server = fields.Char("Moodle Server", default='http://localhost:8888')
    moodle_url = fields.Char("Moodle Url")

    def connect_to_moodle(self):
        self.moodle_url = self.moodle_server + '/webservice/rest/server.php?wstoken=' + self.moodle_token
        parameter = {'wsfunction': 'core_webservice_get_site_info', 'moodlewsrestformat': 'json'}
        response = requests.get(self.moodle_url, params=parameter)
        self.moodle_url = response.url
        response = response.json()
        self.moodle_username = response['username']
