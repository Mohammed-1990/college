from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
import datetime



class Result(models.Model):
    _inherit = ['mail.thread']
    _rec_name = "subject_id"
    _name = 'subject.degree'
    _description = 'result information '

    college_id = fields.Many2one('college.college', string='College')
    program_id = fields.Many2one('program.program', string='Program', domain="[('college_id','=',college_id)]")
    level_id = fields.Many2one('level.level', string=' level')
    semester_id = fields.Many2one('semester.semester', string='Semester', domain="[('level_id','=',level_id)]")
    batch_id = fields.Many2one('batch.batch', string="Batch" )
    subject_id = fields.Many2one('student.subject', string='Subject Name', domain="[('semester_id','=',semester_id),('program_id','=',program_id),('level_id','=',level_id)]")
    degree_line = fields.One2many('subject.degree.line', 'degree_id', string='Opportunities')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('program_board', 'Program Board'),('board_examiners', 'Board Examiners'),('scientific_affairs', 'Scientific Affairs'), ('scientific_council', 'Scientific Council') ,('done', 'Done')], 'Status', default='draft')
    year = fields.Char(' Year', default=lambda self: datetime.datetime.now().year)
    year_stady = fields.Char('Study Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    user_id = fields.Many2one('res.users', 'System User ', default=lambda self: self.env.user)

    def confirm_action(self):
        for record in self:
            record.state = 'confirm'

    def program_board_approve_action(self):
        for record in self:
            record.state = 'program_board'

    def board_examiners_approve_action(self):
        for record in self:
            record.state = 'board_examiners'

    def scientific_affairs_approve_action(self):
        for record in self:
            record.state = 'scientific_affairs'

    def scientific_affairs_approve_action(self):
        for record in self:
            record.state = 'scientific_affairs'

    def scientific_council_approve_action(self):
        for record in self:
            record.state = 'scientific_council'

    def done_action(self):
        for record in self:
            record.state = 'done'


    def grade_calculation(self):
        max_degree = max(self.degree_line.filtered(lambda r: r.total).mapped("total"))
        if max_degree >= 80:
            num = round((max_degree - 50)/6)
            a = 50
            y = a + num
            for rec in self.degree_line:
                if rec.total <= 49 :
                    rec.grad = "F"
                    y = y - 1
                if rec.total >= 50 :
                    rec.grad = "C"
                    b = a + num
                if rec.total >= 55 :
                    rec.grad = "C+"
                    c = b + num
                if rec.total >= 60 :
                    rec.grad = "B"
                    d = c + num
                if rec.total >= 65 :
                    rec.grad = "B+"
                    e = d + num
                if rec.total >= 75 :
                    rec.grad = "A"
                    f = e + num
                if rec.total >= 80 :
                    rec.grad = "A+"



        if max_degree >= 70 and max_degree < 80:
            num = round((max_degree - 50)/5)
            a = 50
            y = a + num
            for rec in self.degree_line:
                if rec.total <= 49 :
                    rec.grad = "F"
                    y = y - 1
                if rec.total >= 50 :
                    rec.grad = "C"
                    b = a + num
                if rec.total >= 54 :
                    rec.grad = "C+"
                    c = b + num
                if rec.total >= 59 :
                    rec.grad = "B"
                    d = c + num
                if rec.total >= 64 :
                    rec.grad = "B+"
                    e = d + num
                if rec.total >= 70 :
                    rec.grad = "A"


        if max_degree < 70:
            num = round((max_degree - 50) / 4)
            a = 50
            y = a + num
            for rec in self.degree_line:
                if rec.total <= 49:
                    rec.grad = "F"
                    y = y - 1
                if rec.total >= 50:
                    rec.grad = "C"
                    b = a + num
                if rec.total >= 53:
                    rec.grad = "C+"
                    c = b + num
                if rec.total >= 58:
                    rec.grad = "B"
                    d = c + num
                if rec.total >= 60:
                    rec.grad = "B+"

    @api.onchange('subject_id')
    def set_student_line(self):
        get_student_list = []
        student_id = self.env['student.registrar'].search([('program_id', '=', self.program_id.id),('level_id', '=', self.level_id.id),('semester_id', '=', self.semester_id.id)])
        if student_id:
            for rec in student_id:
                get_student_list.append(rec.id)
        self.degree_line = [(5, 0, 0)]
        self.write({'degree_line': [(0, 0, {
            'student_id': rec,
            'subject_id': self.subject_id.id,
        }) for rec in get_student_list]})

    # def unlink(self):
    #     for rec in self:
    #         if rec.state != 'draft':
    #             raise UserError(
    #                 ('You Cannot Delete The Result  Which  State Is Not Draft or Cancelled.'))
    #     return super(Result, self).unlink()


    class ResultLine(models.Model):
        _name = 'subject.degree.line'

        student_id = fields.Many2one('student.registrar', string='Student Name')
        degree_id = fields.Many2one('subject.degree', string='degree')
        subject_id = fields.Many2one('student.subject', string='Subject')
        practical = fields.Integer(string='Practical')
        theoretical  = fields.Integer(string='Theoretical ')
        ass = fields.Integer(string='Test')
        final = fields.Integer(string='Final')
        exam_state = fields.Selection([('absent', 'Absent'),('substution', 'Substution'),('deprivation', 'Deprivation'),('cheating', 'Cheating Case')])
        total = fields.Integer( string='Total Mark', store=True, compute="_compute_subject_degree")
        grad = fields.Char(string="Grade")

        @api.depends('ass', 'practical','theoretical', 'final')
        def _compute_subject_degree(self):
            for lin in self:
                if lin.ass < 0 or lin.practical < 0 or lin.theoretical < 0 or lin.final < 0:
                    raise UserError(_('The degree  cannot be negative.'))
                lin.total = lin.ass+lin.practical+lin.theoretical+lin.final
                if lin.total > 100:
                    raise UserError(_('The degree  cannot be < than 100.'))














