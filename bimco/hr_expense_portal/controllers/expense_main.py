from odoo import http
from odoo.http import request
from datetime import date
import base64
from werkzeug.utils import secure_filename


class ExpenseManagement(http.Controller):
    @http.route('/expense', type='http', website=True, auth='user')
    def expense_webform(self, **kw):
        user_id = request.session.uid
        user = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        product_id = request.env['product.product'].sudo().search([('can_be_expensed', '=', True)])
        currency_id = request.env['res.currency'].sudo().search([])
        today_date = date.today().strftime('%Y-%m-%d')
        vals = {'user': user, 'product_id': product_id, 'today_date': today_date, 'currency_id': currency_id}
        return request.render('hr_expense_portal.create_expense_page', vals)

    @http.route('/expense/created', type='http', website=True, auth='user')
    def expense_created(self, **kw):
        product_id = int(kw.get('product_id'))
        product = request.env['product.product'].sudo().browse([product_id])
        product_uom_id = product.uom_id.id

        user_id = request.session.uid
        user = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        if 'attachment_ids' in request.httprequest.files:
            attachment_ids = []
            for attachment in request.httprequest.files.getlist('attachment_ids'):
                if attachment.content_type != 'application/octet-stream':
                    file_data = attachment.read()
                    file_name = secure_filename(attachment.filename)
                    attachment_vals = request.env['ir.attachment'].sudo().create({
                        'name': file_name,
                        'datas': base64.b64encode(file_data),
                        'res_model': 'hr.expense',
                        'res_id': user.id
                    })
                    attachment_ids.append(attachment_vals.id)
                else:
                    pass
            kw['attachment_ids'] = [(6, 0, attachment_ids)]
        expense = request.env['hr.expense'].sudo().create(kw)
        expense.write({'product_uom_id': product_uom_id})

        return request.render('hr_expense_portal.expense_created_thanks_page', {})

    @http.route('/expense/edit/<model("hr.expense"):expense>', type='http', website=True, auth='user')
    def edit_expense_webform(self, expense, **kw):

        domain = [('id', '=', expense.id)]
        expense = request.env['hr.expense'].sudo().search(domain)

        user_id = request.session.uid
        user = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        product_id = request.env['product.product'].sudo().search([('can_be_expensed', '=', True)])
        currency_id = request.env['res.currency'].sudo().search([])
        vals = {'expense': expense, 'user': user, 'product_id': product_id, 'currency_id': currency_id}
        return request.render('hr_expense_portal.edit_expense_page', vals)

    @http.route('/expense/edited', type='http', website=True, auth='user')
    def expense_edited(self, **kw):
        record_id = int(kw.get('id'))
        expense = request.env['hr.expense'].sudo().search([('id', '=', record_id)])
        kw.pop('id', None)

        user_id = request.session.uid
        user = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        attachment_ids = expense.attachment_ids.mapped('id')
        if 'attachment_ids' in request.httprequest.files:
            for attachment in request.httprequest.files.getlist('attachment_ids'):
                if attachment.content_type != 'application/octet-stream':
                    file_data = attachment.read()
                    file_name = secure_filename(attachment.filename)
                    attachment_vals = request.env['ir.attachment'].sudo().create({
                        'name': file_name,
                        'datas': base64.b64encode(file_data),
                        'res_model': 'hr.expense',
                        'res_id': user.id
                    })
                    attachment_ids.append(attachment_vals.id)
                else:
                    pass
            kw['attachment_ids'] = [(6, 0, attachment_ids)]

        kw['product_id'] = int(kw.get('product_id'))
        kw['employee_id'] = int(kw.get('employee_id'))
        kw['currency_id'] = int(kw.get('currency_id'))
        product_id = int(kw.get('product_id'))
        product = request.env['product.product'].sudo().browse([product_id])
        kw['product_uom_id'] = product.uom_id.id

        expense.sudo().write(kw)

        return request.render('hr_expense_portal.expense_updated_thanks_page', {})

    @http.route('/expense/delete/<model("hr.expense"):expense>', type='http', website=True, auth='user')
    def expense_deleted(self, expense, **kw):
        if expense and expense.state == 'draft':
            expense.sudo().unlink()

        return request.render('hr_expense_portal.expense_deleted_thanks_page', {})

    @http.route('/expense/submit/<model("hr.expense"):expense>', type='http', website=True, auth='user')
    def expense_submitted(self, expense, **kw):
        expense.portal_submit_expenses()
        expense.state = 'reported'
        report = request.env['hr.expense.sheet'].sudo().search([('id', '=', expense.sheet_id.id)])
        report.state = 'submit'

        return request.render('hr_expense_portal.expense_submitted_thanks_page', {})
