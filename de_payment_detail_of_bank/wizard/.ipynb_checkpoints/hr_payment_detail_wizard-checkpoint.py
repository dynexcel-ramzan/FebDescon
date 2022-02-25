# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PaymentDetail(models.TransientModel):
    _name = "payment.detail.wizard"
    _description = "Payment Detail Report wizard"

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
   

    
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from','date_to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from','date_to'])[0])
        return self.env.ref('de_payment_detail_of_bank.open_payment_detail_action').report_action(self, data=data, config=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        