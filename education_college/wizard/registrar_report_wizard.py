from odoo import models, fields, api


class EducationPDFReport(models.TransientModel):
    _name = 'education.pdf.report'

    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    level_id = fields.Many2one("level.level", ondelete="cascade", string="Level")
    semester_id = fields.Many2one("semester.semester", ondelete="cascade", string="Semester")
 

    # generate PDF report
    def action_print_report(self):
        pass
        data = {'college_id': self.college_id.id, 'program_id': self.program_id.id, 'batch_id': self.batch_id.id,
                'level_id': self.level_id.id,'semester_id':self.semester_id.id}
        return self.env.ref('education_college.action_education_register_pdf_report').report_action(self, data=data)

class EducationReportPDF(models.AbstractModel):
    _name = 'report.education_college.education_register_pdf_report_template'

    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('college_id'):
            domain.append(('college_id', '=', data.get('college_id')))
        if data.get('program_id'):
            domain.append(('program_id', '=', data.get('program_id')))
        if data.get('batch_id'):
            domain.append(('batch_id', '=', data.get('batch_id')))
        if data.get('level_id'):
            domain.append(('level_id', '=', data.get('level_id')))
        if data.get('semester_id'):
            domain.append(('semester_id', '=', data.get('semester_id')))
    
        docs = self.env['student.registrar'].search(domain)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'student.registrar',
            'docs': docs,
            'datas': data,
        }
