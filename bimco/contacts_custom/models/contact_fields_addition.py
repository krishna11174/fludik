from odoo import api, models, fields
from num2words import num2words
# from odoo.tools import amount_to_text_en
import re



class ResPartnerInheritChanges(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(string='Customer Code')


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    reference_number = fields.Char(string='Reference Number')
    initial_number = fields.Char(string='Initial Revision Number',required=True)
    last_updated_ref_number = fields.Char(string='Last Updated Ref',required=True)
    product_category = fields.Many2one('product.category',string='Product Category')

    def create(self, vals_list):
        categ_id = vals_list[0]['product_category']
        prefix = self.env['product.category'].browse(categ_id)
        current_sequence = prefix.type.last_updated_seq
        suffix = vals_list[0]['last_updated_ref_number']
        next_sequence = current_sequence + 1
        sequence_number = str(next_sequence).zfill(5)
        result = str(prefix.type.name) + str(sequence_number) + str(suffix)
        if self.reference_number == False:
            vals_list[0]['reference_number'] = result
        prefix.type.last_updated_seq = sequence_number
        res = super(ProductTemplateInherit, self).create(vals_list)
        return res

    def write(self, vals):
        print(vals)
        for rec in self:
            if 'product_category' in vals:
                categ_id = vals['product_category']
                prefix = self.env['product.category'].browse(categ_id)
                current_sequence = prefix.type.last_updated_seq
                if 'last_updated_ref_number' in vals:
                    suffix = vals['last_updated_ref_number']
                else:
                    suffix = rec.last_updated_ref_number
                next_sequence = current_sequence + 1
                sequence_number = str(next_sequence).zfill(5)

                result = str(prefix.type.name) + str(sequence_number) + str(suffix)
                vals['reference_number'] = result
                prefix.type.last_updated_seq = sequence_number

            return super(ProductTemplateInherit, self).write(vals)


class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    last_updated_seq = fields.Integer(string='Last Updated Seq')
    type = fields.Many2one('bemco.product.type',string='Type')



class BomProductCategory(models.Model):
    _name = 'bemco.product.type'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    last_updated_seq = fields.Integer(string='Last Updated Seq')
    # category_type = fields.Char(string='Category Type')
    # parent_id = fields.Char(string='Parent Category')
