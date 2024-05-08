from odoo import fields,models,api


class PaymentManagement(models.Model):
    _name='payment.management'
    _description='this model is for manage payments'

    name=fields.Char(string='name',required=True)
    email = fields.Char(string='email')
    amount = fields.Float(string='amount',required=True)
    time = fields.Datetime(string='Date And Time')
    mobile = fields.Integer(string='Mobile Number')