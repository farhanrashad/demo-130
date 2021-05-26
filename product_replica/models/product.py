# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_replica = fields.Boolean()

    def action_create_replica(self):
        product_id = self.env.context.get('template_id')
        product = self.browse(product_id)
        if product.is_replica:
            raise ValidationError(_('Replica already created for this product'))
        config_is_replica = self.env['ir.config_parameter'].sudo().get_param('product_replica.is_replica')
        suffix = self.env['ir.config_parameter'].sudo().get_param('product_replica.suffix')
        product_quality_id = self.env['ir.config_parameter'].sudo().get_param('product_replica.product_quality_id')

        if config_is_replica and self.user_has_groups('product_replica.group_product_replica') and suffix:
            copy_product = product.copy({
                'name': product.name,
                'product_quality_id': product_quality_id,
                'categ_id': product.categ_id.id,
                'default_code': product.default_code + '-' + suffix if product.default_code else '',
                'standard_price': product.standard_price,
            })
            product.is_replica = True
            return {
                'name': copy_product.name,
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'product.product',
                'res_id': copy_product.id,
                'view_id': self.env.ref('product.product_normal_form_view').id,
            }



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_replica = fields.Boolean()

    def action_create_replica(self):
        template_id = self.env.context.get('template_id')
        product = self.browse(template_id)
        if product.is_replica:
            raise ValidationError(_('Replica already created for this product'))
        config_is_replica = self.env['ir.config_parameter'].sudo().get_param('product_replica.is_replica')
        suffix = self.env['ir.config_parameter'].sudo().get_param('product_replica.suffix')
        product_quality_id = self.env['ir.config_parameter'].sudo().get_param('product_replica.product_quality_id')

        if config_is_replica and self.user_has_groups('product_replica.group_product_replica') and suffix:
            copy_product = product.copy({
                'name': product.name,
                'product_quality_id': product_quality_id,
                'categ_id': product.categ_id.id,
                'default_code': product.default_code + '-' + suffix if product.default_code else '',
                'standard_price': product.standard_price,
            })
            product.is_replica = True
            for main_prod in product.product_variant_ids:
                main_variant = main_prod.product_template_attribute_value_ids._get_combination_name()
                for copy_prod in copy_product.product_variant_ids:
                    copy_variant = copy_prod.product_template_attribute_value_ids._get_combination_name()
                    if main_variant == copy_variant and main_prod.default_code:
                        copy_prod.default_code = main_prod.default_code + '-' + suffix if main_prod.default_code else ''

            return {
                'name': copy_product.name,
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'product.template',
                'res_id': copy_product.id,
                'view_id': self.env.ref('product.product_template_only_form_view').id,
            }
