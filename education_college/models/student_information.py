import datetime
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError, ValidationError

import re


class StudantInformation(models.Model):
    _inherit = ['mail.thread']
    _name = 'new.student'
    _description = 'new student basic  information'
    _order = "id desc"

    name = fields.Char(string="Full Name")
    first = fields.Char(string="First Name")
    second = fields.Char(string="Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")
    image_1920 = fields.Binary('image_1920')
    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    level_id = fields.Many2one('level.level', ondelete='cascade', string="Level")
    semester_id = fields.Many2one('semester.semester', ondelete='cascade', string="Semester")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    type_acceptance = fields.Selection(
        [('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'),
         ('tow_vacancy', 'Vacancy Tow'), ('scholarship', 'Scholarship')], straing='Type Of Acceptance')
    nationality_id = fields.Many2one('res.country', string="Nationality")
    type_of_id = fields.Selection(
        [('national_number', 'National  Number'), ('national_card', 'National Card'), ('passport', 'Passport')],
        string="Personality Type")
    id_number = fields.Char(string="The National Number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")

    religion = fields.Selection([('muslim', 'Muslim'), ('christian', 'Christian '), ('other', 'Other')],default ="muslim",
                                string="Religion")
    social_status = fields.Selection([ ('single', 'Single '), ('married', 'Married'),('other', 'Other')], default="single",
                                     string="Social Status")
    birth_date = fields.Date(string="Birth Date")
    address = fields.Char(string="Place Of Birth")
    student_states = fields.Char(string="State")
    local = fields.Char(straing='Local')
    email = fields.Char(string="Email")
    student_mobile = fields.Char(string="Mobile Number")
    whatsapp_phone = fields.Char(string="Whatsapp")
    school_name = fields.Char(string='School Name ')
    sitting_number = fields.Char(string="Sitting Number")
    ratio = fields.Float(string="The Ratio")
    type_of_certificate = fields.Selection(
        [('sudanese', 'Sudanese'), ('arabic', 'Arabic'), ('other', 'Other')],
        string="Type Of Certificate")

    course = fields.Selection([('scientific', 'Scientific'), ('literary', 'Literary')], string="The course")
    form_number = fields.Char(string='Form Number')
    year_stady = fields.Char('Admission Year')
    accept_year = fields.Char(string='Year Of Admission ')
    national_card = fields.Binary(string="National Card")
    school_certificate = fields.Binary(string="High School Certificate")
    applicant = fields.Char(string="Applicant  Name")
    job = fields.Char(string="Job")
    fother_address = fields.Char(string="Address")
    telephone = fields.Char(string="Telephone")
    relative_relation = fields.Char(string="Relative Relation")
    facebook = fields.Boolean(string="Face Book")
    website = fields.Boolean(string="Web Site")
    newspaper = fields.Boolean(string="Newspaper")
    tv = fields.Boolean(string="TV")
    radio = fields.Boolean(string="Radio")
    admission_book = fields.Boolean(string="Admission Book")
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('waiting_approve', 'Waiting Approve'), ('done', 'done') ,('cancel', 'Cancel')], string='Status', default="draft", readonly=True)
    comm_new = fields.Text(string="Comment", readonly="True",  default="اقر انا بصحة البيانات اعلاه و ان التزم بقوانين الكلية وان اتحلى بالسلوك و القيم الفاضلة و اللبس الموحد المحتشم و ان يكون التزامي بسداد المصروفات المقررة التزاما يحقق لي الدراسة من غير انقطاع او مطالبة متكررة و ذلك عند بداية كل فصل دراسي و عدم المطالبة بهذه المصروفات بعد بداية الدراسة او عند انقطاعي عن دراسي لاي سبب و هذا اقرار مني بذلك.")
    company_id = fields.Many2one('res.company', string='Company')

    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    @api.constrains('id_number')
    def validate_id_number(self):
        if self.id_number:
            if not re.match("^[0-9]*$", self.id_number) != None:
                raise UserError(_('The value of Form  ID Number must be positive number'))

    @api.constrains('applicant')
    def validate_applicant(self):
        if self.applicant:
            if not re.search(r'^(?:[^\W\d_]| )+$', self.applicant) != None:
                raise UserError(_('The value of applicant name must only letters'))
    
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date < fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    def confirm_action(self):
        self.state = 'confirm'

    def waiting_approve_action(self):
        self.state = 'waiting_approve'



    def done_action(self):

        self.env['student.registrar'].create({
            'name': self.name,
            'image_1920': self.image_1920,
            'college_id': self.college_id.id,
            'program_id': self.program_id.id,
            'level_id': self.level_id.id,
            'semester_id': self.semester_id.id,
            'batch_id': self.batch_id.id,
            'type_acceptance': self.type_acceptance,
            'id_number': self.id_number,
            'type_of_id': self.type_of_id,
            'gender': self.gender,
            'religion': self.religion,
            'social_status': self.social_status,
            'birth_date': self.birth_date,
            'states': self.student_states,
            'nationality_id': self.nationality_id.id,
            'local': self.local,
            'student_mobile': self.student_mobile,
            'whatsapp_phone': self.whatsapp_phone,
            'email': self.email,
            'school_name': self.school_name,
            'sitting_number': self.sitting_number,
            'ratio': self.ratio,
            'type_of_certificate': self.type_of_certificate,
            'course': self.course,
            'form_number': self.form_number,
            'accept_year': self.accept_year,
            'national_card': self.national_card,
            'school_certificate': self.school_certificate,
            'fother_address': self.fother_address,
            'telephone': self.telephone,
            'job': self.job,
            'relative_relation': self.relative_relation,
            'applicant': self.applicant,
            'company_id': self.company_id.id,

        })
        # self.state = 'done'

    def cancel_acrion(self):
        self.state = 'confirm'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete an Studant Information Which Is Not Draft Or Cancelled. You Should Refund It Instead.'))
        return super(StudantInformation, self).unlink()





class OldStudantInformation(models.Model):
    _inherit = ['mail.thread']
    _name = 'old.student'
    _description = 'old student basic  information'
    _order = "id desc"

    name = fields.Char(string="Full Name")
    first = fields.Char(string="First Name")
    second = fields.Char(string="Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")
    image_1920 = fields.Binary('image_1920')
    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    level_id = fields.Many2one('level.level', ondelete='cascade', string="Level")
    semester_id = fields.Many2one('semester.semester', ondelete='cascade', string="Semester")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    nationality_id = fields.Many2one('res.country', string="Nationality")
    type_of_id = fields.Selection(
        [('national_number', 'National  Number'), ('national_card', 'National Card'), ('passport', 'Passport')],
        string="Personality Type")
    id_number = fields.Char(string="The National Number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    religion = fields.Selection([('muslim', 'Muslim'), ('christian', 'Christian '), ('other', 'Other')],
                                string="Religion")
    social_status = fields.Selection([('married', 'Married'), ('single', 'Single '), ('other', 'Other')],
                                     string="Social Status")
    birth_date = fields.Date(string="Birth Date")
    address = fields.Char(string="Place Of Birth")
    student_states = fields.Char(string="State")
    local = fields.Char(straing='Local')
    email = fields.Char(string="Email")
    student_mobile = fields.Char(string="Mobile Number")
    whatsapp_phone = fields.Char(string="Whatsapp")
    school_name = fields.Char(string='School Name ')
    sitting_number = fields.Char(string="Sitting Number")
    ratio = fields.Float(string="The Ratio")
    type_of_certificate = fields.Selection(
        [('sudanese', 'Sudanese'), ('arabic', 'Arabic'), ('other', 'Other')],
        string="Type Of Certificate")

    course = fields.Selection([('scientific', 'Scientific'), ('literary', 'Literary')], string="The course")
    form_number = fields.Char(string='Form Number')
    year_stady = fields.Char('Admission Year', default=lambda self: datetime.datetime.now().year)
    accept_year = fields.Char(string='Year Of Admission ')
    national_card = fields.Binary(string="National Card")
    school_certificate = fields.Binary(string="High School Certificate")
    applicant = fields.Char(string="Applicant  Name")
    job = fields.Char(string="Job")
    fother_address = fields.Char(string="Address")
    telephone = fields.Char(string="Telephone")
    relative_relation = fields.Char(string="Relative Relation")
    facebook = fields.Boolean(string="Face Book")
    website = fields.Boolean(string="Web Site")
    newspaper = fields.Boolean(string="Newspaper")
    tv = fields.Boolean(string="TV")
    radio = fields.Boolean(string="Radio")
    admission_book = fields.Boolean(string="Admission Book")
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('waiting_approve', 'Waiting Approve'), ('done', 'done') ,('cancel', 'Cancel')], string='Status', default="draft", readonly=True)
    comm_new = fields.Text(string="Comment", readonly="True",  default="اقر انا بصحة البيانات اعلاه و ان التزم بقوانين الكلية وان اتحلى بالسلوك و القيم الفاضلة و اللبس الموحد المحتشم و ان يكون التزامي بسداد المصروفات المقررة التزاما يحقق لي الدراسة من غير انقطاع او مطالبة متكررة و ذلك عند بداية كل فصل دراسي و عدم المطالبة بهذه المصروفات بعد بداية الدراسة او عند انقطاعي عن دراسي لاي سبب و هذا اقرار مني بذلك.")
    company_id = fields.Many2one('res.company', string='Company')

    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    old_accept_type = fields.Selection([
        ('degree_holder', 'حملة الدرجات العلمية'),
        ('transfer', 'التحويل من جامعة الي اخري'),
        ('bridging', 'التجسير'),
        ('mature', 'ناضجين'),
    ], string="Admission After First Year")

    certificate_level = fields.Selection([
        ('bachelors', 'Bachelors'),
        ('diploma', 'Diploma'),
        ('other', 'Other'),
    ], string="Certificate Level")
    certificate_completion = fields.Binary(string="Certificate Completion")
    certificate_details = fields.Binary(string="Certificate Details")
    certificate_other = fields.Binary(string="Certificate Other")
    conduct_certificate = fields.Binary(string="Conduct Certificate")
    academic_profile = fields.Binary(string="Academic Profile ")
    comm_old = fields.Text(string="Comment", readonly="True",  default="اقر انا بصحة البيانات اعلاه و ان التزم بقوانين الكلية وان اتحلى بالسلوك و القيم الفاضلة و اللبس الموحد المحتشم و ان يكون التزامي بسداد المصروفات المقررة التزاما يحقق لي الدراسة من غير انقطاع او مطالبة متكررة و ذلك عند بداية كل فصل دراسي و عدم المطالبة بهذه المصروفات بعد بداية الدراسة او عند انقطاعي عن دراسي لاي سبب و هذا اقرار مني بذلك.")

    @api.constrains('id_number')
    def validate_id_number(self):
        if self.id_number:
            if not re.match("^[0-9]*$", self.id_number) != None:
                raise UserError(_('The value of Form  ID Number must be positive number'))

    @api.constrains('applicant')
    def validate_applicant(self):
        if self.applicant:
            if not re.search(r'^(?:[^\W\d_]| )+$', self.applicant) != None:
                raise UserError(_('The value of applicant name must only letters'))

    def confirm_action(self):
        self.state = 'confirm'

    def waiting_approve_action(self):
        self.state = 'waiting_approve'

    def done_action(self):

        self.env['student.registrar'].create({
            'name': self.name,
            'image_1920': self.image_1920,
            'college_id': self.college_id.id,
            'program_id': self.program_id.id,
            'level_id': self.level_id.id,
            'semester_id': self.semester_id.id,
            'batch_id': self.batch_id.id,
            'old_accept_type': self.old_accept_type,
            'id_number': self.id_number,
            'type_of_id': self.type_of_id,
            'gender': self.gender,
            'religion': self.religion,
            'social_status': self.social_status,
            'birth_date': self.birth_date,
            'states': self.student_states,
            'nationality_id': self.nationality_id.id,
            'local': self.local,
            'student_mobile': self.student_mobile,
            'whatsapp_phone': self.whatsapp_phone,
            'email': self.email,
            'school_name': self.school_name,
            'sitting_number': self.sitting_number,
            'ratio': self.ratio,
            'type_of_certificate': self.type_of_certificate,
            'certificate_level': self.certificate_level,
            'course': self.course,
            'form_number': self.form_number,
            'accept_year': self.accept_year,
            'national_card': self.national_card,
            'school_certificate': self.school_certificate,
            'fother_address': self.fother_address,
            'telephone': self.telephone,
            'job': self.job,
            'relative_relation': self.relative_relation,
            'applicant': self.applicant,
            'company_id': self.company_id.id,

        })
        # self.state = 'done'

    def cancel_acrion(self):
        self.state = 'confirm'






