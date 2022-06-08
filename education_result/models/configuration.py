from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
import datetime
import re

class subject(models.Model):
    _inherit = ['mail.thread']
    _name = 'student.subject'
    _description = 'subject information '

    name = fields.Char(string="Subject")
    college_id = fields.Many2one('college.college', string='College')
    program_id = fields.Many2one('program.program', string='Program', domain="[('college_id','=',college_id)]")
    level_id = fields.Many2one('level.level', string=' Level')
    semester_id = fields.Many2one('semester.semester', string='Semester', domain="[('level_id','=',level_id)]")
    code = fields.Char(string="Code")
    hours = fields.Integer(string="hours")
    year = fields.Char('Year', default=lambda self: datetime.datetime.now().year)
    user_id = fields.Many2one('res.users', 'System User ', default=lambda self: self.env.user)

    @api.constrains('name')
    def validate_subject_name(self):
        if self.name:
            if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                raise UserError(_('The Value Of Subject Name Must Be Only Letters'))

    @api.constrains('code')
    def validate_subject_code(self):
        if self.code:
            if self.code == None :
                raise UserError(_('The Value Of Subject Code Must Be Positive Number'))
    @api.constrains('hours')
    def validate_subject_code(self):
            if self.hours <=0 :
                raise UserError(_('The Value Of Subject Hours Must Be Positive Number'))

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Name Of Subject Must Be Unique"),
        ('code_unique',
         'UNIQUE(code)',
         "The Code  Must Be Unique"),
    ]




