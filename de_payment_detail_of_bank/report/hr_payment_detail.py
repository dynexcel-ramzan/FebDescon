# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class PayemntDetailReport(models.AbstractModel):
    _name = 'report.de_payment_detail_of_bank.payment_transfer_report'
    _description = 'Payment Detail Report'
    
    def _get_report_values(self, docids, data=None):
        
        model = self.env.context.get('active_model')
        docs = self.env['payment.detail.wizard'].browse(self.env.context.get('active_id'))
  
        return {
            
            'docs': docs,
        }