# -*- coding: utf-8 -*-
# from odoo import http


# class DePaymentDetailOfBank(http.Controller):
#     @http.route('/de_payment_detail_of_bank/de_payment_detail_of_bank/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payment_detail_of_bank/de_payment_detail_of_bank/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payment_detail_of_bank.listing', {
#             'root': '/de_payment_detail_of_bank/de_payment_detail_of_bank',
#             'objects': http.request.env['de_payment_detail_of_bank.de_payment_detail_of_bank'].search([]),
#         })

#     @http.route('/de_payment_detail_of_bank/de_payment_detail_of_bank/objects/<model("de_payment_detail_of_bank.de_payment_detail_of_bank"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payment_detail_of_bank.object', {
#             'object': obj
#         })
