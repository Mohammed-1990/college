import datetime
from odoo import models, fields, api, exceptions,_


class Mouth(models.Model):
    _name = 'clinic.mouth'
    _description = 'Mouth'
    _order = "id desc"


    image_1920 = fields.Binary('image_1920')
    patient_id = fields.Char(string='Student Number')
    name = fields.Char(string="Student Name")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('approval', 'Approvaled'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    gender = fields.Char(string="gender")
    birth_date = fields.Date(string='Date Of Birth')
    age = fields.Integer(string='Age')
    date = fields.Char(string='Date', default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'),readonly=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    home = fields.Char(string="Home")
    nationality = fields.Char(string='Nationality')
    religion = fields.Char(string='Religion')
    program = fields.Char(string='Program')
    general = fields.Char(string="General Vision")
    withoutglss = fields.Char(string="With Out Glasses")
    withglasses = fields.Char(string='With  Glasses')
    color = fields.Char(string='Color Vision')
    near = fields.Char(string='Near Vision')
    normal = fields.Boolean(string='1.Normal')
    decayed = fields.Boolean(string='2.Decayed')
    missing = fields.Char(string='Missing')
    filled = fields.Char(string='Filled')
    othera = fields.Char(string='Other Abnormality')
    tongue = fields.Char(string='Tongue')
    assessment = fields.Text(string="Assessment")
    diagonis = fields.Text(string='Diagonis')
    is_assessment = fields.Boolean(string="Is assessment")
    dentist = fields.Char(string='Dentist', default=lambda self: self.env.user.name,readonly=True)




    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)

            self.dentist = self.env.user.name



    def confirm_test_result(self):
        self.state = 'confirm'

    def approval_test_result(self):
        self.state = 'approval'
    
    def done_test_result(self):
        resulit = self.env['clinic.physical'].search([('patient_id','=',self.patient_id)])
        if resulit:
            resulit.update({'mouth_resulit':True})
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete Which is not Draft or Cancelled.'))
        return super(Mouth, self).unlink()





