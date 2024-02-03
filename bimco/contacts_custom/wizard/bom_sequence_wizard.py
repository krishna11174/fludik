
from odoo import models, fields, api

class MyWizard(models.TransientModel):
    _name = 'bom.my_wizard'

    # name = fields.Char(string='Name')
    # notes = fields.Char(string='Notes')


    @api.model
    def default_get(self, fields_list):
        print(fields_list,"ppppppppppppppp")
        res = super(MyWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        print(active_id,"active id")
        record = self.env['mrp.bom'].browse(active_id)
        print(record.product_tmpl_id.reference_number,"recorddd")
        # res['name'] = record.description
        return res

    def action_yes(self):
        print("yes")
        # print(self.notes,"notess")
        active_id = self.env.context.get('active_id')
        print(active_id,"active id")
        active_id_product =self.env['mrp.bom'].browse(active_id)

        print(active_id_product.product_tmpl_id.reference_number, "recorddd")

        # active_id_product.write({'description':self.notes})

        refernce_no_1 = active_id_product.product_tmpl_id.reference_number[-2:]
        refernce_no_2 = active_id_product.product_tmpl_id.reference_number[:-2]
        updated_ref_no = int(refernce_no_1)
        updated_ref_no = updated_ref_no + 1
        result_ref_no = str(updated_ref_no).zfill(len(refernce_no_1))
        print(result_ref_no,"result")
        present_revision_no = active_id_product.product_tmpl_id.last_updated_ref_number[1:]
        print(present_revision_no,"ooo")
        updated_revision_no = int(present_revision_no)
        updated_revision_no = updated_revision_no + 1
        result_initial_revision_no = str(updated_revision_no).zfill(len(present_revision_no))
        final_result_ref_no = refernce_no_2 + result_ref_no
        print(final_result_ref_no,"final")
        active_id_product.product_tmpl_id.last_updated_ref_number = active_id_product.product_tmpl_id.last_updated_ref_number[0] + result_initial_revision_no
        active_id_product.product_tmpl_id.reference_number = final_result_ref_no

        # for rec in self:
            # if rec.name:
            #     refernce_no_1 = rec.reference_number[-2:]
                # refernce_no_2 = rec.reference_number[:-2]
                # updated_ref_no = int(refernce_no_1)
                # updated_ref_no = updated_ref_no + 1
                # result_ref_no = str(updated_ref_no).zfill(len(refernce_no_1))
                # present_revision_no = rec.initial_number[1:]
                # updated_revision_no = int(present_revision_no)
                # updated_revision_no = updated_revision_no + 1
                # result_initial_revision_no = str(updated_revision_no).zfill(len(present_revision_no))
                # final_result_ref_no = refernce_no_2 + result_ref_no
                # rec.initial_number = rec.initial_number[0] + result_initial_revision_no
                # rec.reference_number = final_result_ref_n

    def action_no(self):
        print("no")
        # Add your code to execute when the "No" button is clicked
        # For example, you can cancel the operation or do nothing
        # return {'type': 'ir.actions.act_window_close'}

