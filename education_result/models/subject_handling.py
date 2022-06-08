from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, ValidationError
import datetime



class SubjectHandling(models.Model):
    _inherit = ['mail.thread']
    _rec_name = "subject_id"
    _name = 'subject.handling'
    _description = 'subject_handling information '

    college_id = fields.Many2one('college.college', string='College')
    program_id = fields.Many2one('program.program', string='Program', domain="[('college_id','=',college_id)]")
    level_id = fields.Many2one('level.level', string='Level')
    semester_id = fields.Many2one('semester.semester', string='Semester', domain="[('level_id','=',level_id)]")
    batch_id = fields.Many2one('batch.batch', string="Batch" )
    subject_id = fields.Many2one('student.subject', string='Subject Name', domain="[('semester_id','=',semester_id),('program_id','=',program_id),('level_id','=',level_id)]")
    handling_line_ids = fields.One2many('subject.handling.line', 'handling_id', string='Opportunities')
    state = fields.Selection([('draft', 'Drift'),('confirm', 'Confirm'),('waiting_approve', ' Waiting Approval'),('approve', 'Approval'), ('done', 'Done')], 'Status', default='draft')
    year = fields.Char('Study Year', default=lambda self: datetime.datetime.now().year)
    year_stady = fields.Char('Study Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    user_id = fields.Many2one('res.users', 'System User ', default=lambda self: self.env.user)

    # def unlink(self):
    #     if any(self.filtered(lambda r: r.state not in ('draft', 'cancel'))):
    #         raise UserError(_('You cannot delete a record which is not draft or cancelled!'))
    #     return super(SubjectHandling, self).unlink()

    def confirm_action(self):
        self.state ='confirm'

    def waiting_approve_action(self):
        for record in self:
            record.state = 'waiting_approve'

    def waiting_approve_action(self):
        for record in self:
            record.state = 'waiting_approve'
    def done_action(self):

                subject_degree = self.env['subject.degree'].search(
                    [('college_id', '=', self.college_id.id), ('program_id', '=', self.program_id.id),
                     ('level_id', '=', self.level_id.id), ('semester_id', '=', self.semester_id.id),
                     ('subject_id', '=', self.subject_id.id), ('year', '=', self.year)])
                degree_line = subject_degree.mapped("degree_line")
                for lin in self.handling_line_ids:
                    mark = degree_line.filtered(lambda r: r.student_id == lin.student_id)
                    mark.practical = mark.theoretical = mark.ass = 0.0
                    mark.final = lin.total

                self.state = 'done'
    def cancel_action(self):
            for record in self:
                record.state = 'draft'
    def calculated_results_action(self):
        average = self.env['calculation.average'].search(
            [('college_id', '=', self.college_id.id), ('program_id', '=', self.program_id.id),
             ('level_id', '=', self.level_id.id), ('year', '=', self.year)], limit=1)
        average_line = average.mapped("average_line")

        for rec in average_line:
            if rec.student_id.id == self.handling_line_ids.student_id.id:
                 print('===========================')


    @api.onchange('subject_id')
    def set_student_line(self):
        subject_degree = self.env['subject.degree'].search([('college_id', '=', self.college_id.id), ('program_id', '=', self.program_id.id),('level_id', '=', self.level_id.id), ('semester_id', '=', self.semester_id.id),('subject_id', '=', self.subject_id.id), ('year', '=', self.year)])
        if subject_degree:
            self.handling_line_ids = [(5, 0, 0)]
            self.write({'handling_line_ids': [(0, 0, {
                'student_id': rec.student_id.id,
                'exam_state': rec.exam_state,
            }) for rec in subject_degree.degree_line.filtered(lambda r: r.total < 50 )]})
            # and r.exam_state in ['absent', 'substution']
    class ResultLine(models.Model):
        _name = 'subject.handling.line'
        student_id = fields.Many2one('student.registrar', string='Student Name')
        handling_id = fields.Many2one('subject.handling', string='Subject Handling')
        exam_state = fields.Selection([('absent', 'Absent'),('substution', 'Substution'),('deprivation', 'Deprivation')])
        total = fields.Integer( string='Total Mark')














