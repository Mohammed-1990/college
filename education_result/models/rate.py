from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, ValidationError
import datetime



class CalculationRate(models.Model):
    _inherit = ['mail.thread']
    _name = 'calculation.rate'
    _description = 'average rate'
    college_id = fields.Many2one('college.college', string='College')
    program_id = fields.Many2one('program.program', string='Program', domain="[('college_id','=',college_id)]")
    level_id = fields.Many2one('level.level', string='Level')
    semester_id = fields.Many2one('semester.semester', string='Semester', domain="[('level_id','=',level_id)]")
    rate_line_ids = fields.One2many('line.rate', 'rate_id', string='Opportunities')
    state = fields.Selection([('draft', 'Drift'),('confirm', 'Confirm'),('waiting_approve', 'Waiting Approval'),('approve', 'Approval'), ('done', 'Done')], 'Status', default='draft')
    year = fields.Char('Study Year', default=lambda self: datetime.datetime.now().year)
    year_stady = fields.Char('Study Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    def confirm_action(self):
        for record in self:
            record.state = 'confirm'

    def waiting_approve_action(self):
        for record in self:
            record.state = 'waiting_approve'

    def waiting_approve_action(self):
        for record in self:
            record.state = 'waiting_approve'

    def done_action(self):
        for record in self:
            record.state = 'done'

    def cancel_action(self):
        for record in self:
            record.state = 'draft'


    @api.onchange('semester_id')
    def get_subject_degree(self):
        hour =[]
        mark =[]
        total =[]
        self.rate_line_ids =[(5,0,0)]
        rate_ids = self.env['calculation.rate'].search([('college_id', '=', self.college_id.id), ('program_id', '=', self.program_id.id),('level_id', '=', self.level_id.id), ('year', '=', self.year)], limit=1)
        degree_ids = self.env['subject.degree'].search([('program_id', '=', self.program_id.id),('level_id', '=', self.level_id.id),('semester_id', '=', self.semester_id.id)])
        subject_degree_line =degree_ids.mapped("degree_line")
        studant_ids = subject_degree_line.mapped("student_id")

        if rate_ids:
            chack_rate= self.env['calculation.rate'].search(
                [('college_id', '=', self.college_id.id), ('program_id', '=', self.program_id.id),
                 ('level_id', '=', self.level_id.id), ('semester_id', '=', self.semester_id.id),
                 ('year', '=', self.year)], limit=1)
            if chack_rate:
                raise ValidationError(_('The result of this semester has already been entered.'))
            else:
                average_lin = rate_ids.mapped("average_line")
                for rec in studant_ids:
                    semester_average = average_lin.filtered(lambda r: r.student_id == rec)
                    subject_degree = subject_degree_line.filtered(lambda r: r.student_id == rec)
                    for lin in subject_degree:
                        total.append(lin.total)
                        mark.append(lin.subject_id.hours * lin.total)
                        hour.append(lin.subject_id.hours)
                        cumulative_average = round((sum(mark) / sum(hour) / 25), 2)

                    result = ((semester_average.semester_average * semester_average.hours) + (
                                cumulative_average * sum(hour))) / (semester_average.hours + sum(hour))
                    self.write({'average_line': [(0, 0, {
                        'student_id': line.id,
                        'semester_average': semester_average.semester_average,
                        'cumulative_average': cumulative_average,
                        'result': result,
                        'decision': 'pass',

                    }) for line in rec]})
                    mark.clear()
                    total.clear()
                    hour.clear()

        else:
            for rec in studant_ids:
                subjects = subject_degree_line.filtered(lambda r: r.student_id == rec)
                for lin in subjects:
                    hour.append(lin.subject_id.hours)
                    mark.append(lin.subject_id.hours * lin.total)
                self.write({'rate_line_ids': [(0, 0, {
                    'student_id': line.id,
                    'hours': sum(hour),
                     'semester_average': round((sum(mark)/sum(hour)/25),2),
                    'cumulative_average': 0,

                }) for line in rec]})

class AverageLine(models.Model):
    _name = 'line.rate'
    _description = 'average calculation Line'

    rate_id = fields.Many2one('calculation.rate', string='Rate')
    student_id = fields.Many2one('student.registrar', string='Student Name')
    hours = fields.Float(string="number of hours")
    semester_average = fields.Float(string='S-GPA I',digits = (1,2))
    cumulative_average = fields.Float(string='S-GPA II' ,digits = (1,2))
    result = fields.Float(string='GPA' ,digits = (1,2))
    sub =fields.Integer(string='Sub')
    supp =fields.Integer(string='Supp')
    decision = fields.Selection([('pass', 'Pass'), ('second', 'Second Period')], string="Decision")









