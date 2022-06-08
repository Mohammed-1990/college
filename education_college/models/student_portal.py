# -*- coding: utf-8 -*-
from odoo import models, fields


class StudentPortal(models.Model):
    _inherit = 'res.partner'

    form_numper = fields.Char("Form Number")
    is_student = fields.Boolean("Is a Student")
