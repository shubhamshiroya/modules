from odoo import fields, models, api


class ExpenseManagement(models.Model):
    _name = "expense.management"
    _description='this model is for manage expenses'

    expense_name = fields.Char(string="Expense Name",required=True)
    amount_of_expense = fields.Float(string="Amount Of Expense")
    date_and_time_of_expense = fields.Datetime(string="Date And Time")
    vendor_name = fields.Char(string="Vendor Name")

    def name_get(self):
        result = []
        for i in self:
            record1 = i.expense_name
            result.append((i.id, record1))
        return result
