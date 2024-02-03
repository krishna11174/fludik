from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http


class ExpensePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        rtn = super(ExpensePortal, self)._prepare_home_portal_values(counters)
        user_id = request.env.user.id
        domain = [('employee_id.user_id', '=', user_id)]
        rtn['expense_counts'] = request.env['hr.expense'].sudo().search_count(domain)
        return rtn

    @http.route(['/my/expense', '/my/expense/page/<int:page>'], type='http', website=True, auth="user")
    def portal_my_expense(self, page=1, **kw):
        user_id = request.env.user.id
        domain = [('employee_id.user_id', '=', user_id)]
        total_expense_count = request.env['hr.expense'].sudo().search_count(domain)
        page_detail = pager(url='/my/expense/', total=total_expense_count, page=page, step=10)
        expense = request.env['hr.expense'].sudo().search(domain, limit=10, offset=page_detail['offset'])

        vals = {'expense': expense, 'page_name': 'portal_my_expense_list_view', 'pager': page_detail}
        return request.render('hr_expense_portal.expense_list_view_portal', vals)

    @http.route('/my/expense/<model("hr.expense"):expense>', type='http', website=True, auth='user')
    def portal_my_expense_form(self, expense, **kw):
        domain = [('id', '=', expense.id)]
        expense = request.env['hr.expense'].sudo().search(domain)
        vals = {'expense': expense, 'page_name': 'portal_my_expense_form_view'}
        # below the code for form_view pagination
        user_id = request.env.user.id
        domain = [('employee_id.user_id', '=', user_id)]
        expense_records = request.env['hr.expense'].sudo().search(domain)
        expense_ids = expense_records.ids
        expense_index = expense_ids.index(expense.id)
        if expense_index != 0 and expense_ids[expense_index - 1]:
            vals['prev_record'] = '/my/expense/{}'.format(expense_ids[expense_index - 1])
        if expense_index < len(expense_ids) - 1 and expense_ids[expense_index + 1]:
            vals['next_record'] = '/my/expense/{}'.format(expense_ids[expense_index + 1])
        return request.render('hr_expense_portal.expense_form_view_portal', vals)
