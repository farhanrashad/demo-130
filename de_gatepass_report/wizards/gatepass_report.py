class GatepassReportReport(models.TransientModel):
    _name = "gatepass.report.wizard"
    _description = "Employee Wizard"

    date_from = fields.Date(string="Date From", default=datetime.datetime.today())
    date_to = fields.Date(string="Date To", default=datetime.datetime.today())
    total_acc_qty = fields.Boolean(string="Total Accumulate Gatepass QTY")
    show_products = fields.Boolean(string="Show Only Full Sent Products")
    delivery_order = fields.Many2one('stock.picking', string="Delivery Order")
    
    
    
    
    
    def generate_pdf_report(self):
        result = self.env('stock.gatepass').search([('date','<=','date_from'),('date','>=','date_to')])
        data = {}
        for rec in result:
            
            data = {
                'product':rec.product_id.name
                }
        return self.env.ref('de_gatepass_report.de_gatepass_report_id').report_action([], data=data)