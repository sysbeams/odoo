from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties definition"

    name = fields.Char('Estate Name', required=True, translate=True)
    description = fields.Text('Estate description', required=True)
    location = fields.Char('Geo Location', required=True)
    postcode = fields.Char('Postal Address')
    date_availability = fields.Date('Available date', required=True)
    expected_price = fields.Float('Price', required=True)
    selling_price = fields.Float('Selling Price', required=True)
    bedrooms = fields.Integer('Number of bedrooms', required=True)
    living_area = fields.Integer('Number of living room', required=True)
    owner = fields.Char('Owner name', required=True)
    active = fields.Boolean('Active', default=True)
