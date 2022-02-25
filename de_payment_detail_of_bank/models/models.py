# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_payment_detail_of_bank(models.Model):
#     _name = 'de_payment_detail_of_bank.de_payment_detail_of_bank'
#     _description = 'de_payment_detail_of_bank.de_payment_detail_of_bank'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
