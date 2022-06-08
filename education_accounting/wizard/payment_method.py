# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MethodInvoice(models.TransientModel):
    _name = "payment.method"
    _rec_name = "money_type"
    _description = "Membership Invoice"
    student_id = fields.Many2one(
        'education.accounting', string='Student Name')
    money_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank '),
    ], string='Journal')
    amount = fields.Char(string=" Amount")
    currency_type = fields.Selection([('usd', 'Dollar'), ('sd', 'Sudanese Bound')], string="Currency Type")
    safe_id = fields.Many2one('safe.safe', string='Name of Cash', ondelete='cascade')
    bank_id = fields.Many2one("bank.bank", ondelete="cascade", string="Name of Bank")
    check_num = fields.Char(string="Check Number")
    about = fields.Char(string="About")


    @api.onchange('student_id')
    def amount_info(self):
        for rec in self:
            rec.amount = rec.student_id.the_fees
            rec.currency_type = rec.student_id.currency_type
            rec.about = rec.student_id.about


    # action for print account wizard report
    def create_accounting_wizard_report(self):
        result = self.env['education.accounting'].browse(self.student_id.ids)
        result.update(
             {
                 'money_type': self.money_type,
                  'state': 'confirm',
                  'admission_ids': self.env.user.name

             }
        )
