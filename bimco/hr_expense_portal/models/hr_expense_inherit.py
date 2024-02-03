from odoo import fields, models, _


class HrExpenseInherit(models.Model):
    _inherit = 'hr.expense'

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    def portal_submit_expenses(self):
        context_vals = self._get_default_expense_sheet_values()
        if len(context_vals) > 0:
            if len(context_vals) == 1:
                # Create a single expense sheet with the provided values
                expense_sheet = self.env['hr.expense.sheet'].create(context_vals[0])
                return {
                    'name': _('New Expense Report'),
                    'type': 'ir.actions.act_window',
                    'res_id': expense_sheet.id,
                    'view_mode': 'form',
                    'res_model': 'hr.expense.sheet',
                    'view_id': False,
                    'target': 'current',
                }
            else:
                # Create multiple expense sheets with the provided values
                expense_sheets = self.env['hr.expense.sheet'].create(context_vals)
                return {
                    'name': _('New Expense Reports'),
                    'type': 'ir.actions.act_window',
                    'views': [[False, "list"], [False, "form"]],
                    'res_model': 'hr.expense.sheet',
                    'domain': [('id', 'in', expense_sheets.ids)],
                    'context': self.env.context,
                }
        else:
            return {
                'type': 'ir.actions.act_window_close',
            }
