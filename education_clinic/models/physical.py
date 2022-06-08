import datetime
from odoo import models, fields, api, exceptions,_


class Physical(models.Model):
    _name = 'clinic.physical'
    _description = 'physical'
    _order = "id desc"


    image_1920 = fields.Binary('image_1920')
    patient_id = fields.Char(string='Student Number')
    student_ids = fields.Char(string="student_ids")
    name = fields.Char(string="Student Name")
    gender = fields.Char(string="Gender")
    birth_date = fields.Date(string='Date Of Birth')
    age = fields.Integer(string='Age')
    date = fields.Char(string='Date', default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'),  readonly=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    nationality = fields.Char(string='Nationality')
    religion = fields.Char(string='Religion')
    program = fields.Char(string='Program')
    home = fields.Char(string="Address")
    general = fields.Char(string='General')
    appearance = fields.Char(string='Appearance')
    constitution = fields.Char(string='Constitution')
    normal = fields.Char(string="Normal")
    abnormal = fields.Char(string="Abnormality")
    normal_one = fields.Char(string='Normal')
    enlarge = fields.Char(string='Enlarged')
    normal_two = fields.Char(string='Normal')
    external = fields.Char(string='Otitis External') 
    media = fields.Char(string='Otitis Media')
    hearing = fields.Char(string='Hearing') 
    nose = fields.Char(string='Nose')
    general_one = fields.Char(string='General')
    clear = fields.Char(string='Clear')
    abnormality = fields.Char(string='Abnormality') 
    normal_th = fields.Char(string='Normal')
    abnormal_th = fields.Char(string='Abnormality') 
    general_fo = fields.Char(string='General') 
    normal_fo = fields.Char(string='Normal')
    paipable = fields.Char(string='Paipable Finger b.c.m')
    normal_no = fields.Char(string='Normal')
    paip = fields.Char(string='Paipable Finger')
    other = fields.Char(string='Other Massas') 
    fluid = fields.Char(string='Fluid')
    hernia = fields.Char(string='Hernia')
    genitalia = fields.Char(string='Genitalia')
    lower = fields.Char(string='Lower Limbs')
    intell = fields.Char(string='Intelligence')
    speech = fields.Char(string='Speech')
    fungi = fields.Char(string='Fungi') 
    cranial = fields.Char(string='Cranial Nerves')
    motor = fields.Char(string='Motor System')
    sensory = fields.Char(string='Sensory System')
    reflexes = fields.Char(string='Reflexes')
    skin = fields.Char(string='Skin')
    comment = fields.Char(string='Comment On Examination')
    upper = fields.Char(string='Upper Limps')
    thyroid = fields.Char(string='Thyroid')
    central = fields.Char(string='Central')
    deviated = fields.Char(string='Deviated to Rt/Left')
    result_data = fields.Date(string="Result Data")
    diagonis = fields.Text(string='Diagonis')
    doctor_name = fields.Char(string='Doctor name',default=lambda self: self.env.user.name,readonly=True)
    result = fields.Selection([
        ('fit', 'Medically fit'),
        ('unfit', 'Medically Unfit'),
        ('other', 'Others '),
    ], string="Result")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('approval', 'Approvaled'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    nursing_resulit = fields.Boolean(default=False ,string="Nursing")
    optical_resulit =fields.Boolean(default=False,string="Optical")
    mouth_resulit = fields.Boolean(default=False,string="Mouth")
    laboratory_resulit = fields.Boolean(default=False,string="Laboratory")
    psychological_resulit =fields.Boolean(default=False,string="Psychological")
    userid = fields.Char("User ID", default=lambda self: self.env.user.name,readonly=True)

    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)

    def confirm_test_result(self):
        self.state = 'confirm'

    def approval_test_result(self):
        self.state = 'approval'
    
    def done_test_result(self):
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete Which is not Draft or Cancelled.'))
        return super(Physical, self).unlink()



    

    def get_nursing_medical_examination(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Medical Examination",
            'view_mode': 'tree,form',
            'res_model': 'clinic.nursing',
            'domain': [('patient_id', '=', self.patient_id),('state','=','done')],
            }
    def get_eye_medical_examination(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Medical Examination",
            'view_mode': 'tree,form',
            'res_model': 'clinic.eye',
            'domain': [('patient_id', '=', self.patient_id),('state','=','done')],
            }
    def get_mouth_medical_examination(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Medical Examination",
            'view_mode': 'tree,form',
            'res_model': 'clinic.mouth',
            'domain': [('patient_id', '=', self.patient_id),('state','=','done')],
            }
    def get_laboratory_medical_examination(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': "Medical Examination",
            'view_mode': 'tree,form',
            'res_model': 'clinic.laboratory',
            'domain': [('patient_id', '=', self.patient_id),('state','=','done')],
            }
    def get_psychological_medical_examination(self):

        self.ensure_one()
        return {
        'type': 'ir.actions.act_window',
        'name': "Medical Examination",
        'view_mode': 'tree,form',
        'res_model': 'clinic.psychological',
        'domain': [('patient_id', '=', self.patient_id),('state','=','done')],
        }


