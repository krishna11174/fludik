from odoo import models, fields, api

class fetch_data_to_account_move(models.Model):
    _inherit = 'sale.order'


#Transfer the field values from sale.order to account.move

    def _prepare_invoice(self):
        res = super(fetch_data_to_account_move, self)._prepare_invoice()

        res.update({
            'delivery_date' : self.commitment_date,
        })

        return res