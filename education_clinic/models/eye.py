import datetime
from odoo import models, fields, api, exceptions,_


class Eyeclinic(models.Model):
    _name = 'clinic.eye'
    _description = 'Eye'
    _order = "id desc"

    image_1920 = fields.Binary('image_1920')
    patient_id = fields.Char(string='Student Number' )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('approval', 'Approvaled'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    name = fields.Char(string="Student Name")
    gender = fields.Char(string="gender" )
    birth_date = fields.Date(string='Date Of Birth' )
    date = fields.Char(string='Date', default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'),  readonly=True)
    phone = fields.Char(string="Phone" )
    email = fields.Char(string="Email" )
    nationality = fields.Char(string='Nationality' )
    religion = fields.Char(string='Religion' )
    program = fields.Char(string='Program' )
    home = fields.Char(string="address")
    
    general = fields.Char(string="General Vision")
    withoutglss = fields.Char(string="With Out Glasses")
    withglasses = fields.Char(string='With  Glasses')
    color = fields.Char(string='Color Vision')
    near = fields.Char(string='Near Vision')
    opthahmologist = fields.Char(string='Opthahmologist', readonly=True, default=lambda self: self.env.user.name )
    assessment = fields.Text(string="Assessment")
    diagonis = fields.Text(string='Diagonis')
    is_assessment = fields.Boolean(string="Is assessment")

    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)
    
    def confirm_test_result(self):
        self.state = 'confirm'

    def approval_test_result(self):
        self.state = 'approval'
    
    def done_test_result(self):
        resulit = self.env['clinic.physical'].search([('patient_id','=',self.patient_id)])
        if resulit:
            resulit.update({'optical_resulit':True})
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete Which is not Draft or Cancelled.'))
        return super(Eyeclinic, self).unlink()


 






