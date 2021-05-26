from odoo import models, fields, api, _
from odoo.exceptions import Warning


class ProductProduct(models.Model):
    _inherit = 'product.product'

    
    default_code = fields.Char(
        default='/',
        help="Set to '/' and save if you want a new internal reference "
             "to be proposed.")
    
    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', " cd!"),]
    
    @api.constrains('default_code')
    def not_allowed(self):
        existing_product = self.env['product.product']
        for record in self:
            if record.default_code:
                existing_product = record.env['product.product'].search([('id','!=',record.id),('default_code','=',record.default_code)])
            if existing_product:
                raise Warning("You can't have the same Internal Reference Number in Odoo twice!")

    
    @api.model
    def create(self, vals):
        if 'default_code' not in vals or vals['default_code'] == '/':
            categ_id = vals.get("categ_id")
            template_id = vals.get("product_tmpl_id")
            categ = sequence = False
            if categ_id:
                # Created as a product.product
                categ = self.env['product.category'].browse(categ_id)
            elif template_id:
                # Created from a product.template
                template = self.env["product.template"].browse(template_id)
                categ = template.categ_id
            if categ:
                sequence = categ.sequence_id
            if not sequence:
                sequence = self.env.ref('product_sequence.seq_product_auto')
            vals['default_code'] = sequence.next_by_id()
        return super(ProductProduct, self).create(vals)

    def write(self, vals):
        """To assign a new internal reference, just write '/' on the field.
        Note this is up to the user, if the product category is changed,
        she/he will need to write '/' on the internal reference to force the
        re-assignment."""
        for product in self:
            if vals.get('default_code', '') == '/':
                category_id = vals.get('categ_id', product.categ_id.id)
                category = self.env['product.category'].browse(category_id)
                sequence = category.sequence_id
                if not sequence:
                    sequence = self.env.ref(
                        'product_sequence.seq_product_auto')
                ref = sequence.next_by_id()
                vals['default_code'] = ref
                if len(product.product_tmpl_id.product_variant_ids) == 1:
                    product.product_tmpl_id.write({'default_code': ref})
            super(ProductProduct, product).write(vals)
        return True

    def copy(self, default=None):
        if default is None:
            default = {}
        if self.default_code:
            default.update({
                'default_code': self.default_code + _('-copy'),
            })
        return super(ProductProduct, self).copy(default)

class Producttemplated(models.Model):
    _inherit = 'product.template'

    @api.constrains('default_code')
    def not_allowed12(self):
        existing_product = self.env['product.template']
        for record in self:
            if record.default_code:
                existing_product = record.env['product.template'].search([('id','!=',record.id),('default_code','=',record.default_code)])
            if existing_product:
                raise Warning("You can't have the same Internal Reference Number in Odoo twice!")