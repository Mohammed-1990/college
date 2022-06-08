import datetime

from odoo import models, fields, api, exceptions,_


class Laboratory(models.Model):
    _name = 'clinic.laboratory'
    _description = 'laboratory'
    _order = "id desc"


    image_1920 = fields.Binary('image_1920')
    patient_id = fields.Char(string='Student Number')
    name = fields.Char(string="Student Name")
    gender = fields.Char(string="gender")
    birth_date = fields.Date(string='Date Of Birth')
    age = fields.Integer(string='Age')
    date = fields.Char(string='Date', default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'),readonly=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('approval', 'Approvaled'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    nationality = fields.Char(string='Nationality')
    religion = fields.Char(string='Religion')
    program = fields.Char(string='Program')
    home = fields.Char(string="Address")
    color = fields.Char(string="Color")
    reaction = fields.Char(string="Reaction")
    glucose = fields.Char(string='Glucose')
    protein = fields.Char(string='Protein')
    ketones = fields.Char(string='Ketones')
    pus = fields.Char(string="Pus Cells")
    rbs = fields.Char(string="R.B.Cs")
    epithel = fields.Char(string='Epithelial Cells')
    casts = fields.Char(string='Casts')
    crystals = fields.Char(string='Crystals')
    other = fields.Char(string='Others')
    hbv = fields.Char(string='HBV')
    hcv = fields.Char(string='HCV')
    hiv = fields.Char(string='HIV')
    hb = fields.Char(string='HB')
    ho = fields.Char(string='%')
    Blood_g = fields.Char(string='Blood Group')
    investig = fields.Char(string='Other Investigations')
    addiction = fields.Char(string='Drug Addiction')
    recommend = fields.Char(string='Recommendations')
    date_two = fields.Date(string='Date')
    physician = fields.Char(string='PHYSICIAN')
    signature = fields.Char(string='Signature')
    assessment = fields.Text(string="Assessment")
    diagonis = fields.Text(string='Diagonis')
    name_of = fields.Char(string='Name Of Examining doctor', readonly=True, default=lambda self: self.env.user.name)


    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)

            self.name_of = self.env.user.name

    def confirm_test_result(self):
        self.state = 'confirm'

    def approval_test_result(self):
        self.state = 'approval'
    
    def done_test_result(self):
        resulit = self.env['clinic.physical'].search([('patient_id','=',self.patient_id)])
        if resulit:
            resulit.update({'laboratory_resulit':True})
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete Which is not Draft or Cancelled.'))
        return super(Laboratory, self).unlink()






