import datetime
import re
from num2words import num2words
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EducationAccounting(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _rec_name = "student_id"
    _name = 'education.accounting'
    _description = 'information accounting'

    student_id = fields.Many2one('student.registrar', string='Name')
    college_id = fields.Many2one("college.college", ondelete="cascade",string="College")
    program_id = fields.Many2one("program.program", ondelete="cascade",string="Program")
    level_id = fields.Many2one('level.level', string='Level',ondelete='cascade')
    semester_id = fields.Many2one('semester.semester', string='Semester', ondelete='cascade')
    form_number = fields.Char(string='University ID')
    money_type = fields.Selection([('cash', 'Cash'),('bank', 'Bank'),], string='Method Of Payment')
    currency_type = fields.Selection([('usd', 'Dollar'), ('sd', 'Sudanese Bound')], string="Currency Type")
    the_fees = fields.Float(string="Fees")
    receipt_code = fields.Char(string="Receipt Number", copy=False, readonly=True, index=True, default=lambda self: _('New'))
    the_amount = fields.Char(string="The Amount" , compute="_compute_amount" , store=True)
    about = fields.Char(string="About")
    year = fields.Date(string='Date ',default=fields.Date.today())
    presentation = fields.Boolean(string='yes ', default=False )
    register_office = fields.Boolean(string='register Office ', default=False )
    admission_ids = fields.Char(string="Accountant Name")
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'), ('done', 'done')], string='Status', default="draft", readonly=True)
    register_office = fields.Boolean(string='register Office ', default=False )
    type_of_fees = fields.Selection([('stady','Stady'),('management','Management')])
    is_managemanent = fields.Boolean(string=" Type Of Fees")

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete The Fees  Which  State Is Not Draft or Cancelled.'))
        return super(EducationAccounting, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('receipt_code', _('New')) == _('New'):
            vals['receipt_code'] = self.env['ir.sequence'].next_by_code('education_accounting.account_code.sequence') or _(
                'New')
            return super(EducationAccounting, self).create(vals)

    @api.depends('the_amount')
    def _compute_amount(self):
        self.the_amount = num2words(self.the_fees, lang='ar')

    def action_done(self):
        remaining_fee =0.0
        self.state = "done"
        if self.type_of_fees == "stady":
            obj = self.env['student.registrar'].search([('id','=',self.student_id.id)])
            if obj.student_state =='not_registered':
                remaining_fee = obj.remaining_fee - (self.the_fees - obj.register_fees)
                installment ='first'
                student_state="first_semester"
            else:
                remaining_fee =obj.remaining_fee - self.the_fees
                installment ='first_semester'
                student_state="first_semester"


            obj.update({
                'remaining_fee':remaining_fee,
                # 'installment':installment,
                'student_state':student_state

            })

    def print_account_report(self):
        return self.env.ref('education_accounting.report_session').report_action(self)




