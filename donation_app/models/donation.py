# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class DonationForm(models.Model):
    _name = 'donation.form'
    _description = 'donation form'

    donor_name = fields.Char(string="Donor's Name",required=True)
    number = fields.Char(string="Donor's Phone No:")
    address = fields.Text(string="Donor's Address")
    donation_purpose = fields.Char(string='Purpose of Donation')
    street = fields.Char(string='Street name')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char(string='Zip')
    amount = fields.Float(string='Amount of Donation')
    sequence = fields.Char(string='Sequence',default='New')
    email = fields.Char(string='Email',required=True)
    name = fields.Char(string="Id", default='New')
    current_time = fields.Datetime(string='Time', default=lambda self: fields.Datetime.now(),readonly=True)
    birthday_date = fields.Date(string="Birthday Date",default=lambda self: fields.Date.today(),required=True)
    anniversary_date = fields.Date(string="Anniversary Date")

    @api.onchange('amount')
    def amount_type_onchange(self):
        for check in self:
            if check.amount < 0:
                raise ValidationError('Please Enter Amount >0')

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('donation.form')
        return super(DonationForm, self).create(vals)

    def birthday_email_scheduler(self):
        template = self.env.ref('donation_app.donation_email_template')
        today = date.today().strftime('%d-%m')
        active_record_ids = self.env['donation.form'].search([])

        for id in active_record_ids:
            if id.birthday_date.strftime('%d-%m') == today or (id.anniversary_date and id.anniversary_date.strftime('%d-%m') == today):
                template.send_mail(id.id, force_send=True, raise_exception=False)

    def payment_offline(self):
        payment = self.env['payment.management'].create(
            {
                'name': self.donor_name,
                'email': self.email,
                'time': self.current_time,
                'mobile': self.number,
                'amount': self.amount,
            }
        )
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Offline Payment Done.. Thank You..',
                'type': 'rainbow_man',
            }
        }