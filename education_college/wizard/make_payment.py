import datetime
from num2words import num2words
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreatePayment(models.TransientModel):
    _name = 'create.payment'
    _description = "Create Make a payment"

    student_id = fields.Many2one('student.registrar', string='Student Name', )
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Brogram")
    college_id = fields.Many2one('college.college', string='College', ondelete='cascade')
    level_id = fields.Many2one('level.level', string='Level', ondelete='cascade' )
    semester_id = fields.Many2one('semester.semester', string='Semester', ondelete='cascade')
    batch_id = fields.Many2one("batch.batch", ondelete="cascade", string="Batch")
    acceptance_type = fields.Selection([('general', 'General acceptance'), ('special', 'Special'), ('expats', 'Expats'), ('one_vacancy', 'Vacancy one'), ('tow_vacancy', 'Vacancy Tow'),('scholarship', 'Scholarship')], string="Acceptance Type")
    currency_type = fields.Selection([('usd', 'Dollar'), ('sd', 'Sudanese Bound')], string="Currency Type")
    revenue_id = fields.Many2one("revenue.revenue", ondelete="cascade", string="Other Revenue")
    register_fees = fields.Float(string="Register  Fees")
    type_of_fees = fields.Selection([('stady','Stady'),('management','Management')])
    installment = fields.Selection([('one', '100%'), ('two', '50%'), ], string="Installment")
    remaining_fee = fields.Float(string="Total Received Fees")
    paying = fields.Float(string="paying off")
    other_fees = fields.Float(string="Other Revenue ")
    about = fields.Char(string="about")


    @api.onchange('student_id')
    def create_appointment(self):
        student_id = self.env['student.registrar'].search([('id', '=', self.student_id.id)])
        if student_id:
            self.program_id = student_id.program_id.id
            self.college_id = student_id.college_id.id
            self.level_id = student_id.level_id.id
            self.semester_id = student_id.semester_id.id
            self.batch_id = student_id.batch_id.id
            self.acceptance_type = student_id.type_acceptance
            self.register_fees = student_id.register_fees
            self.remaining_fee = student_id.remaining_fee
            if self.acceptance_type == 'expats':
                self.currency_type = 'usd'
            else:
                self.currency_type = 'sd'

    @api.onchange('installment')
    def create_installment(self):
        self.other_fees = 0.0
        self.about = " "
        self.type_of_fees = "stady"
        if self.installment:
            if self.installment == 'one':
                if self.student_id.student_state == 'not_registered':
                    self.paying = self.remaining_fee + self.register_fees
                    self.about = "رسوم تسجيل + رسوم دراسية "
                else:
                    self.paying = self.remaining_fee
                    self.about = "رسوم دراسية "
            elif self.installment == 'two':
                if self.student_id.student_state == 'not_registered':
                    self.paying = self.register_fees +(self.remaining_fee / 2)
                    self.about = "رسوم تسجيل + رسوم دراسية "
                else:
                    self.paying = self.remaining_fee / 2
                    self.about = "رسوم دراسية "

    @api.onchange('revenue_id')
    def create_other_revenue(self):
        revenue = self.env['revenue.revenue'].search([('id', '=', self.revenue_id.id)])
        self.paying = 0.0
        self.about = " "
        self.type_of_fees = "management"
        if self.revenue_id:
            if self.acceptance_type:
                if self.acceptance_type == 'expats':
                    self.other_fees = revenue.for_foreig
                    self.about = revenue.revenue_type_id.name
                    self.currency_type = 'usd'
                else:
                    self.other_fees = revenue.for_sudanes
                    self.about = revenue.revenue_type_id.name
                    self.currency_type = 'sd'

    def create_payment(self):
        the_fees = 0.0
        if self.paying > 1:
            the_fees = self.paying
        elif self.other_fees > 1:
            the_fees = self.other_fees
        if self.acceptance_type == 'expats':
            currency_type = 'usd'
            self.currency_type = 'usd'
        else:
            self.currency_type = 'sd'
            currency_type = 'sd'

        if the_fees <= 0.0:
            raise UserError(('The value of the fees paid must be greater than zero'))

        self.env['education.accounting'].create({
            'student_id': self.student_id.id,
            'program_id': self.program_id.id,
            'level_id': self.level_id.id,
            'semester_id': self.semester_id.id,
            'the_fees': the_fees,
            'type_of_fees': self.type_of_fees,
            'currency_type': currency_type,
            'about': self.about,

        })

