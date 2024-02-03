from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError




class MrpBomInherit(models.Model):
    _inherit = "mrp.bom"

    is_approved = fields.Boolean(default=False, copy=False)
    to_approve = fields.Boolean(default=True, copy=False)
    is_approval_compute = fields.Boolean()
    state = fields.Selection([('to_approve', 'To Approve'),
                               ('approved', 'Approved'),
                               ], tracking=True, copy=False)
    bool_check_update = fields.Boolean(string='check',required=True)
    bool_button_update = fields.Boolean(string='check button',default=False)

    @api.onchange('product_tmpl_id')
    @api.depends('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        for rec in self:
            partners = self.env['product.template'].search([('state', '=', 'approved')])
            return {'domain': {'product_tmpl_id': [('id', 'in', partners.ids)]}}

    # def action_yes(self):
    #     print("yes")
    #     for rec in self:
    #         refernce_no_1 = rec.product_tmpl_id.reference_number[-2:]
    #         refernce_no_2 = rec.product_tmpl_id.reference_number[:-2]
    #         updated_ref_no = int(refernce_no_1)
    #         updated_ref_no = updated_ref_no + 1
    #         result_ref_no = str(updated_ref_no).zfill(len(refernce_no_1))
    #         print(result_ref_no,"result")
    #         present_revision_no = rec.product_tmpl_id.initial_number[1:]
    #         print(present_revision_no,"ooo")
    #         updated_revision_no = int(present_revision_no)
    #         updated_revision_no = updated_revision_no + 1
    #         result_initial_revision_no = str(updated_revision_no).zfill(len(present_revision_no))
    #         final_result_ref_no = refernce_no_2 + result_ref_no
    #         print(final_result_ref_no,"final")
    #         rec.product_tmpl_id.initial_number = rec.product_tmpl_id.initial_number[0] + result_initial_revision_no
    #         rec.product_tmpl_id.reference_number = final_result_ref_no

    # @api.onchange('product_qty')
    # def show_warning_before_save(self):
    #     return {
    #         'warning': {
    #             'title': 'Warning',
    #             'message': 'You have made changes. Do you want to proceed with the save?',
    #             'buttons': [
    #                 {'name': 'Yes', 'action': 'action_yes'},
    #                 {'name': 'Cancel', 'action': 'cancel'},
    #                 {'name': 'Custom Button', 'action': 'action_yes'},
    #             ],
    #         }
    #     }
    #
    # def write(self, vals):
    #     if self._context.get('show_warning_on_save', True):
    #         print(self.is_edited(vals),"pppppppppppppppppp")
    #         if self.is_edited(vals):
    #             return self.show_warning_before_save()
    #     return super(MrpBomInherit, self).write(vals)


    # def write(self, vals):
    #     print(vals,"vaklsss")
    #     if vals.get('bool_check_update') == True and 'bool_check_update' not in vals:
    #         return super(MrpBomInherit, self).write(vals)
    #     else:
    #         raise ValidationError("Please click on 'Update' before saving the BOM.")



    def wizard_open(self):
        print("000000000")
        # result = self.get_changed_fields()
        self.bool_check_update = False
        self.bool_button_update = True

        # result = self.get_changed_fields()
        return {
            'name': 'Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'bom.my_wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('contacts_custom.view_bom_wizard_form').id,
            'target': 'new',
            'context': {'active_id': self.id},
        }


    # @api.onchange('product_templ_id','code','type','bom_line_ids','consumption','picking_type_id')
    @api.onchange('bom_line_ids')
    def _onchange_of_field(self):
        print("in onchnage")
        # return self.wizard_open()
        self.bool_check_update = True
        # res = self.env['ir.actions.act_window'].search([('name','=','My Wizard Bom')])
        # return res

    # def return_wizard(self):
    #     print("oooo44555")
    #     res = self.env['ir.actions.act_window'].search([('name', '=', 'My Wizard Bom')])
    #     print(res)
    #     return res

    # @api.constrains('bool_check_update')
    # def _check_needs_update(self):
    #     for record in self:
    #         if record.bool_check_update == True:
    #             raise ValidationError("Please click on 'Update' before saving the BOM.")


    @api.constrains('product_templ_id','product_qty','code','type','bom_line_ids','consumption','picking_type_id')
    def _state_change(self):
        for record in self:
            print(record,"ooo")
            if record.state == 'approved':
                print(record.state,"22222")
                record.state = 'to_approve'

    def button_approve(self):
        if not self.state or self.state == 'to_approve':
            self.state = 'approved'





#
# class MrpBomLine(models.Model):
#
#     _inherit = "mrp.bom.line"
#
#     to_approve = fields.Boolean(default=True, copy=False)


class MrpProductionInherit(models.Model):
    _inherit = "mrp.production"

    bom_ids = fields.Many2many('mrp.bom', string='Bom IDs')
    bool_field = fields.Boolean(string='Bool')

    # @api.onchange('product_id')
    # @api.depends('product_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',rec.product_id.name)])
    #         print(bom,"ppppppppp")
    #         self.bom_id = bom.id or False
    #         if rec.bom_id.state == 'to_approve':
    #             print(rec.bom_id,"pppppp")
    @api.onchange('product_id')
    @api.depends('product_id')
    def _onchange_product_id_only(self):
        for rec in self:
            partners = self.env['product.product'].search([('state', '=', 'approved')])
            # print(partners, "ppppppppp")
            print(partners.ids, "ppppppppp")
            # print(partners.id,"ppppppppp")
            # self.product_id = partners.ids
            return {'domain': {'product_id': [('id', 'in', partners.ids)]}}

    @api.onchange('bom_id')
    # @api.depends('product_id')
    def _onchange_product_id(self):
        for rec in self:
            # print(self.product_id.name,"llllllll")
            # print(rec.product_id.id,"llllllll")
            bom = self.env['mrp.bom'].search([('state','=','approved')])
            print(bom,"tttttttttttttt")
            print(bom.ids,"tttttttttttttt")
            # if bom:
            # print(partners.id,"ppppppppp")
            #     self.bom_ids = bom.ids
            #     print(self.bom_ids,"bom ids")
            return {'domain': {'bom_id': [('id', 'in', bom.ids)]}}
            # else:
            #     rec.bom_id = False

    @api.onchange('move_raw_ids')
    def _onchange_move_raw_ids(self):
        print("l")
        self.bool_field = True




