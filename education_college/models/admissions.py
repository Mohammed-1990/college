from odoo import models, fields, api, _
import datetime
import re

from odoo.exceptions import UserError


class EducatinAdmissions(models.Model):
    _inherit = ['mail.thread']
    _order = "id desc"
    _name = 'new.admission'
    _description = 'add admission information'
    _inherits = {"res.partner": "partner_id"}

    first = fields.Char(string="First Name")
    second = fields.Char(string="Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    college_id = fields.Many2one('college.college', string='College', ondelete='cascade',
                                 default=lambda self: self.env['college.college'].search([]))
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program",
                                 domain="[('college_id', '=', college_id)]")
    batch_id = fields.Many2one('batch.batch', string='Batch', ondelete='cascade',
                               domain="[('program_id','=',program_id),('year','=',datetime.datetime.now().year)]")
    level_id = fields.Many2one('level.level', ondelete='cascade', string="Level",
                               default=lambda self: self.env['level.level'].search([]))
    semester_id = fields.Many2one('semester.semester', ondelete='cascade', string="Semester",
                                  domain="[('level_id','=',level_id)]",
                                  default=lambda self: self.env['semester.semester'].search([]))
    admission_type = fields.Selection(
        [('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'),
         ('tow_vacancy', 'Vacancy Tow'), ('scholarship', 'Scholarship')], string="Type Of Admission", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('waiting_approve', 'Waiting Approve'), ('done', 'done'),
         ('cancel', 'Cancel')], string='Status', default="draft", readonly=True)
    school_name = fields.Char(string="School Name ")
    student_number = fields.Char(string="Form Number", size=10)
    year_stady = fields.Char('Admission Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    company_id = fields.Many2one('res.company', string='Company')
    accept_year = fields.Char('Admission Year', default=lambda self: datetime.datetime.now().year)
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    @api.constrains('student_number')
    def check_studentNumber(self):
        for record in self:
            obj = self.search([('student_number', '=', record.student_number), ('id', '!=', record.id)])
            self.form_numper =self.student_number
            self.is_student =True
            if obj:
                raise UserError('The Number Of Student Must Be Unique!')

    @api.onchange('first', 'second', 'third', 'last')
    def _onchange_name(self):
        self.name = str(self.first) + " " + str(
            self.second) + " " + str(self.third)+ " " + str(self.last)

    @api.onchange('program_id')
    def get_company(self):
        for rec in self:
            rec.company_id = rec.program_id.company_id.id



    @api.constrains('first')
    def validate_student_full_name(self):
        if self.first:
            if not re.search(r'^(?:[^\W\d_]| )+$',
                             self.first + " " + self.second + " " + self.third + " " + self.last) != None:
                raise UserError(_('The value Of Student Name Must Be Only Letters'))

    @api.constrains('student_number')
    def validate_student_number(self):
        if self.student_number:
            if not re.match("^[0-9]*$", self.student_number) != None:
                raise UserError(_('The value of Form Number Must Be Positive Number'))

    def draft_action(self):
        self.state = 'confirm'

    def waiting_approve_action(self):
        self.state = 'waiting_approve'

    def done_action(self):
        val = {
            'name': self.name,
            'college_id': self.college_id.id,
            'program_id': self.program_id.id,
            'level_id': self.level_id.id,
            'semester_id': self.semester_id.id,
            'batch_id': self.batch_id.id,
            'type_acceptance': self.admission_type,
            'school_name': self.school_name,
            'form_number': self.student_number,
            'accept_year': self.accept_year,
            'year_stady': self.year_stady,
            'company_id': self.company_id.id,
        }
        self.env['new.student'].create(val)
        self.state = 'done'

    def cancel_acrion(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete an Admission Which Is Not Draft Or Cancelled. You Should Refund It Instead.'))
        return super(EducatinAdmissions, self).unlink()


class EducatinDegreeHolder(models.Model):
    _inherit = ['mail.thread']
    _order = "id desc"
    _name = 'degree.holder'
    _description = 'add degree holder'
    _inherits = {"res.partner": "partner_id"}

    univercity_name = fields.Char(string="University  Name ")
    type_of_certificate = fields.Selection([('sudanese', 'Sudanese'), ('arabic', 'Arabic'), ('other', 'Other')],
                                           string="Type Of Certificate")
    first = fields.Char(string="First Name")
    second = fields.Char(string="Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")

    college_id = fields.Many2one('college.college', string='College', ondelete='cascade',
                                 default=lambda self: self.env['college.college'].search([]))

    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program",
                                 domain="[('college_id', '=', college_id)]")
    batch_id = fields.Many2one('batch.batch', string='Batch', ondelete='cascade',
                               domain="[('program_id','=',program_id),('year','=',datetime.datetime.now().year)]")
    level_id = fields.Many2one('level.level', ondelete='cascade', string="Level")
    semester_id = fields.Many2one('semester.semester', ondelete='cascade', string="Semester",
                                  domain="[('level_id','=',level_id)]")
    student_number = fields.Char(string="Form Number", )
    school_name = fields.Char(string="School Name ")
    accept_year = fields.Char('Admission Year', default=lambda self: datetime.datetime.now().year)

    old_accept_type = fields.Selection([
        ('degree_holder', 'حملة الدرجات العلمية'),
        ('transfer', 'التحويل من جامعة الي اخري'),
        ('bridging', 'التجسير'),
        ('mature', 'ناضجين'),
    ], string="Admission After First Year")

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('waiting_approve', 'Waiting Approve'), ('done', 'done'),
         ('cancel', 'Cancel')], string='Status', default="draft", readonly=True)

    batch_id = fields.Many2one('batch.batch', string='Batch', ondelete='cascade',
                               domain="[('program_id', '=', program_id)]")
    company_id = fields.Many2one('res.company', string='Company',)
    year_stady = fields.Char('Admission Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    @api.onchange('first', 'second', 'third', 'last')
    def _onchange_name(self):
        self.name = str(self.first) + " " + str(
            self.second) + " " + str(self.third) + " " + str(self.last)

    @api.onchange('program_id')
    def get_company(self):
        for rec in self:
            rec.company_id = rec.program_id.company_id.id

    @api.constrains('student_number')
    def check_studentNumber(self):
        for record in self:
            obj = self.search([('student_number', '=', record.student_number), ('id', '!=', record.id)])
            self.form_numper = self.student_number
            self.is_student = True
            if obj:
                raise UserError('The Number Of Student Must Be Unique!')

    def draft_action(self):
        self.state = 'confirm'

    def waiting_approve_action(self):
        self.state = 'waiting_approve'

    def done_action(self):
        val = {
            'name': self.name,
            'college_id': self.college_id.id,
            'program_id': self.program_id.id,
            'level_id': self.level_id.id,
            'semester_id': self.semester_id.id,
            'batch_id': self.batch_id.id,
            'old_accept_type': self.old_accept_type,
            'school_name': self.school_name,
            'form_number': self.student_number,
            'accept_year': self.accept_year,
            'type_of_certificate': self.type_of_certificate,
            'company_id': self.company_id.id,
            'year_stady': self.year_stady,
        }
        self.env['old.student'].create(val)
        print(self.name)
        # self.state = 'done'
