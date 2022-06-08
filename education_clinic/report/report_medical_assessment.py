
# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime

# Report

class MedicalReportCicology(models.AbstractModel):
    _name = 'assessment.report'
    _description = 'Medical Report'

    @api.model

    def _get_medical_report_values(self, docids):

        docs = self.env['clinic.assessment'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.assessment',
                'docs': docs,

            }
