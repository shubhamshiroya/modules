# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re
from odoo.exceptions import ValidationError


class DonationRegistration(models.Model):
    _name = 'donation.registration'
    _description = 'registration for donation'

    first_name = fields.Char(string='First Name',required=True)
    last_name = fields.Char(string='Last Name',required=True)
    center_name = fields.Char(string='Center Name',required=True)
    number = fields.Char(string='Phone Number')
    address = fields.Text(string='Center Address')
    email = fields.Char(string='Email',required=True)
    street = fields.Char(string='Street name')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='Zip')
    country_id = fields.Many2one('res.country', string='Country')
    password = fields.Char('Password',required=True)
    confirm_password = fields.Char(string='Confirm Password',required=True)

    def name_get(self):
        result = []
        for i in self:
            record1 = i.first_name + ' ' + i.last_name
            result.append((i.id, record1))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        domain = ['|', ('last_name', operator, name), ('first_name', operator, name)]
        record = super(DonationRegistration, self).search(domain, limit=limit).name_get()
        return record

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Please Enter valid E-mail ID')

    @api.model
    def create(self, vals):
        res = super(DonationRegistration, self).create(vals)
        if res.password != res.confirm_password:
            raise ValidationError("Password and confirm Password not matched")
        template = self.env.ref('donation_app.registration_email_admin_template')
        template.send_mail(res.id, force_send=True, raise_exception=False)
        user1 = self.env['res.users'].create({
            'name': res.first_name + ' ' + res.last_name,
            'login': res.email,
            'email': res.email,
            'password': res.password,
            'groups_id': [(6, 0, [self.env.ref('base.user_admin').id,self.env.ref('base.group_partner_manager').id,
                                  self.env.ref('base.group_user').id,
                                  self.env.ref('donation_app.admin_group').id])],

        })
        return res
