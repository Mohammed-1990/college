# -*- coding: utf-8 -*-
# from odoo import http


# class EducationCollege(http.Controller):
#     @http.route('/education_college/education_college/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_college/education_college/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_college.listing', {
#             'root': '/education_college/education_college',
#             'objects': http.request.env['education_college.education_college'].search([]),
#         })

#     @http.route('/education_college/education_college/objects/<model("education_college.education_college"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_college.object', {
#             'object': obj
#         })
