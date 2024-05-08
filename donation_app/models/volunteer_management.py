# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class VolunteerManagement(models.Model):
    _name = 'volunteer.management'
    _description = 'Volunteer Management'

    first_name = fields.Char(string='First Name',required=True)
    last_name = fields.Char(string='Last Name',required=True)
    user_name = fields.Char(string='User Name')
    email = fields.Char(string='Email',required=True)
    name = fields.Char(string='Name')
    image_1920 = fields.Image("Image")
    volunteer_role_id = fields.Many2one('volunteer.role',string='Volunteer Role',required=True)
    number = fields.Char(string='Phone No:')
    state = fields.Selection([('draft','Draft'),('active','Active'),('inactive','Inactive'),('cancel','Cancel'),('done','Done')],string="State",default="draft")
    donation_purpose = fields.Char(string='Purpose of Donation')
    street = fields.Char(string='Street name')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State Id')
    mentor_id = fields.Many2one('priest.management', string='Mentor',required=True)
    zip = fields.Char(string='Zip')
    country_id = fields.Many2one('res.country', string='Country')
    password = fields.Char(string='Password',required=True)
    confirm_password = fields.Char(string='Confirm Password',required=True)

    def name_get(self):
        result = []
        for i in self:
            record1 = i.first_name + ' ' + i.last_name
            result.append((i.id, record1))
        return result

    def priest_active(self):
        self.write({'state': 'active'})
        record= self.env['res.users'].sudo().search([('login', '=', self.email)])
        query = "SELECT id FROM res_users"
        self.env['res.users'].flush(['id', 'active', 'state'])
        self.env.cr.execute(query, {
            'login': self.email,
        })
        for i in self.env.cr.fetchall():
            user = self.env['res.users'].sudo().browse(i)
            if user.login == self.email:
                user.write({'active': True})

    def priest_inactive(self):
        self.write({'state': 'inactive'})
        user = self.env['res.users'].sudo().search([('login', '=', self.email)])
        user.write({'active': False})

    @api.model
    def create(self, vals):
        res = super(VolunteerManagement, self).create(vals)
        group_id_rec = 0
        if res.volunteer_role_id.name == "Donation Management":
            group_id_rec += self.env.ref('donation_app.donation_form_group').id
        elif res.volunteer_role_id.name == "Volunteer Management":
            group_id_rec += self.env.ref('donation_app.volunteer_group').id
        elif res.volunteer_role_id.name == "Calendar Management":
            group_id_rec += self.env.ref('donation_app.calendar_group').id
        elif res.volunteer_role_id.name == "Payment Management":
            group_id_rec += self.env.ref('donation_app.payment_group').id
        elif res.volunteer_role_id.name == "Expense Management":
            group_id_rec += self.env.ref('donation_app.expense_group').id
        if res.password != res.confirm_password:
            raise ValidationError("Password and confirm Password not matched")
        template = self.env.ref('donation_app.registration_email_volunteer_template')
        template.send_mail(res.id, force_send=True, raise_exception=False)
        user1 = self.env['res.users'].create({
            'name': res.first_name + ' ' + res.last_name,
            'login': res.email,
            'email': res.email,
            'password': res.password,
            'groups_id': [(6, 0, [group_id_rec,self.env.ref('base.group_user').id])],
        })
        res.write({'state': 'active'})
        return res

    def write(self, values):
        res = super(VolunteerManagement, self).write(values)
        group_id_rec = 0
        if self.volunteer_role_id.name == "Donation Management":
            group_id_rec += self.env.ref('donation_app.donation_form_group').id
        elif self.volunteer_role_id.name == "Volunteer Management":
            group_id_rec += self.env.ref('donation_app.volunteer_group').id
        elif self.volunteer_role_id.name == "Calendar Management":
            group_id_rec += self.env.ref('donation_app.calendar_group').id
        elif self.volunteer_role_id.name == "Payment Management":
            group_id_rec += self.env.ref('donation_app.payment_group').id
        elif self.volunteer_role_id.name == "Expense Management":
            group_id_rec += self.env.ref('donation_app.expense_group').id
        user1 = self.env['res.users'].search([('login', '=', self.email)])
        user1.update({
            'groups_id': [(6, 0,
                           [group_id_rec, self.env.ref('base.group_user').id])],
        })
        return res

    @api.model
    def default_get(self, fields):
        rec = super(VolunteerManagement, self).default_get(fields)
        user = self.env['priest.management'].search([])
        if self.mentor_id not in rec:
            rec.update({
                'mentor_id': user.id
            })
        return rec