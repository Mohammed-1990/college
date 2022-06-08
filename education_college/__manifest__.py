# -*- coding: utf-8 -*-
{
    'name': "education_college",

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
    'depends': ['base','mail'],


    # always loaded
    'data': [
        'security/education_security.xml',
        'security/ir.model.access.csv',
        'menus/education_menu.xml',
        'views/configuration.xml',
        'views/admission.xml',
        'views/new_student_information.xml',
        'views/old_student_information.xml',
        'views/fees.xml',
        'wizard/discounts_wizard.xml',
        'wizard/make_payment.xml',
        'views/registrar_office.xml',
        # 'views/forms.xml',
         'views/student_portal_view.xml',
         'report/header_footer.xml',
        'report/report_presentation.xml',
        'report/report_presentation_template.xml',
        'report/report_registar_template.xml',
        'report/report_admission_template.xml',
        'wizard/registrar_report_wizard.xml',
        'wizard/admission_report_wizard.xml',


        




    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
