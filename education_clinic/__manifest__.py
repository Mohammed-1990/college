 # -*- coding: utf-8 -*-
{
    'name': "education_clinic",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'education_college'

                ],
    # always loaded
    'data': [
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        'menus/clinic.xml',
        'views/nursing.xml',
        'views/eye.xml',
        'views/mouth.xml',
        'wizards/clinic_wizard.xml',
        'views/physical.xml',
        'views/laboratory.xml',
        'views/psychological.xml',
        'report/report_medical_assessment.xml',
        'report/report_clinic.xml',
        'report/report_clinic_template.xml',
        'report/report_medical_assessment_template.xml',
        # menus



    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
