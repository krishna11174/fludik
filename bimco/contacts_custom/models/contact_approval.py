from odoo import api, models, fields




class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    is_approved = fields.Boolean(default=False, copy=False)
    to_approve = fields.Boolean(default=True, copy=False)
    is_approval_compute = fields.Boolean()
    state = fields.Selection([('to_approve', 'To Approve'),
                               ('approved', 'Approved'),
                               ], tracking=True, copy=False)

    # def write(self, vals):
    #     print(vals,"ppppppppppppppp")
    #     if 'state' not in vals:
    #         vals['state']='to_approve'
    #         # i.state = 'to_approve'
    #     print(vals,"oooo")
    #     res = super(ResPartnerInherit, self).write(vals)
    #
    #     return res

    @api.constrains('function','phone')
    @api.depends('function','phone')
    def changing_values_need_approval(self):
        for rec in self:
            rec.state = 'to_approve'


    def button_approve(self):
            if not self.state or self.state == 'to_approve':
                self.state = 'approved'





# class MrpBomLine(models.Model):
#
#     _inherit = "mrp.bom.line"
#
#     to_approve = fields.Boolean(default=True, copy=False)


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    partner_ids = fields.Many2many('res.partner', string='Partner')


    @api.onchange('partner_id')
    # @api.depends('partner_id')
    def _onchange_product_id(self):
        for rec in self:
            partners = self.env['res.partner'].search([('state','=','approved')])
            print(partners,"ppppppppp")
            print(partners.ids,"ppppppppp")
            # print(partners.id,"ppppppppp")
            self.partner_ids = partners.ids
            return {'domain': {'partner_id': [('id', 'in', partners.ids)]}}


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    partner_ids = fields.Many2many('res.partner', string='Partner')
    state = fields.Selection([
        ('draft', 'PR'),
        ('sent', 'PR Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    @api.onchange('partner_id')
    @api.depends('partner_id')
    def _onchange_product_id(self):
        for rec in self:
            partners = self.env['res.partner'].search([('state', '=', 'approved')])
            print(partners, "ppppppppp")
            print(partners.ids, "ppppppppp")
            # print(partners.id,"ppppppppp")
            self.partner_ids = partners.ids
            return {'domain': {'partner_id': [('id', 'in', partners.ids)]}}
