from odoo import fields, models, api


class Medicine(models.Model):
    _name = 'student.record'
    _description = 'student management'

    name = fields.Char(string='Name:', required=True)
    phone_numbers = fields.Char("Phone Number:")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],'Gender:')
    birthday = fields.Date(string="Birthday:")
    email = fields.Char(string='Email:')
    address = fields.Char(string="Address:")
    password = fields.Char(string='Password:')
    active = fields.Boolean(default=True)

    def action_confirm_archive(self):
        print('\n\n work fine')

    def action_confirm_unarchive(self):
        print('\n\n work fine unarchive')

