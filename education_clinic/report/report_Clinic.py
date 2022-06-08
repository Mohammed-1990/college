# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime

# Added For report
class MedicalReport(models.AbstractModel):
    _name = 'physical.report'
    _description = 'Medical Report'

    @api.model

    def _get_medical_report_values(self, docids):

        docs = self.env['clinic.physical'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.physical',
                'docs': docs,

            }

# Added For laboratory
class MedicalReport(models.AbstractModel):
    _name = 'laboratory.report'
    _description = 'Medical Report'

    @api.model

    def _get_medical_report_values(self, docids):

        docs = self.env['clinic.laboratory'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.laboratory',
                'docs': docs,

            }

# Added For Optical
class MedicalReport(models.AbstractModel):
    _name = 'eye.report'
    _description = 'Medical Report'
    @api.model
    def _get_medical_report_values(self, docids):
        docs = self.env['clinic.eye'].browse(docids)

        return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.eye',
                'docs': docs,

            }

    # Added For Nursing
    class MedicalReport(models.AbstractModel):
        _name = 'nursing.report'
        _description = 'Medical Report'

        @api.model
        def _get_medical_report_values(self, docids):
            docs = self.env['clinic.nursing'].browse(docids)

            return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.nursing',
                'docs': docs,

            }
    # Added For Dental
    class MedicalReport(models.AbstractModel):
        _name = 'mouth.report'
        _description = 'Medical Report'

        @api.model
        def _get_medical_report_values(self, docids):
            docs = self.env['clinic.mouth'].browse(docids)

            return {
                'doc_ids': docs.ids,
                'doc_model': 'clinic.mouth',
                'docs': docs,

            }

            # Added For Psychological

        class MedicalReport(models.AbstractModel):
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












