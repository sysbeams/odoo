from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Tabel for property records"

    name = fields.Char('Plan name', required=True)
    description = fields.Text('Property description', required=True)
    postcode = fields.Char('Property Postcode', required=True)
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("Good", "Good"), ("Bad", "Bad")])
