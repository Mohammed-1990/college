import datetime
from odoo import models, fields, api, exceptions



class ClinicReportWizard(models.TransientModel):
    _name = 'clinic.wizard'
    _description = "Create Medical Report"
    patient_id = fields.Char(string='Student Number', readonly=True)
    name = fields.Char(string='Full Name')
    student_id = fields.Many2one(
        'clinic.physical', string='Student Name')
    gender = fields.Char(string="Gender")
    birth_date = fields.Date(string='Date Of Birth')
    age = fields.Char(string='Age')
    date = fields.Date(string='Date Requested')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    nationality = fields.Char(string='Nationality')
    religion = fields.Char(string='Religion')
    program = fields.Char(string='Program')
    result = fields.Selection([
        ('fit', 'Medically fit'),
        ('unfit', 'Medically Unfit'),
        ('other', 'Others '),
    ], string="Result")
    result_date = fields.Char(string="Result Date", default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'))
    diagonis = fields.Text(string="Medical Report")
    doctor_name = fields.Char(string="Doctor Name", readonly=True, default=lambda self: self.env.user.name)

    #Function Wizards

    @api.onchange('student_id')
    def create_wizard(self):
        result = self.env['clinic.physical'].search([('id', '=',self.student_id.id)])
        if result:
            self.student_id =result.id
            self.birth_date = result.birth_date
            self.nationality = result.nationality
            self.patient_id = result.patient_id
            self.religion = result.religion
            self.program = result.program
            self.gender = result.gender



    # Func send to registeration

    def create_medical_report(self):

        result_physical = self.env['clinic.physical'].search([('id', '=',self.student_id.id)])
        if result_physical:
            result_physical.update({
                            'result': self.result,
                            'diagonis': self.diagonis,
                            'result_data': self.result_date,
                            'doctor_name': self.doctor_name,
                            })
        result = self.env['student.registrar'].search([('form_number', '=', self.patient_id)])
        if result:

            for rec in result:
                rec.update({
                        'result': self.result,
                        'doctor_comment': self.diagonis,
                        'result_data': self.result_date,
                        'result': self.result,
                        })
        






