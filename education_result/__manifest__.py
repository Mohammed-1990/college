# -*- coding: utf-8 -*-
{
    'name': "Scientific Affairs",

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
                'education_college',
                ],
    # always loaded
    'data': [
         'security/result_security.xml',
        'security/ir.model.access.csv',
# menus
        'menus/menu.xml',
        'views/configuration.xml',
        'views/result.xml',
        'views/rate.xml',
        'views/subject_handling.xml',
        'views/processing_degree.xml',
        'report/report_exam_result_template.xml',
        'wizard/exam _result_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
