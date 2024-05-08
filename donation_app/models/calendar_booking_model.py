from odoo import fields,models,api,exceptions,_
import pytz
from datetime import datetime,timedelta


class CalendarModel(models.Model):
    _name="calendar.booking"
    _description="this model is for creating custom calendar view for booking"

    name = fields.Char(string="Event Name",required=True)
    date_and_time = fields.Datetime(string="Date and Time")
    address = fields.Char(string="Address")
    purpose = fields.Char(string="Purpose")
    email = fields.Char(string="Email")
    mobile_number = fields.Integer(string="Mobile number")
    uid = fields.Many2one('res.users', string="Users",required=True)
    partner_ids = fields.Many2many(
        'res.partner', 'calendar_booking_res_partner_rel',
        string='Attendees')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
        ], string='State', default="draft")
    attendee_ids = fields.One2many(
        'calendar.attendee', 'event_id', 'Participant')

    def call_from_js(self):
        groups = self.env.user.groups_id.ids

        if self.env.ref('donation_app.priest_group').id in groups:
            return True

    @api.model
    def default_get(self, fields):
        rec = super(CalendarModel, self).default_get(fields)
        group = self.env.user.groups_id.ids
        user = self.env.user.id
        if self.env.ref('donation_app.admin_group').id in group:
            rec.update({
                'state': 'accept',
                'uid':user
            })
        else:
            rec.update({
                'state': 'draft',
                'uid':user
            })
        return rec

    def button_accept(self):
        self.write({'state': 'accept'})

    def button_reject(self):
        self.write({'state': 'reject'})

    def name_get(self):
        result = []
        for i in self:
            record1 = i.name
            result.append((i.id, record1))
        return result

    def get_notification_event_scheduler(self):
        time_zone=pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        ind_time = datetime.now(time_zone)+ timedelta(minutes=10)
        validation = self.env['calendar.booking'].search([('state','=','accept')])
        for rec in validation:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            if rec.date_and_time and pytz.utc.localize(rec.date_and_time).astimezone(user_tz).strftime('%Y-%m-%d %H:%M') == ind_time.strftime('%Y-%m-%d %H:%M'):
                rec.uid.notify_info()

    @api.model
    def default_get(self, fields):
        rec = super(CalendarModel, self).default_get(fields)
        if self.uid not in rec:
            rec.update({
                'uid': self.env.user.id
            })
        return rec