# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
import cx_Oracle

logger = logging.getLogger(__name__)




class AccountAccount(models.Model):
    _inherit = 'account.move'

    is_posted = fields.Boolean(string="Posted On Oracle")

    def action_delete_ebs_data(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        statement='delete from XX_ODOO_GL_INTERFACE'
        statementfetch = 'select STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR, REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10, REFERENCE21, GROUP_ID, PERIOD_NAME from XX_ODOO_GL_INTERFACE'
        cur.execute(statement)
        conn.commit()
        cur.execute(statementfetch) 
        attendances = cur.fetchall()
        raise UserError(str(attendances))
    
    def action_view_jv_data_posted(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        statement='delete from XX_ODOO_GL_INTERFACE'
        statementfetch = 'select STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR, REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10, REFERENCE21, GROUP_ID, PERIOD_NAME from XX_ODOO_GL_INTERFACE'
        cur.execute(statementfetch) 
        attendances = cur.fetchall()
        raise UserError(str(attendances))


  
    def action_posted_on_oracle(self):
        for jv in self:
            #if jv.is_posted == False:
            expense_sub_category_name = ' ' 
            for inv in self.line_ids:
                if inv.product_id:
                    expense_sub_category_name = inv.product_id.sub_category_id.name
                inv_name = inv.name
                ledger_id = int(inv.move_id.company_id.ledger_id)
                currency_code = inv.company_id.currency_id.name
                date_created = fields.date.today().strftime('%d-%b-%Y')
                created_by = -1
                flag = 'A'
                jv_category = 'Odoo '+ str(inv.move_id.journal_id.name)
                #company code
                segment1 = inv.move_id.company_id.segment1
                #cost center
                segment2 = inv.analytic_account_id.code if inv.analytic_account_id else '000'
                code_spliting = inv.account_id.code.split('.')
                #control-account
                segment3 = code_spliting[0]
                #sub account
                segment4 = code_spliting[1]
                segment5 =  '00'
                segment6 =  '00'
                entered_dr = int(inv.debit)
                entered_cr = int(inv.credit)
                accounting_dr = int(inv.debit)
                accountng_cr = int(inv.credit)
                ref1 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.name)+ ' '+str(inv.move_id.company_id.ledger_id) +str(inv.move_id.date.strftime('%Y%m%d'))  
                reference1 = ref1
                ref2 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.name)+ ' '+str(inv.move_id.company_id.ledger_id) +str(inv.move_id.date.strftime('%Y%m%d')) 
                reference2 = ref2
                ref4 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.name)+ ' '+str(inv.move_id.id)+ ' ' +str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name) 
                reference4 = ref4
                ref5 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.name)+ ' '+str(inv.move_id.id)+ ' ' +str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name) 
                reference5 = ref5
                reference6 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.name)  +' '+ str(expense_sub_category_name)
                emp_office_id = 0
                employee_office_id = self.env['hr.employee'].search([('address_home_id','=', inv.partner_id.id)], limit=1)
                    
                ref10 = str(employee_office_id.name) + ' ' + str(employee_office_id.emp_number) +' '+str(expense_sub_category_name)+' '+str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name)
                reference10 = ref10
                ref21= str(inv.move_id.company_id.ledger_id)+str(inv.move_id.id)+str(inv.id)
                reference21=ref21
                group_uniq_ref = str(inv.move_id.company_id.ledger_id)+str(fields.datetime.now().strftime('%Y%m%d'))+str(inv.move_id.id)
                group_id = int(group_uniq_ref)
                period_name = inv.date.strftime('%b-%y')
                context = inv.analytic_account_id.name if inv.analytic_account_id.name else 'NULL'
                attribute1 = inv.analytic_account_id.code if inv.analytic_account_id.code else 'NULL'
                inv_date = inv.date.strftime('%d-%b-%Y')
                conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
                cur = conn.cursor()
                statement = 'insert into XX_ODOO_GL_INTERFACE(STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR,REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10,REFERENCE21, GROUP_ID, PERIOD_NAME) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9,: 10,:11,: 12,:13,: 14,:15,: 16,:17,: 18,:19,: 20,:21,: 22,:23,: 24,:25,:26,:27,:28,:29)'
                cur.execute(statement,('NEW', ledger_id, inv_date, currency_code, date_created, created_by, flag,  jv_category, 'Odoo',segment1, segment2, segment3, segment4, segment5,segment6, entered_cr, entered_dr, accountng_cr, accounting_dr, reference1, reference2, reference4, reference5, reference6, reference10,reference21, group_id, period_name))
                conn.commit()
            jv.is_posted = True



















