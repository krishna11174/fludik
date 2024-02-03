# -*- coding: utf-8 -*-
# from odoo import http


# class SequenceGeneration(http.Controller):
#     @http.route('/sequence_generation/sequence_generation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sequence_generation/sequence_generation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sequence_generation.listing', {
#             'root': '/sequence_generation/sequence_generation',
#             'objects': http.request.env['sequence_generation.sequence_generation'].search([]),
#         })

#     @http.route('/sequence_generation/sequence_generation/objects/<model("sequence_generation.sequence_generation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sequence_generation.object', {
#             'object': obj
#         })
