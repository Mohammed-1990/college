from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
import re
from datetime import datetime


class EducationSafe(models.Model):
    _inherit = ['mail.thread']
    _name = 'safe.safe'
    _description = 'add cash  Name'

    name = fields.Char(string="Cash Name", help="enter Name of Safe")

    # @api.constrains('name')
    # def validate_college_name(self):
    #     if self.name:
    #         if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
    #             raise UserError(_('The Value Of College Name Must Be Only Letters'))

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Name Of Cash Must Be Unique"),
    ]

    class EducationBank(models.Model):
        _inherit = ['mail.thread']
        _name = 'bank.bank'
        _description = 'add bank Name'

        name = fields.Char(string="Name of Bank",  help="enter Name of bank")

        @api.constrains('name')
        def validate_level_name(self):
            if self.name:
                if not re.search(r'^(?:[^\W\d_]| )+$', self.name) != None:
                    raise UserError(_('Name of Bank  Must Be Only Letters'))

        _sql_constraints = [
            ('name_unique',
             'UNIQUE(name)',
             "Name of Bank Must Be Unique"),
        ]



