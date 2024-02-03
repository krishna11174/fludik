from odoo import api, models, fields



class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    is_approved = fields.Boolean(default=False, copy=False)
    to_approve = fields.Boolean(default=True, copy=False)
    is_approval_compute = fields.Boolean()
    state = fields.Selection([('to_approve', 'To Approve'),
                               ('approved', 'Approved'),
                               ], tracking=True, copy=False)

    # @api.depends('description')
    def open_wizard(self):
        print("000000000")
        print(self.env.ref('contacts_custom.view_my_wizard_form').id,"44444444444")
        # return self.env.ref('contacts_custom.view_my_wizard_form')
        # return  self.env["ir.actions.act_window"]._for_xml_id("contacts_custom.action_my_wizard")

        return {
            'name': 'Do you want to increase the initial number',
            'type': 'ir.actions.act_window',
            'res_model': 'my.module.my_wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contacts_custom.view_my_wizard_form').id,
            'target': 'new',
            'context': {'active_id': self.id},
        }

    @api.constrains('list_price', 'taxes_id', 'default_code', 'barcode', 'l10n_in_hsn_code', 'l10n_in_hsn_discription',
                    'product_tag_ids', 'reference_number', 'initial_number', 'last_updated_ref_number',
                    'product_category', 'invoice_policy')
    def _state_change_product(self):
        for record in self:
            if record.state == 'approved':
                record.state = 'to_approve'

    def write(self, vals):
        # Check if the 'description' field is being updated
        print(vals, "vals")
        if 'state' not in vals:
            if 'description' not in vals:
                print(" not des")
                vals['state'] = 'to_approve'
                res = super(ProductTemplateInherit, self).write(vals)
                return res
        if 'description' in vals:

            print("oooooooooooo")
            old_description = self.description
            print(old_description, "old description")
            new_description = vals['description']
            # Update the field and create a log note
            vals['state'] = 'to_approve'
            result = super(ProductTemplateInherit, self).write(vals)
            self.message_post(
                body="Description changed from:<br/>%sto:<br/>%s" % (old_description, new_description),
                message_type="comment",
                subtype_id=self.env.ref('mail.mt_comment').id
            )
            return result
        else:
            return super(ProductTemplateInherit, self).write(vals)



    def button_approve(self):
            if not self.state or self.state == 'to_approve':
                self.state = 'approved'

    # @api.onchange('description')
    # def _onchange_product_id(self):
    #     print("uuuu")
    #     print(self,"oo")
    #     for rec in self:
    #         if rec.name:
    #             refernce_no_1 = rec.reference_number[-2:]
    #             refernce_no_2 = rec.reference_number[:-2]
    #             updated_ref_no = int(refernce_no_1)
    #             updated_ref_no = updated_ref_no + 1
    #             result_ref_no = str(updated_ref_no).zfill(len(refernce_no_1))
    #             present_revision_no = rec.initial_number[1:]
    #             updated_revision_no = int(present_revision_no)
    #             updated_revision_no = updated_revision_no + 1
    #             result_initial_revision_no = str(updated_revision_no).zfill(len(present_revision_no))
    #             final_result_ref_no = refernce_no_2 + result_ref_no
    #             rec.initial_number = rec.initial_number[0]+result_initial_revision_no
    #             rec.reference_number = final_result_ref_no



            # previous_ref_no =
            # rec.initial_number = result



class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    product_ids = fields.Many2many('res.partner', string='Products')

    @api.onchange('product_template_id')
    @api.depends('product_template_id')
    def _onchange_product_id(self):
        for rec in self:
            partners = self.env['product.template'].search([('state', '=', 'approved')])
            print(partners, "ppppppppp")
            print(partners.ids, "ppppppppp")
            # print(partners.id,"ppppppppp")
            self.product_ids = partners.ids
            return {'domain': {'product_template_id': [('id', 'in', partners.ids)]}}



class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    product_ids = fields.Many2many('product.template', string='Products')

    @api.onchange('product_id')
    @api.depends('product_id')
    def _onchange_product_id(self):
        for rec in self:
            partners = self.env['product.product'].search([('state', '=', 'approved')])
            print(partners, "ppppppppp")
            print(partners.ids, "ppppppppp")
            # print(partners.id,"ppppppppp")
            self.product_ids = partners.ids
            return {'domain': {'product_id': [('id', 'in', partners.ids)]}}




