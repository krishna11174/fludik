from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class PuchaseOrderSeqNew(models.Model):
    _inherit = "purchase.order"

    # added
    is_changed = fields.Boolean(string='Is The Details  Changed')

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

    def action_rfq_send(self):
        res = super(PuchaseOrderSeqNew, self).action_rfq_send()
        for rec in self:
            rec.state = 'sent'
            print(rec.is_verified)
        return rec





    # def action_rfq_send(self):
    #     self.ensure_one()
    #     ir_model_data = self.env['ir.model.data']
    #     try:
    #         if self.env.context.get('send_rfq', False):
    #             template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase')[2]
    #         else:
    #             template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase_done')[2]
    #     except ValueError:
    #         template_id = False
    #     try:
    #         compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
    #     except ValueError:
    #         compose_form_id = False
    #     ctx = dict(self.env.context or {})
    #     ctx.update({
    #         'default_model': 'purchase.order',
    #         'active_model': 'purchase.order',
    #         'active_id': self.ids[0],
    #         'default_res_id': self.ids[0],
    #         'default_use_template': bool(template_id),
    #         'default_template_id': template_id,
    #         'default_composition_mode': 'comment',
    #         'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
    #         'force_email': True,
    #         'mark_rfq_as_sent': True,
    #     })
    #     lang = self.env.context.get('lang')
    #     if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
    #         template = self.env['mail.template'].browse(ctx['default_template_id'])
    #         if template and template.lang:
    #             lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]
    #
    #     self = self.with_context(lang=lang)
    #     if self.state in ['draft', 'sent']:
    #         ctx['model_description'] = _('Request for Quotation')
    #     else:
    #         ctx['model_description'] = _('Purchase Order')
    #
    #     for rec in self:
    #         rec.state = 'sent'
    #         print(rec.is_verified)
    #     # return res


        # return {
        #     'name': _('Compose Email'),
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'view_id': compose_form_id,
        #     'target': 'new',
        #     'context': ctx,
        # }




