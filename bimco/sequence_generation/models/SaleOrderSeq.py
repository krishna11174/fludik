from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class SaleOrderSeq(models.Model):
    _inherit = "sale.order"
    is_changed = fields.Boolean(string='Is The Details  Changed')
    # added
    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        required = True,
        compute='_compute_payment_term_id',
        store=True, readonly=False, precompute=True, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.constrains('is_changed')
    def sequnce_modify(self):

        if (self.is_changed):

            data = self.name
            if ("R" in data and data[-3] == 'R'):
                first_data, second_data = data[:-3], data[-2:]

                second_data = int(second_data) + 1
                first_data += "R%02d" % (second_data)

                self.name = first_data
                self.is_changed = False
            else:
                data = data + "R01"
                self.name = data
                self.is_changed = False

    @api.model
    def create(self, vals):
        date = datetime.now()
        year = date.year
        month = date.month
        print(month)
        result = '%d%02d' % (year, month)
        if vals.get('name', _('New')) == _('New'):
            result += "QTN" + self.env['ir.sequence'].next_by_code(
                'quotation.send') or _('New')

        vals['name'] = result

        res = super(SaleOrderSeq, self).create(vals)
        return res

    def action_confirm(self):
        date = datetime.now()
        year = date.year
        month = date.month
        result = '%d%02d' % (year, month)
        data = self.env['ir.sequence'].next_by_code(
            'sale.order.sale') or _('New')
        result += "SO" + data
        self.name = result
        return super(SaleOrderSeq, self).action_confirm()

    def action_quotation_send_new(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('sale.action_report_pro_forma_invoice').report_action(self, data=data)


class PuchaseOrderSeq(models.Model):
    _inherit = "purchase.order"
    is_verified = fields.Boolean("verify")
    is_req_sent = fields.Boolean("send")


    @api.model
    def create(self, vals):
        date = datetime.now()
        year = date.year
        month = date.month
        print(month)
        result = '%d%02d' % (year, month)

        if vals.get('name', _('New')) == _('New'):
            data = self.env['ir.sequence'].next_by_code(
                'purchase.order.quotation') or _('New')
            print(data)
            result += ("PR" + data)
        res = super(PuchaseOrderSeq, self).create(vals)
        res['name'] = result
        return res

    def button_confirm(self):
        if (self.is_verified == True):
            date = datetime.now()
            year = date.year
            month = date.month
            result = '%d%02d' % (year, month)
            data = self.env['ir.sequence'].next_by_code(
                'purchase.order.order') or _('New')
            result += "PO" + data
            print(self.state, '23456787654321234567876543234567')
            self.name = result
            return super(PuchaseOrderSeq, self).button_confirm()
        else:
            raise ValidationError("Request not Approved by Admin")

    def req_send(self):
        # print(self.is_req_sent)
        # self.is_req_sent = True
        for rec in self:
            rec.is_req_sent = True
            print(rec.is_req_sent)

    def approve_quotation(self):
        for rec in self:
            rec.is_verified = True
            rec.is_req_sent = False


    def approval_sent(self):
        pass

    def approved(self):
        pass

