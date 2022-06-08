# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime

# New Student Information
class ReportStudentEducation(models.AbstractModel):
    _name = 'new.student.report'
    _description = 'education Report'


    @api.model

    def _get_report_values(self, docids):

        docs = self.env['new.student'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'new.student',
                'docs': docs,

            }



# Old Student Information

class ReportEducationStudent(models.AbstractModel):
    _name = 'old.student.report'
    _description = 'education Report'


    @api.model

    def _get_presentation_report(self, docids):

        docs = self.env['old.student'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'old.student',
                'docs': docs,

            }

    # Register   Information

    class ReportRegisterOffice(models.AbstractModel):
        _name = 'student.registrar.report'
        _description = 'office Report'

        @api.model
        def _get_register_office_report(self, docids):
            docs = self.env['student.registrar'].browse(docids)

            return {
                'doc_ids': docs.ids,
                'doc_model': 'student.registrar',
                'docs': docs,
            }

    class ReportRegisterform(models.AbstractModel):
        _name = 'request.form.report'
        _description = 'forms Report'

        @api.model
        def _get_report_form_resignation(self, docids):
            docs = self.env['form.resignation'].browse(docids)

            return {
                'doc_ids': docs.ids,
                'doc_model': 'form.resignation',
                'docs': docs,
            }











