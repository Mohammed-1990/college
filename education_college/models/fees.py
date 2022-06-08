from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
import datetime


class StudyFees(models.Model):
    _inherit = ['mail.thread']
    _name = 'study.fees'
    _rec_name = 'program_id'
    _description = 'add fees information'

    college_id = fields.Many2one('college.college', ondelete='cascade', string="Collage",
                                 default=lambda self: self.env['college.college'].search([]))
    program_id = fields.Many2one("program.program", ondelete="cascade", string="Program")
    sudaness_study = fields.Integer(string="Sudanes Study")
    foreigners_study = fields.Integer(string=" Foreig Study")
    sdn_register_fees = fields.Integer(string=" Sudanes Register")
    foriegn_register_fees = fields.Integer(string=" Foreig Register")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'done')], string='Status',
                             default="draft")
    study_year = fields.Char('Study Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(datetime.datetime.now().year))
    company_id = fields.Many2one('res.company', string='Company')
    year = fields.Char('Study Year', default=lambda self: datetime.datetime.now().year)
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    @api.onchange('program_id')
    def get_company(self):
        for rec in self:
            rec.company_id = rec.program_id.company_id.id
    @api.constrains('sudaness_study')
    def validate_fees(self):
        if self.sudaness_study <= 0 or self.sdn_register_fees <= 0 or self.foreigners_study <= 0 or self.foriegn_register_fees <= 0:
            raise UserError(_('The Value Of Fees Must Be Gred Than zero'))

    @api.model
    def create(self, vals):
        chack_data = self.env['study.fees'].search(
            [('college_id', '=', vals['college_id']), ('program_id', '=', vals['program_id']), ('year', '=', vals['year'])])
        if chack_data :
            raise UserError(_('The Fees Have Been Previously Entered. Cannot Be Entered More Than Once Ber Year'))
        else:
            ret =super(StudyFees, self).create(vals)
            return ret

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete The Fees  Which  State Is Not Draft or Cancelled.'))
        return super(StudyFees, self).unlink()


class ManagementFees(models.Model):
    _inherit = ['mail.thread']
    _name = 'revenue.revenue'
    _description = 'add revenue fees'
    _rec_name = "revenue_type_id"

    revenue_type_id = fields.Many2one('other.revenue', string="Fees Type ", ondelete='cascade')
    for_sudanes = fields.Integer(string="Sudanes ", required=True)
    for_foreig = fields.Integer(string="Foreign ", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'done')], string='Status',
                             default="draft")
    year = fields.Char('Year', default=lambda self: datetime.datetime.now().year)
    study_year = fields.Char('Study Year', default=lambda self: str(datetime.datetime.now().year - 1) + " - " + str(
        datetime.datetime.now().year))
    company_id = fields.Many2one('res.company', string='Company')
    user_id = fields.Many2one('res.users', 'Creant User ', default=lambda self: self.env.user)

    @api.constrains('revenue_type_id')
    def validate_revenue_fees(self):
        if self.for_sudanes <= 0 or self.for_foreig <= 0:
            raise UserError(_('The Value Of Fees Must Be Gred Than zero'))

    @api.model
    def create(self, vals):
        chack_data = self.env['revenue.revenue'].search([('revenue_type_id', '=', vals['revenue_type_id']),('year', '=', vals['year'])])
        if chack_data:
            raise UserError(_('The Fees Have Been Previously Entered. Cannot Be Entered More Than Once Ber Year'))
        else:
            ret = super(ManagementFees, self).create(vals)
            return ret

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    ('You Cannot Delete The Fees  Which  State Is Not Draft or Cancelled.'))
        return super(ManagementFees, self).unlink()


