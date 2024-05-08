from odoo import fields,models,api
import pytz
from datetime import datetime,timedelta

class CalendarModel(models.Model):
    _name="calendar.management"
    _description="this model is for creating custom calendar view"

    @api.model
    def _default_partners_calendar(self):
        """ When active_model is res.partner, the current partners should be attendees """
        partners = self.env.user.partner_id
        active_id = self._context.get('active_id')
        if self._context.get('active_model') == 'res.partner' and active_id:
            if active_id not in partners.ids:
                partners |= self.env['res.partner'].browse(active_id)
        return partners

    name = fields.Char(string="Event Name",required=True)
    date_and_time = fields.Datetime(string="Date and Time")
    address = fields.Char(string="Address")
    purpose = fields.Char(string="Purpose")
    email = fields.Char(string="Email")
    mobile_number = fields.Integer(string="Mobile number")
    uid = fields.Many2one('res.users', string="Users",required=True)
    partner_ids = fields.Many2many(
        'res.partner', 'calendar_management_res_partner_rel',
        string='Attendees', default=_default_partners_calendar)

    def name_get(self):
        result = []
        for i in self:
            record1 = i.name
            result.append((i.id, record1))
        return result

    @api.model
    def default_get(self, fields):
        rec = super(CalendarModel, self).default_get(fields)
        if self.uid not in rec:
            rec.update({
                'uid': self.env.user.id
            })
        return rec