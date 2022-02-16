from odoo import api, fields, models, _
from calendar import monthrange

from odoo.exceptions import UserError
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


class HrOvertimeApproval(models.Model):
    _name = 'hr.overtime.approval'
    _description = 'Overtime Approval'
    _inherit = ['mail.thread']
    _rec_name = 'incharge_id'

   
    incharge_id = fields.Many2one('hr.employee', string='Overtime Incharge')  
    approval_request_id = fields.Many2one('approval.request', string="Approval")
    category_id = fields.Many2one('approval.category', string='Approval Category')
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'To Approve'), ('approved', 'Approved'),('refused', 'Refused')], string='Status',
                             default='draft')    
    overtime_line_ids = fields.One2many('hr.overtime.approval.line', 'site_ot_id', string="Overtime Lines")
    
    work_location_id = fields.Many2one('hr.work.location', string="Work Location", compute='_compute_employee_location')
    workf_location_id = fields.Many2one('hr.work.location', string="Work Location")

    @api.depends('incharge_id')
    def _compute_employee_location(self):
        for line in self:
            line.update({
               'work_location_id': line.incharge_id.work_location_id.id,
               'workf_location_id': line.incharge_id.work_location_id.id,
                })
    
    
    @api.constrains('employee_id')
    def _check_incharge(self):
        for line in self:
            if line.incharge_id.user_id.id != self.env.uid:                   
                raise UserError('Only Employee Site Incharge can Approve Overtime!')

                    
    @api.model
    def create(self, vals):
        sheet = super(SiteAttendnace, self.with_context(mail_create_nosubscribe=True, mail_auto_subscribe_no_notify=True)).create(vals)
        sheet.action_submit()
        sheet.action_create_approval_request_site_attendance()
        
        return sheet
    
    
    def action_create_approval_request_site_attendance(self):
        approver_ids  = []       
        request_list = []
        for line in self:
            approval_categ=self.env['approval.category'].search([('name','=','Overtime'),('company_id','=', line.incharge_id.company_id.id)], limit=1)
            if not approval_categ:
                category = {
                    'name': 'Overtime',
                    'company_id': line.incharge_id.company_id.id,
                    'is_parent_approver': False,
                }
                approval_categ = self.env['approval.category'].sudo().create(category)
            line.category_id=approval_categ.id  
            if approval_categ:
                request_list.append({
                        'name': 'Overtime Approval' + ' Date From ' + str(line.date_from.strftime('%d-%b-%Y'))+' '+' Date To '+str(line.date_to.strftime('%d-%b-%Y')),
                        'request_owner_id': line.incharge_id.user_id.id,
                        'category_id': approval_categ.id,
                        'site_ot_id': line.id,
                        'reason': 'Overtime Approval' + ' Date From ' + str(line.date_from.strftime('%d-%b-%Y'))+' '+' Date To '+str(line.date_to.strftime('%d-%b-%Y')),
                        'request_status': 'new',
                })
                approval_request_id = self.env['approval.request'].sudo().create(request_list)
                vals ={
                    'user_id': line.incharge_id.user_id.id,
                    'request_id': approval_request_id.id,
                    'status': 'new',
                }
                approvers=self.env['approval.approver'].sudo().create(vals)
                approval_request_id._onchange_category_id()
                approval_request_id.action_confirm()
                line.approval_request_id = approval_request_id.id
                
            
    def unlink(self):
        for line in self:
            if line.state in ('submitted','approved'):
                raise UserError('Not Allow to delete  Document!')
        return super(HrOvertimeApproval, self).unlink()
    
    
    def action_approve(self):
        self.state = 'approved'  

    def action_submit(self):
        self.state = 'submitted'       
            
    def action_refuse(self):
        self.state = 'refused'
                
    def action_reset(self):
        self.state = 'draft'
        
   
class HrOvertimeLine(models.Model):
    _name = 'hr.overtime.approval.line'
    _description = 'Overtime Line'
    _rec_name = 'employee_id'

    site_ot_id = fields.Many2one('hr.overtime.approval', string='Site OT')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=False)
    normal_ot = fields.Float(string='Normal OT')
    rest_day_ot = fields.Float(string="Rest Day OT")
    gazetted_ot = fields.Float(string="Gazetted OT")
    work_location_id = fields.Many2one('hr.work.location', string="Work Location", compute='_compute_employee_location')
    workf_location_id = fields.Many2one('hr.work.location', string="Work Location")

    @api.depends('employee_id')
    def _compute_employee_location(self):
        for line in self:
            line.update({
               'work_location_id': line.employee_id.work_location_id.id,
               'workf_location_id': line.employee_id.work_location_id.id,
                })
    
    
    def unlink(self):
        for line in self:
            if line.state != 'draft':
                raise UserError('A record in Submitted or Approved state can`t be deleted!')
        return super(HrOvertimeLine, self).unlink()


    
    
    