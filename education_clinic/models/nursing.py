import datetime
from odoo import models, fields, api, exceptions,_



class NursingLap(models.Model):
    _name = 'clinic.nursing'
    _description = 'Nursing'
    _order = "id desc"


    image_1920 = fields.Binary('image_1920')
    patient_id = fields.Char(string='Student Number', )
    name = fields.Char(string="Student Name")
    gender = fields.Char(string="gender", )
    birth_date = fields.Date(string='Date Of Birth', )
    age = fields.Integer(string='Age')
    date = fields.Char(string='Date', default=lambda self: datetime.datetime.today().strftime('%Y-%m-%d'), readonly=True)
    phone = fields.Char(string="Phone", )
    email = fields.Char(string="Email", )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('approval', 'Approvaled'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    nationality = fields.Char(string="Nationality", )
    religion = fields.Char(string='Religion', )
    program = fields.Char(string='Program', )
    hom = fields.Char(string="Address", )
    elementary = fields.Char(string="Elementary")
    inter = fields.Char(string="Intermediate")
    intermediate = fields.Char(string='Intermediate')
    secondary = fields.Char(string='Secondary')
    home = fields.Char(string='Home')
    University = fields.Char(string="University fee ls")
    bursary = fields.Char(string='Bursary ls')
    height = fields.Char(string='Height')
    weight = fields.Char(string='Weight')
    pulse = fields.Char(string="Pulse")
    bp = fields.Char(string='B.P')
    tube = fields.Boolean('Tuberculosis')
    chronic = fields.Boolean('Chronic Cough')
    diabetes = fields.Boolean('Diabetes Mellitus')
    hypertension = fields.Boolean('Hypertension')
    heart = fields.Boolean('HeartDisease')
    typhoid = fields.Boolean('typhoid')
    dysentery = fields.Boolean('Dysentery')
    asthma = fields.Boolean('Asthma')
    syphlls = fields.Boolean('Syphllls')
    hay2 = fields.Boolean('Hay Fever')
    eczema2 = fields.Boolean('Eczema')
    skin = fields.Boolean('Other Skin Disease')
    pept = fields.Boolean('Peptic Ulcer')
    migrain = fields.Boolean('Megraine')
    epile = fields.Boolean('Epilepsy')
    nervous = fields.Boolean('Nervous Trouble')
    illness = fields.Boolean('Other Illness')
    hepatit = fields.Boolean('Hepatitis')
    malaria = fields.Boolean('Malaria')
    infective2 = fields.Boolean('Infective Hepatitis')
    sore = fields.Boolean('Sore throat')
    chest = fields.Boolean('Chest Trouble')
    eczema = fields.Boolean('Eczema')
    hay = fields.Boolean('Hay Feve')
    none = fields.Boolean('None')
    trans = fields.Boolean('Blood Transfusion')
    bilharz = fields.Boolean('Bilharzias')
    cough = fields.Boolean('Whooping Cough')
    mumps = fields.Boolean('Mumps')
    tuber = fields.Boolean('Tuberculosis')
    trouble = fields.Boolean('Heart Trouble')
    rheumatism = fields.Boolean('Rheumatism')
    pain = fields.Boolean('Chronic Abdominal Pain')
    peptic_ulcer = fields.Boolean('Peptic Ulcer')
    worms = fields.Boolean('Intestinal Worms')
    dysant = fields.Boolean('Dysantery')
    onchocer = fields.Boolean('Onchocerciasis')
    sensitiv = fields.Boolean('sensitivity to any drug')
    breakdown = fields.Boolean('Nervous Breakdown')
    exams = fields.Boolean('Nervous trouble with exams')
    dysam = fields.Boolean('Dysamenmhoea')
    tonsillectomy = fields.Boolean('Tonsillectomy')
    appendisectomy = fields.Boolean('Appendisectomy')
    peptic = fields.Boolean('Peptic')
    accidents = fields.Boolean('Accidentse')
    other = fields.Date('Other')
    small = fields.Date('Small Box')
    yellow = fields.Date('Yellow Fever')
    bcg = fields.Date('B.C.G')
    typhoid1 = fields.Date('Typhoid')
    infective = fields.Date('Infective Hepatitis')
    other2 = fields.Boolean('Others')
    alive = fields.Boolean('IS HE ALIVE?')
    dead = fields.Boolean('Dead')
    age = fields.Char('Your age when he died')
    occupation = fields.Char('job')
    education = fields.Char('Educational Level')
    alive2 = fields.Boolean('IS HE ALIVE?')
    dead2 = fields.Boolean('Dead')
    age2 = fields.Integer('Your age when he died')
    divorced2 = fields.Char('divorced')
    education2 = fields.Char('Educational Level')
    parents = fields.Boolean('Both Parents')
    father = fields.Boolean(' With Father')
    mother = fields.Boolean('With Mother')
    relative = fields.Boolean('With Relative')
    sibling = fields.Char('Number of Sibling')
    place = fields.Char('Your Arrangement in The Family')
    alcohol = fields.Boolean('Do You Use Alcohol')
    tobacco = fields.Boolean('Do You Use Tobacco')
    snuff = fields.Boolean('Do You Use Snuff')
    hashish = fields.Boolean('Do You Use Hashish')
    otherh = fields.Boolean('Other Habits')
    type2 = fields.Char('What Types')
    social = fields.Char('Social Activity')
    hobby = fields.Char('Others Hobbies')
    attitu = fields.Char('Attitude To Religion')
    assessment = fields.Text(string="Assessment")
    diagonis = fields.Text(string='Diagonis')
    nursing = fields.Char(string='Name of doctor',  default=lambda self: self.env.user.name,readonly=True)

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
            resulit.update({'nursing_resulit':True})
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete Which is not Draft or Cancelled.'))
        return super(NursingLap, self).unlink()










    
