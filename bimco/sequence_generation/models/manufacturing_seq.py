from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError

class ManufacturingOrderSeq(models.Model):
    _inherit = "mrp.production"
    is_changed = fields.Boolean(string='Is The Details  Changed')

    @api.constrains('is_changed')
    def manufacturing_ord_seq_upadating(self):
        if self.is_changed:
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
    def create(self, vals_list):
        res = super(ManufacturingOrderSeq, self).create(vals_list)
        res.update({
            'name': str(datetime.now().year) + str(datetime.now().month) + 'MO' + res.name[6::]
        })
        return res
