from odoo import fields, models, api, _
import datetime
from datetime import datetime, timedelta

   
class helpdesk_customized(models.Model):
    _inherit = 'helpdesk.ticket'
   
    status_sla_line=fields.One2many("helpdesk.ticket.status.sla","ticket_id")
    
    
    

    
    @api.onchange('ticket_type_id')
    def _onchange_ticket_type_id(self):
        line=[(5,0,0)]
        if self.ticket_type_id:
            lines = self.env['helpdesk.ticket.sla'].search([])
            for lin in lines:
                if self.ticket_type_id.id==lin.ticket_type_id.id:
                    z=self.create_date+timedelta(lin.time_days)
                    j=z + timedelta(hours=lin.time_hours)
                    
                    vals = {
                        'name':lin.name,
                        'date':j,
                        'stage':lin.stage_id.id,
                    }
                            
                                
                    line.append((0, 0, vals))
                    
                
                    self.status_sla_line=line
            
                            
    @api.onchange('stage_id')
    def stage_change(self):
        time= datetime.now()
        time_for = format(time, '%Y-%m-%d %H:%M:%S')
        for attendance in self.status_sla_line:
            for attendances in attendance:
                liness = self.env['helpdesk.ticket.sla'].search([('name','=',attendances.name)])
                for lins in liness:
                    if time_for.split(' ')[0] >= attendances.date.strftime('%Y-%m-%d'):
                        if lins.stage_id.name!=attendances.ticket_id.stage_id.name:
                            if attendances.status==False:
               
                                attendances.update({'status':'fail'})
                                attendances.update({'is_fail':True})
                    if time_for.split(' ')[0] >= attendances.date.strftime('%Y-%m-%d'):
                        if lins.stage_id.name==attendances.ticket_id.stage_id.name:
                            if attendances.status==False:
                                attendances.update({'status':'acheived'})
                                attendances.update({'is_success':True})
                                attendances.update({'reached':datetime.now()})
    
    
class helpdesk_ticket(models.Model):
    _name='helpdesk.ticket.status.sla'
    
    ticket_id=fields.Many2one("helpdesk.ticket")
    
    name=fields.Char("Sla name")
    
    status=fields.Selection([
        ('fail', 'Failed'),
        ('acheived', 'Success'),
        ], string='Status')
    
    date=fields.Datetime("Deadline")
    reached=fields.Datetime("Reached")
    stage=fields.Many2one("helpdesk.ticket.stage",string="Stage")
    is_success=fields.Boolean("Is a Success")
    is_fail=fields.Boolean("Is a Fail")

    
    
    
    
    def stage_get(self):
        time= datetime.now()
        time_for = format(time, '%Y-%m-%d %H:%M:%S')
        for attendance in self.search([('date','!=',False)]):
            for attendances in attendance:
                liness = self.env['helpdesk.ticket.sla'].search([('name','=',attendances.name)])
                for lins in liness:
                    if time_for.split(' ')[0] >= attendances.date.strftime('%Y-%m-%d'):
                        if lins.stage_id.name!=attendances.ticket_id.stage_id.name:
                                attendances.update({'status':'fail'})
                                attendances.update({'is_fail':True})
                                
                    if time_for.split(' ')[0] >= attendances.date.strftime('%Y-%m-%d'):
                        if lins.stage_id.name==attendances.ticket_id.stage_id.name:
                                attendances.update({'status':'acheived'})
                                attendances.update({'is_success':True})
                                attendances.update({'reached':datetime.now()})
        
        
        
        
