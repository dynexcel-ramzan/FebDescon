# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
import ast

def overtime_approval_lines_content(): 
    overtime = request.env['hr.overtime.approval'].sudo().search([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
    return {
        'overtime': overtime,
    }

      
class CustomerPortal(CustomerPortal):


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'overtime_count' in counters:
            values['overtime_count'] = request.env['hr.overtime.approval'].sudo().search_count([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
        return values
  
    def _overtime_get_page_view_values(self,overtime, access_token = None, **kwargs):
        overtime = request.env['hr.overtime.approval'].sudo().search([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
        values = {
            'page_name' : 'Overtime',
            'overtime' : overtime,
        }
        return self._get_page_view_values(overtime, access_token, values, 'my_overtime_history', False, **kwargs)

    @http.route(['/overtime/approvals', '/overtime/approvals/page/<int:page>'], type='http', auth="user", website=True)
    def portal_overtime_approvals(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                         search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': _('Default'), 'order': 'id asc'},
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'incharge_id desc' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }                                       
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }  
        searchbar_inputs = {
            'id': {'input': 'id', 'label': _('Search in No#')},
            'incharge_id.name': {'input': 'incharge_id.name', 'label': _('Search in Incharge')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }
        project_groups = request.env['hr.overtime.approval'].sudo().search([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
#         domain = []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       
        # search
        if search and search_in:
            search_domain = []
            if search_in in ('id', 'ID'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('incharge_id.name', 'Incharge'):
                search_domain = OR([search_domain, [('incharge_id.name', 'ilike', search)]])
            domain += search_domain
            
        domain += [('incharge_id.user_id', '=',http.request.env.context.get('uid'))]
        ot_amount_count = request.env['hr.overtime.approval'].sudo().search_count(domain)
        pager = portal_pager(
            url="/overtime/approvals",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in, 'search': search},
            total=site_attendance_count,
            page=page,
            step=self._items_per_page
        )
        _overtimes = request.env['hr.overtime.approval'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_overtime_history'] = _overtimes.ids[:100]
        grouped_overtime = [_overtimes]      
        paging(0,0,1)
        paging(grouped_overtime)
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_overtime': grouped_overtime,
            'page_name': 'overtime',
            'default_url': '/overtime/approvals',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("de_portal_overtime.portal_hr_overtime_req", values)   


    @http.route(['/overtime/approval/<int:overtime_id>'], type='http', auth="user", website=True)
    def portal_overtime_request_approval(self, overtime_id, access_token=None, **kw):
        values = []
        id = overtime_id
        try:
            attendance_sudo = request.env['hr.overtime.approval'].sudo().search([('id','=',overtime_id)])
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._overtime_get_page_view_values(attendance_sudo, access_token, **kw) 
        return request.render("de_portal_overtime.portal_overtime_lines", values)


    