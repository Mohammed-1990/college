from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
import re
from datetime import datetime

class EducationCollege(models.Model):
    _inherit = ['mail.thread']
    _name = 'college.college'
    _description = 'add college  information'

    name = fields.Char(string="College Name")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    @api.constrains('name')
    def validate_college_name(self):
        if self.name:
            if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                raise UserError(_('The Value Of College Name Must Be Only Letters'))

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Name Of College Must Be Unique"),
    ]

    class EducationProgram(models.Model):
        _inherit = ['mail.thread']
        _name = 'program.program'
        _description = 'add  program information '

        name = fields.Char(string="Program")
        college_id = fields.Many2one('college.college',
                                     ondelete='cascade', string="College Name",
                                     default=lambda self: self.env['college.college'].search([]))
        code = fields.Char(string="Code", size=12)
        company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

        @api.constrains('name')
        def validate_program_name(self):
            if self.name:
                if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                    raise UserError(_('The Value Of Program Name Must Be Only Letters'))

        @api.constrains('code')
        def validate_program_code(self):
            if self.code:
                if self.code == None:
                    raise UserError(_('The Value Of Program Code Must Be Positive Number'))

        _sql_constraints = [
            ('name_unique',
             'UNIQUE(name)',
             "The Name Of Program Must Be Unique"),
            ('code_unique',
             'UNIQUE(code)',
             "The Code  Must Be Unique"),
        ]


    class EducationLevel(models.Model):
        _inherit = ['mail.thread']
        _name = 'level.level'
        _description = 'add level information'

        name = fields.Char(string="Academic  Level")
        company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

        @api.constrains('name')
        def validate_level_name(self):
            if self.name:
                if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                    raise UserError(_('Academic  Level  Must Be Only Letters'))

        _sql_constraints = [
            ('name_unique',
             'UNIQUE(name)',
             "Academic  Level Must Be Unique"),
        ]

    class EducationSemester(models.Model):
        _inherit = ['mail.thread']
        _name = 'semester.semester'
        _description = ' add semester information'

        name = fields.Char(string="Semester")
        level_id = fields.Many2one('level.level', string='Academic level')
        company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

        @api.constrains('name')
        def validate_semester_name(self):
            if self.name:
                if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                    raise UserError(_('Semester Name  Must Be Only Letters'))

        _sql_constraints = [
            ('name_unique',
             'UNIQUE(name)',
             "Semester Name Must Be Unique"),
        ]

    class EducationBatch(models.Model):
        _inherit = ['mail.thread']
        _name = 'batch.batch'
        _order = "id desc"
        _description = 'add  batch information '
        name = fields.Char(string="Batch Name")
        college_id = fields.Many2one('college.college',ondelete='cascade', string="Collage Name",
                                     default=lambda self: self.env['college.college'].search([]))
        program_id = fields.Many2one('program.program', ondelete='cascade', string='Program')
        # study_year = fields.Char(string='Study Year',default=str(datetime.today().year-1) + " - " + str(datetime.today().year))
        study_year = fields.Char(string='Study Year',compute='get_study_year', store=True)
        # year = fields.Char(default=datetime.today().year)
        year = fields.Char( )
        company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

        @api.depends('year')
        def get_study_year(self):
            self.study_year = str(self.year+1) + " - " + str(self.year)

        @api.constrains('name')
        def validate_batch_name(self):
            if self.name:
                if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                    raise UserError(_('Batch Name  Must Be Only Letters'))




        @api.onchange('college_id')
        def get_program(self):
            college = self.env['program.program'].search([('college_id', '=', self.college_id.id)]).mapped("id")
            if college:
                return {'domain': {'program_id': [('id', 'in', college)]}}


    class EducationSpecialization(models.Model):
        _inherit = ['mail.thread']
        _name = 'specialization.specialization'
        _description = ' add specialization information  '

        name = fields.Char(string="Specialization", help="enter Name of Specialization")
        college_id = fields.Many2one('college.college',ondelete='cascade', string="College",
                                     default=lambda self: self.env['college.college'].search([]))
        program_id = fields.Many2one('program.program',
                                     ondelete='cascade', string="Program")
        company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

        @api.onchange('college_id')
        def get_program(self):
            college = self.env['program.program'].search([('college_id', '=', self.college_id.id)]).mapped("id")
            if college:
                return {'domain': {'program_id': [('id', 'in', college)]}}

            @api.constrains('name')
            def validate_specialization_name(self):
                if self.name:
                    if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                        raise UserError(_('Specialization  Name Must Be Only Letters'))

            _sql_constraints = [
                ('name_unique',
                 'UNIQUE(name)',
                 "Specialization Name  Must Be Unique"),
            ]


    class EducationTypeOfAdmissio(models.Model):
        _inherit = ['mail.thread']
        _name = 'type.admission'
        _description = 'type of admission '

        admission_type = fields.Selection([('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'), ('tow_vacancy', 'Vacancy Tow'),('scholarship', 'Scholarship')],string="Type Of Admission" ,required=True)
        nationality = fields.Selection([('sudanese','Sudanese'),('foreigner','Foreigners')],string="Nationality", required=True)



        class OtherRevenue(models.Model):
            _inherit = ['mail.thread']
            _name = 'other.revenue'
            _description = ' add revenue type information '

            name = fields.Char(string="Revenue Name")
            company_id = fields.Many2one('res.company', string='Company')

            @api.constrains('name')
            def validate_revenue_name(self):
                if self.name:
                    if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                        raise UserError(_('Revenue Name  Must Be Only Letters'))

            _sql_constraints = [
                ('name_unique',
                 'UNIQUE(name)',
                 "Other Revenue Name  Must Be Unique"),
            ]
