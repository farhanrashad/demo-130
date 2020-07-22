from odoo import api, fields, models, _
import ast


class productcateg(models.Model):
    _inherit = "product.category"
    
    
    attribute_ids=fields.Many2many("product.attribute",string="Attribute")
    measurement=fields.Boolean("Measurement")

class product_measure(models.Model):
    _name='product.measurement'
    _description="Product Measurement"
    
    product_measure_line=fields.One2many("product.measurement.line","id_order")

    
    name=fields.Char('Name')
    
class product_measure_line(models.Model):
    _name='product.measurement.line'
    _description="Product Measurement"
    
    id_order=fields.Many2one("product.measurement")   

    
    name=fields.Char('Name')
    
        
class wizard_sale_line(models.Model):
  
    _name='sale.order.line.product.measurement'
    _description="Measurement"
    
    sale_measure_line=fields.One2many("wizard.sale.line.sale","lines")
    
    def compute_get_stock(self):
        context  =self._context
        p =self.env['sale.order.line'].search([('id', '=', context['active_id'])]).product_id
        
        if p:
            return p.id
        
    def compute_get_value(self):
        context  =self.env.context.get('active_ids')
        if context:
            return context
        
    context_id=fields.Char('Context Id',default=compute_get_value)

    product_id=fields.Many2one('product.product',string="Product", default=compute_get_stock)
    
    
    def confirm(self):
        a=[]
        if self.sale_measure_line:
            for s in self.sale_measure_line:
                a.append(s.name+str(s.value))
            js=self.env['sale.order.line'].search([('id','=',self._context.get('active_id'))]).name
            aa=' '.join(map(str,a))
            jss=js+''+aa
            self.env['sale.order.line'].browse(self._context.get('active_id')).update({'name':jss}) 

                
    
    @api.onchange('product_id')
    def get_value_name(self):
        line=[(5,0,0)]
        if self.product_id:
            if self.product_id.categ_id.measurement==True:
                    lines = self.env['product.measurement'].search([])
                    liness=sorted(lines)
                    linn=liness[-1]
                    fd=self.env['product.measurement'].search([('id','=',linn.id)])
                    for l in fd:
                        if l.product_measure_line:
                            for ll in l.product_measure_line:
                                for hg in ll:
                                        vals = {
                                                    'name':hg.name,
                                                }
                                        
                                        
                                        line.append((0, 0, vals))
                                        
                                    
                                        self.sale_measure_line=line
    
    
class sale_measure_line(models.Model):
    _name='wizard.sale.line.sale'
    _description="Product Measurement"
    
   
    
    lines=fields.Many2one("sale.order.line.product.measurement",readonly=True,invisible=True)   


    
    value=fields.Float("Value")
    
    
    
    
    
    name=fields.Char(string="Name")   
    
    
    
class sale_order_wizard(models.Model):
    _inherit='sale.order.line'
    
    
    
    def action_show_details(self):
        a=[]
        a.append(self.id)
#         zz=self.env['sale.order.line.product.measurement'].search(())
#         for z in zz:
#             
#             j=ast.literal_eval(z.context_id)
#             if a==ast.literal_eval(z.context_id):
                
        po = self.env['sale.order.line.product.measurement'].search([('context_id', '=', str(a))])   
        if self.product_id.categ_id.measurement==True:
            if po: 
                return {
                    'name': _('Measurement Operations'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'sale.order.line.product.measurement',
                    'res_id': po.id,
                    'target': 'new',
                }
            else:
                return {
                    'name': _('Measurement Operations'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'sale.order.line.product.measurement',
                    'target': 'new',
                }
