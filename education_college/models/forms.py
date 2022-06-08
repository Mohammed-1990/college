
from odoo import models, fields, api,_
import datetime
import re

from odoo.exceptions import UserError

# Health Request

class HealthInsurance(models.Model):
    _inherit = ['mail.thread']
    _rec_name ='student_ids'
    _name = 'form.health'
    _description = 'add health insurance'

    student_ids = fields.Many2one('student.registrar', string='Student Name')
    birth_date = fields.Date(string="Date of Birth", ondelete="cascade", related='student_ids.birth_date')
    date = fields.Char(string="Date",default=lambda self: fields.Date.today())
    id_document = fields.Selection(string="Identification Card", ondelete="cascade", related='student_ids.type_of_id')
    the_number = fields.Char(string="The  Number", ondelete="cascade", related='student_ids.id_number')
    form_number = fields.Char(ondelete="cascade", related='student_ids.form_number')
    place_of_issue = fields.Char(string="Place Of Issue")
    social_status =  fields.Selection(string="Social State", ondelete="cascade", related='student_ids.social_status')
    educational_level = fields.Selection([
        ('secondary', 'Secondary'),
        ('university', ' University'),
        ('other', 'Other')],
        string="Educational Level")
    local = fields.Char(string="Local", ondelete="cascade", related='student_ids.local')
    unit = fields.Char(string="Administrative unit")
    neighborhood = fields.Char(string="Neighborhood ")
    home_number = fields.Char(string="Home Number ")
    the_phone = fields.Char(string="Phone Number",ondelete="cascade", related='student_ids.student_mobile')
    e_mail = fields.Char(string="E-mail ", ondelete="cascade", related='student_ids.email')
    mother_name = fields.Char(string="Mother's Name ")
    place_of_birth = fields.Char(string="Place Of Birth ")
    chronic_diseases = fields.Text(string="Chronic Diseases ")
    health_center = fields.Char(string="Health Center ")
    hospital = fields.Char(string="Hospital ")


    # The Resignation request

    class RequestResignation(models.Model):
        _inherit = ['mail.thread']
        _name = 'form.resignation'
        _description = 'resignation information'
        _order = " id desc"
        _rec_name = "student_ids"
        student_ids = fields.Many2one('student.registrar', string='Student Name')
        college = fields.Many2one('college.college', ondelete="cascade", related='student_ids.college_id',
                                  string="College")
        program = fields.Many2one("program.program", ondelete="cascade", related='student_ids.program_id',
                                  string="Program")
        form_number = fields.Char(string='Sitting Number', ondelete="cascade", related='student_ids.form_number')
        st_phone = fields.Char(string=" Phone Number one", ondelete="cascade", related='student_ids.student_mobile')
        st_moble = fields.Char(string="Phone Number two", ondelete="cascade", related='student_ids.whatsapp_phone')
        date_admission = fields.Date(string='College admission date')
        exam_location = fields.Char(string='Exam location')
        reasons = fields.Char(string='Reasons for submitting resignation')

        reasons_resignation = fields.Char(string='Reasons for submitting resignation')

        data = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        user_name = fields.Char(string="System User ", default=lambda self: self.env.user.name)

        registrar_name = fields.Char(string="Registrant Name ", readonly=True, default=lambda self: self.env.user.name)
        registrar_date = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        registrar_signature = fields.Char(string="Registrant signature")

        coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
                                       default=lambda self: self.env.user.name)
        coordinator_date = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        coordinator_recommend = fields.Text(string="Coordinator Recommendation ")
        academic_position = fields.Char(string="Academic Position")
        Coordinator_signature = fields.Char(string="Coordinator signature")

        agent_name = fields.Char(string="Agent Name", readonly=True,)
        agent_date = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        agent_signature = fields.Char(string="Agent signature")

        scientific_recommend = fields.Text(string="Recommendation of the Secretary of Scientific Affairs ")
        scientific_name = fields.Char(string="Scientific Name", readonly=True,)
        scientific_date = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        scientific_signature = fields.Char(string="Scientific signature")

        accreditation_date = fields.Date(string="Date", required=False, readonly=True, default=lambda self: fields.date.today())
        accreditation_signature = fields.Char(string="Accreditation signature")

        # form Request
    class HealthInsurance(models.Model):
            _inherit = ['mail.thread']
            _rec_name = 'student_ids'
            _name = 'form.request'
            _description = 'add health insurance'

            student_ids = fields.Many2one('student.registrar', string='Student Name')
            date = fields.Char(string="Date", default=lambda self: fields.Date.today())
            form_number = fields.Char(string="Student Number", ondelete="cascade", related='student_ids.form_number')
            level_id = fields.Many2one("level.level", ondelete="cascade", string="Level", related='student_ids.level_id')

            program = fields.Many2one("program.program", ondelete="cascade", related='student_ids.program_id',
                                      string="Program")

            coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
                                           default=lambda self: self.env.user.name)
            coordinator_date = fields.Date(string="Date", required=False, readonly=True,
                                           default=lambda self: fields.date.today())
            Coordinator_signature = fields.Char(string="Coordinator signature")

            #
            # coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
            #                                default=lambda self: self.env.user.name)
            # coordinator_date = fields.Date(string="Date", required=False, readonly=True,
            #                                default=lambda self: fields.date.today())
            # Coordinator_signature = fields.Char(string="Coordinator signature")
            #
            # coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
            #                                default=lambda self: self.env.user.name)
            # coordinator_date = fields.Date(string="Date", required=False, readonly=True,
            #                                default=lambda self: fields.date.today())
            # Coordinator_signature = fields.Char(string="Coordinator signature")
            #
            # coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
            #                                default=lambda self: self.env.user.name)
            # coordinator_date = fields.Date(string="Date", required=False, readonly=True,
            #                                default=lambda self: fields.date.today())
            # Coordinator_signature = fields.Char(string="Coordinator signature")
            #
            # coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
            #                                default=lambda self: self.env.user.name)
            # coordinator_date = fields.Date(string="Date", required=False, readonly=True,
            #                                default=lambda self: fields.date.today())
            # Coordinator_signature = fields.Char(string="Coordinator signature")
            #
            # coordinator_name = fields.Char(string="Coordinator Name ", readonly=True,
            #                                default=lambda self: self.env.user.name)
            # coordinator_date = fields.Date(string="Date", required=False, readonly=True,
            #                                default=lambda self: fields.date.today())
            # Coordinator_signature = fields.Char(string="Coordinator signature")
            #
            #







