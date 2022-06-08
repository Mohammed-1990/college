from odoo import models, fields, api


class ExamResultPdfReport(models.TransientModel):
    _name = 'exam.result.pdf.report'

    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    level_id = fields.Many2one('level.level', string='Level')
    semester_id = fields.Many2one('semester.semester', string='Semester', domain="[('level_id','=',level_id)]")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")

 
#
    # generate PDF report
    def action_print_exam_result_report(self):
        data = {'college_id': self.college_id.id, 'program_id': self.program_id.id, 'level_id': self.level_id.id,
                'semester_id': self.semester_id.id,'batch_id':self.batch_id.id}
        return self.env.ref('education_result.action_exam_result_pdf_report').report_action(self, data=data)

class EducationExamResultReportPdf(models.AbstractModel):
    _name = 'report.education_result.report_exam_result_template'

    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('college_id'):
            domain.append(('college_id', '=', data.get('college_id')))
        if data.get('program_id'):
            domain.append(('program_id', '=', data.get('program_id')))
        if data.get('semester_id'):
            domain.append(('semester_id', '=', data.get('semester_id')))

        docs = self.env['calculation.rate'].search(domain)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'calculation.rate',
            'docs': docs,
            'datas': data,
        }
