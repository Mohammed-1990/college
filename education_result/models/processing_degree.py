from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
import datetime



class Result(models.Model):
    _inherit = ['mail.thread']
    _name = 'processing.degree'
    _description = '  Processing student grades information '

    college_id = fields.Many2one('college.college', string='College')
    program_id = fields.Many2one('program.program', string='program', domain="[('college_id','=',college_id)]")
    level_id = fields.Many2one('level.level', string=' level')
    semester_id = fields.Many2one('semester.semester', string='semester', domain="[('level_id','=',level_id)]")
    batch_id = fields.Many2one('batch.batch', string="Batch" )
    Subject_id = fields.Many2one('student.subject', string='the Subject', domain="[('semester_id','=',semester_id),('program_id','=',program_id),('level_id','=',level_id)]")
    handling_line_ids = fields.One2many('subject.handling.line', 'handling_id', string='Opportunities')
    state = fields.Selection([('draft', 'Drift'),('confirm', 'Confirm'),('waiting_approve', ' Waiting Approval'),('approve', 'Approval'), ('done', 'Done')], 'Status', default='draft')
    year = fields.Char('Study Year', default=lambda self: datetime.datetime.now().year)
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

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















