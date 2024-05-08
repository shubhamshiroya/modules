# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VolunteerRole(models.Model):
    _name = 'volunteer.role'
    _description = 'Volunteer Role'

    name = fields.Char(string='Name',required=True)