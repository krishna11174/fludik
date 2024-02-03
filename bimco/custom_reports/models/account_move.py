# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.tools.misc import get_lang

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Delivery address for current invoice.")

    delivery_date = fields.Datetime(string='Sale Delivery Date')
    #change the report Attachment name
    def _get_report_proforma_filename(self):
        name = 'Proforma' + self.name
        print(name,"###################")
        if name == 'Proforma/':
            return 'Proforma_Draft'
        else:
            return 'Proforma_' + self.name

    def amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang='en_IN').title()
            except NotImplementedError:
                return num2words(number, lang='en_IN').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.currency_id.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        print(integer_value, fractional_value, '********************************8')

        lang_code = self.env.context.get('lang') or self.env.user.lang or get_lang(self.env).code
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        # amount_words = 'Rupees '+ num2words(integer_value)+ ' And '+num2words(fractional_value) + ' Paise only'

        amount_words = 'Rupees ' + (tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word='Rupees',
        )).replace('Rupees', ' ')
        if not self.currency_id.is_zero(amount - integer_value):
            amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=_num2words(fractional_value, lang=lang.iso_code),
                amt_word='Paise',
            )
        return amount_words + ' Only'
