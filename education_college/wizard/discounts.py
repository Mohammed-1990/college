from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateDiscounts(models.TransientModel):
    _name = 'student.discounts.wizard'
    _description = "Create User for selected Student(s)"

    student_id = fields.Many2one(
        'student.registrar', string='Student Name')
    college_id = fields.Many2one("college.college", ondelete="cascade", string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    level_id = fields.Many2one("level.level", ondelete="cascade", string="Level")
    semester_id = fields.Many2one("semester.semester", ondelete="cascade", string="Semester")
    discount_type = fields.Selection([
        ('0', 'Select Discount Type'),
        ('1', 'Percentage'),
        ('2', 'amount'), ], string="Discount Type" ,default='0')
    form_number = fields.Char(straing='University ID')
    register_fees = fields.Float(straing='Register Fees')
    program_fees  = fields.Float(straing='Study Fees')
    acceptance_type = fields.Selection(
        [('general', 'General acceptance'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'),
         ('tow_vacancy', 'Vacancy Tow'), ('scholarship', 'Scholarship')],string="Acceptance Type")
    after_discount= fields.Float(string=" The Fees After Discount",comput="_comput_discount", store=True)
    discount_prcentage = fields.Selection([
        ('10', '10%'),
        ('20', '20%'),
        ('30', '30%'),
        ('40', '40%'),
    ], string="Discount Prcentage")

    @api.onchange('student_id')
    def _get_studen_information(self):
        self.college_id= self.student_id.college_id.id
        self.program_id= self.student_id.program_id.id
        self.batch_id= self.student_id.batch_id.id
        self.level_id= self.student_id.level_id.id
        self.semester_id= self.student_id.semester_id.id
        self.acceptance_type= self.student_id.type_acceptance
        if self.student_id.after_discount > 0.00:
            self.program_fees= self.student_id.after_discount

        else:
            self.program_fees= self.student_id.study_fees

    @api.onchange('discount_prcentage')
    def _comput_discount(self):

        # if int(self.student_id.discount_fees) > 0:
        #     raise UserError(('Student Discount Has Already Been Made'))
        if self.student_id.type_acceptance == "scholarship":
            raise UserError(('This Type Of Acceptance Has No Discount'))
        if self.discount_prcentage:
            if self.student_id.after_discount <= 0.00:
                self.after_discount = self.program_fees - (self.program_fees * (int(self.discount_prcentage) / 100))
            else:
                self.after_discount = self.student_id.remaining_fee-(self.student_id.remaining_fee*(int(self.discount_prcentage) / 100))

    def Create_student_discounts(self):
        record = self.env['student.registrar'].browse(self.student_id.id)
        record.update({
            'after_discount': self.after_discount,
        })

