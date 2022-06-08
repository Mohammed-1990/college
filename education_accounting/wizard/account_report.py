
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
class accountReport(models.TransientModel):
    _name = 'account.pdf.report'
    _description = "account Report"
    
    
    college_id = fields.Many2one('college.college', string='College', ondelete='cascade')
    program_id = fields.Many2one("program.program",ondelete="cascade",string="program", domain="[('college_id', '=', college_id)]")
    level_id = fields.Many2one('level.level', string='the level',ondelete='cascade')
    semester_id = fields.Many2one('semester.semester', string='Semester',ondelete='cascade', domain="[('level_id','=',level_id)]")
    student_id = fields.Many2one('education.accounting', string='Student Name')
    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)


    # generate PDF report
    def print_accunt_report(self):
        data = {'date_from': self.date_from, 'date_to': self.date_to, 'student': self.student_id.id,'college': self.college_id.id,
          'program': self.program_id.id,'level': self.level_id.id,
                'semester': self.semester_id.id}
        return self.env.ref('education_accounting.action_education_account_pdf_report').report_action(self, data=data)


class AccountReport (models.AbstractModel):
    
    _name = 'report.education_accounting.account_wizerd_template'

    def _get_report_values(self, docids, data=None):
        domain = [('type_of_fees', '!=', 'management')]
        if data.get('student'):
            domain.append(('student_id', '=', data.get('student')))
            domain.append(('program_id', '=', data.get('program')))
        if data.get('semester'):
            domain.append(('semester_id', '=', data.get('semester')))
        if data.get('level'):
            domain.append(('level_id', '=', data.get('level')))
        if data.get('date_from'):
            domain.append(('year', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('year', '<=', data.get('date_to')))
        docs = self.env['education.accounting'].search(domain)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'education.accounting',
            'docs': docs,
            'datas': data,
        }    



        
        

