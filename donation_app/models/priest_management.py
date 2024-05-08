# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class PriestManagement(models.Model):
    _name = 'priest.management'
    _description = 'Priest Management'

    first_name = fields.Char(string='First Name',required=True)
    last_name = fields.Char(string='Last Name',required=True)
    user_name = fields.Char(string='User Name')
    email = fields.Char(string='Email',required=True)
    name = fields.Char(string='Name')
    image_1920 = fields.Image("Image")
    role = fields.Char(string='Role')
    number = fields.Char(string='Phone No:')
    state = fields.Selection([('draft','Draft'),('active','Active'),('inactive','Inactive'),('cancel','Cancel'),('done','Done')],string="State",default="draft")
    donation_purpose = fields.Char(string='Purpose of Donation')
    street = fields.Char(string='Street name')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State Id')
    mentor_id = fields.Many2one('donation.registration', string='Guid')
    zip = fields.Char(string='Zip')
    country_id = fields.Many2one('res.country', string='Country')
    password = fields.Char(string='Password',required=True)
    confirm_password = fields.Char(string='Confirm Password',required=True)
    volunteer_ids = fields.One2many('volunteer.management','mentor_id',string="Volunteers")
    guid_id = fields.Many2one('res.users',string='Mentor',default=lambda self: self.env.user.id,readonly=True)

    def name_get(self):
        result = []
        for i in self:
            record1 = i.first_name + ' ' + i.last_name
            result.append((i.id, record1))
        return result

    def priest_active(self):
        self.write({'state': 'active'})
        query = "SELECT id FROM res_users"
        self.env['res.users'].flush(['id', 'active', 'state'])
        self.env.cr.execute(query, {
            'login': self.email,
        })
        for i in self.env.cr.fetchall():
            user = self.env['res.users'].sudo().browse(i)
            if user.login==self.email:
                user.write({'active': True})

    def priest_inactive(self):
        self.write({'state': 'inactive'})
        user1 = self.env['res.users'].sudo().search([('login', '=', self.email)])
        user1.write({'active': False})

    @api.model
    def create(self, vals):
        res = super(PriestManagement, self).create(vals)
        if res.password != res.confirm_password:
            raise ValidationError("Password and confirm Password not matched")
        template = self.env.ref('donation_app.registration_email_template')
        template.send_mail(res.id, force_send=True, raise_exception=False)
        user1 = self.env['res.users'].create({
            'name': res.first_name + ' ' + res.last_name,
            'login': res.email,
            'email': res.email,
            'password': res.password,
            'groups_id': [(6, 0,[self.env.ref('base.user_admin').id,self.env.ref('base.group_partner_manager').id,
                                 self.env.ref('base.group_user').id,self.env.ref('donation_app.priest_group').id])],
        })
        res.write({'state': 'active'})
        return res
