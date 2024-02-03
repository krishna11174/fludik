from odoo import http
from odoo.http import request
from datetime import datetime, date
import base64
from werkzeug.utils import secure_filename


class TimeOffManagement(http.Controller):

    @http.route('/timeoff', type='http', website=True, auth='user')
    def timeoff_webform(self, **kw):
        holiday_status_id = request.env['hr.leave.type'].sudo().search([('requires_allocation', '=', 'no')])
        today_date = date.today().strftime('%Y-%m-%d')

        vals = {'holiday_status_id': holiday_status_id, 'today_date': today_date}
        return request.render('hr_timeoff_portal.create_timeoff_page', vals)

    @http.route('/timeoff/created', type='http', website=True, auth='user')
    def timeoff_created(self, **kw):
        print(kw)
        user_id = request.session.uid
        user = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])

        start_date = datetime.strptime(kw['request_date_from'], '%Y-%m-%d')
        end_date = datetime.strptime(kw['request_date_to'], '%Y-%m-%d')

        # Set the desired start and end times (9:00 AM and 6:00 PM)
        start_time = start_date.replace(hour=3, minute=30, second=0)
        end_time = end_date.replace(hour=12, minute=30, second=0)

        # Set the desired start and end times for half day (morning and afternoon)
        am_start_time = start_date.replace(hour=3, minute=30, second=0)
        am_end_time = start_date.replace(hour=7, minute=30, second=0)
        pm_start_time = start_date.replace(hour=8, minute=30, second=0)
        pm_end_time = start_date.replace(hour=12, minute=30, second=0)

        if 'supported_attachment_ids' in request.httprequest.files:
            supported_attachment_ids = []
            for attachment in request.httprequest.files.getlist('supported_attachment_ids'):
                if attachment.content_type != 'application/octet-stream':
                    file_data = attachment.read()
                    file_name = secure_filename(attachment.filename)
                    attachment_vals = request.env['ir.attachment'].sudo().create({
                        'name': file_name,
                        'datas': base64.b64encode(file_data),
                        'res_model': 'hr.leave',
                        'res_id': user.id
                    })
                    supported_attachment_ids.append(attachment_vals.id)
                else:
                    pass
            kw['supported_attachment_ids'] = [(6, 0, supported_attachment_ids)]
        vals = {
            'holiday_status_id': int(kw['holiday_status_id']),
            'date_from': start_time,
            'date_to': end_time,
            'request_date_from': start_date,
            'request_date_to': end_date,
            'name': kw['name'],
            'employee_id': user.id,
            'supported_attachment_ids': kw['supported_attachment_ids']
        }
        am_vals = {
            'holiday_status_id': int(kw['holiday_status_id']),
            'date_from': am_start_time,
            'date_to': am_end_time,
            'request_date_from': am_start_time,
            'request_date_to': am_end_time,
            'name': kw['name'],
            'employee_id': user.id,
            'supported_attachment_ids': kw['supported_attachment_ids'],
            'request_unit_half': kw.get('request_unit_half', False),
            'request_date_from_period': kw.get('request_date_from_period', False)
        }
        pm_vals = {
            'holiday_status_id': int(kw['holiday_status_id']),
            'date_from': pm_start_time,
            'date_to': pm_end_time,
            'request_date_from': pm_start_time,
            'request_date_to': pm_end_time,
            'name': kw['name'],
            'employee_id': user.id,
            'supported_attachment_ids': kw['supported_attachment_ids'],
            'request_unit_half': kw.get('request_unit_half', False),
            'request_date_from_period': kw.get('request_date_from_period', False)
        }
        # Check if 'request_unit_half' and 'request_date_from_period' exist in kw, and use False as default if not found
        request_unit_half = kw.get('request_unit_half', False)
        request_date_from_period = kw.get('request_date_from_period', False)
        print(request_unit_half)
        print(request_date_from_period)
        if request_unit_half and request_date_from_period:
            if request_unit_half == 'on' and request_date_from_period == 'am':
                request.env['hr.leave'].sudo().create(am_vals)
            elif request_unit_half == 'on' and request_date_from_period == 'pm':
                request.env['hr.leave'].sudo().create(pm_vals)
        else:
            request.env['hr.leave'].sudo().create(vals)

        return request.render('hr_timeoff_portal.timeoff_created_thanks_page', {})
