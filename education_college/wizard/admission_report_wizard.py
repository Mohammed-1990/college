from odoo import models, fields, api


class EducationAdmissionPdfReport(models.TransientModel):
    _name = 'admission.pdf.report'

    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    admission_type = fields.Selection([('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'), ('tow_vacancy', 'Vacancy Tow'),('scholarship', 'Scholarship')], string="Type Of Admission")

 

    # generate PDF report
    def action_print_admission_report(self):
        data = {'college_id': self.college_id.id, 'program_id': self.program_id.id, 'batch_id': self.batch_id.id,
                'admission_type': self.admission_type}
        return self.env.ref('education_college.action_education_admission_pdf_report').report_action(self, data=data)

class EducationAdmissionReportPdf(models.AbstractModel):
    _name = 'report.education_college.education_admission_template'

    def _get_report_values(self, docids, data=None):
        domain = [ ]
        if data.get('college_id'):
            domain.append(('college_id', '=', data.get('college_id')))
        if data.get('program_id'):
            domain.append(('program_id', '=', data.get('program_id')))
        if data.get('batch_id'):
            domain.append(('batch_id', '=', data.get('batch_id')))
        if data.get('admission_type'):
            domain.append(('admission_type', '=', data.get('admission_type')))


        docs = self.env['new.admission'].search(domain)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'new.admission',
            'docs': docs,
            'datas': data,
        }
