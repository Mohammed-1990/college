import datetime
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError
import re
class RegistrarOffices(models.Model):
    _inherit = ['mail.thread']
    _name = 'student.registrar'
    _description = 'student registrar office'

    name = fields.Char(string="Full Name")
    image_1920 = fields.Binary('image_1920')
    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    level_id = fields.Many2one("level.level", ondelete="cascade", string="Level")
    semester_id = fields.Many2one("semester.semester", ondelete="cascade", string="Semester")
    year_stady = fields.Char('Study Year  :',  default=lambda self: str(datetime.datetime.now().year -1)+" - "+str(datetime.datetime.now().year))
    old_accept_type = fields.Selection([
        ('degree_holder', 'Hold Degrees'),
        ('transfer', 'Transfer From University'),
        ('bridging', 'Bridging'),
        ('mature', 'Mature'),
    ], string="Admission After First Year")
    type_acceptance = fields.Selection([('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'), ('tow_vacancy', 'Vacancy Tow'),('scholarship', 'Scholarship')], string="Type Of Acceptance")
    accept_year = fields.Char(string='Accept year ')
    nationality_id = fields.Many2one('res.country', string="Nationality")
    type_of_id = fields.Selection([('national_number', 'National  Number'), ('national_card', 'National Card'), ('passport', 'Passport')], string="Personality Type")
    id_number = fields.Char(string="The National Number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    religion = fields.Selection([('muslim', 'Muslim'), ('christian', 'Christian '), ('other', 'Other')], string="Religion")
    social_status = fields.Selection([('married', 'Married'), ('single', 'Single '), ('other', 'Other')], string="Social Status")
    birth_date = fields.Date(string="Barth Day")
    states = fields.Char(string="State")
    local = fields.Char(straing='Local')
    student_mobile = fields.Char(string="Mobile Number")
    whatsapp_phone = fields.Char(string="Whatsapp")
    email = fields.Char(string="Email")
    school_name = fields.Char(string='School Name ')
    sitting_number = fields.Char(string="Sitting Number")
    ratio = fields.Float(string="The Ratio")
    type_of_certificate = fields.Selection(
        [('sudanese', 'Sudanese'), ('arabic', 'Arabic'), ('other', 'Other')],
        string="Type Of Certificate")
    course = fields.Selection([('scientific', 'Scientific'), ('literary', 'Literary')], string="The course")
    form_number = fields.Char(string='University ID')
    certificate_level = fields.Char(string="Certificate level")
    national_card = fields.Binary(string="National Card")
    school_certificate = fields.Binary(string="High School Certificate")
    applicant = fields.Char(string="applicant  Name")
    fother_address = fields.Char(string="Address")
    telephone = fields.Char(string="Telphone")
    job = fields.Char(string="Job")
    student_position = fields.Selection([('not_registered', 'Not Registered'),('first_period', 'First Period'),('second_period', 'Second Period')],default='not_registered', string="Student's position")
    relative_relation = fields.Char(string="Relative Relation")
    state = fields.Selection([('draft', 'Draft'), ('done', 'done')], string='Status', default="done")
    previous_result = fields.Selection(
        [('scientific', 'طالب جديد'), ('literary', 'نجاح'), ('literary', 'اعادة'), ('literary', 'فصل  اكاديمي')
         ], string="The Result")
    study_fees = fields.Float(string="Study  Fees" ,compute='_compute_fees', store=True)
    register_fees = fields.Float(string="Register  Fees" ,compute='_compute_fees', store=True)
    after_discount = fields.Float(string="Fees ِAfter Discount")
    remaining_fee = fields.Float(string="Payment Fees" , compute='_compute_fees_after_discount', store=True)
    is_clinic = fields.Boolean(string="Is Clinic Book")
    doctor_comment = fields.Text(string='Doctor Comment')
    result = fields.Selection([
        ('fit', 'Medically fit'),
        ('unfit', 'Medically Unfit'),
        ('other', 'Others '),
    ], string="Result")
    result_data = fields.Char(string="Result Date", readonly=True)
    doctor_name = fields.Char(string="Doctor Name", readonly=True)
    user_id = fields.Many2one('res.users', 'Creant User ',  default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company')

    def get_invoicing(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Invoicing Violation",
            'view_mode': 'tree,form',
            'res_model': 'education.accounting',
            'domain': [('student_id', '=', self.id),('state', '=','done'),('type_of_fees', '=','stady')],
            }

    def get_medical_examination(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Medical Examination",
            'view_mode': 'tree,form',
            'res_model': 'clinic.physical',
            'domain': [('patient_id', '=', self.form_number)],
            }

    




    @api.depends('type_acceptance','old_accept_type')
    def _compute_fees(self):
        fees = self.env['study.fees'].search([('college_id', '=', self.college_id.id ), ('program_id', '=', self.program_id.id),('year', '=', datetime.datetime.now().year )])
        if fees:
            if self.type_acceptance:
                if self.type_acceptance == "expats":
                    self.study_fees = fees.foreigners_study
                    self.remaining_fee = fees.foreigners_study
                    self.register_fees = fees.foriegn_register_fees
                if self.type_acceptance == "scholarship":
                    self.study_fees = 0.0
                    self.remaining_fee = 0.0
                    self.register_fees = fees.sdn_register_fees
                else:
                    self.study_fees = fees.sudaness_study
                    self.remaining_fee = fees.sudaness_study
                    self.register_fees = fees.sdn_register_fees
            elif self.old_accept_type:
                if self.type_of_certificate :
                    if self.type_of_certificate == "sudanese":
                        self.study_fees = fees.sudaness_study
                        self.remaining_fee = fees.sudaness_study
                        self.register_fees = fees.sdn_register_fees
                    else:
                        self.study_fees = fees.foreigners_study
                        self.remaining_fee = fees.foreigners_study
                        self.register_fees = fees.foriegn_register_fees






    @api.depends('after_discount')
    def _compute_fees_after_discount(self):
        self.remaining_fee= self.after_discount

    def send_student_clinic(self):
        self.is_clinic = True
        # 1- For Nursing
        self.env['clinic.nursing'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'phone': self.student_mobile,
            'hom': self.local,
        })

        # 2- For Eye
        self.env['clinic.eye'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'phone': self.student_mobile,
            'home': self.local,
        })

        # # 3- For Mouth
        self.env['clinic.mouth'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'phone': self.student_mobile,
            'home': self.local,

        })

        # # 4- For Physical
        self.env['clinic.physical'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'phone': self.student_mobile,
            'home': self.local,

        })
        # 5- For Cicology
        self.env['clinic.psychological'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'social': self.social_status,
            'home': self.local,
            'email': self.email,
            'phone': self.telephone,

        })

        # # 6- For Laboratory
        self.env['clinic.laboratory'].create({
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'nationality': self.nationality_id.name,
            'religion': self.religion,
            'program': self.program_id.name,
            'patient_id': self.form_number,
            'phone': self.student_mobile,
            'home': self.local,
        })

    def create_student_user(self):
        pass







