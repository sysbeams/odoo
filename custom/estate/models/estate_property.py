import datetime

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties definition"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Estate description')
    location = fields.Char('Geo Location')
    postcode = fields.Char('PostCode')
    date_availability = fields.Date('Available From', copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)', default=2)
    owner = fields.Char('Owner name', required=True)
    active = fields.Boolean('Active', default=False)
    state = fields.Selection(
        [('new', 'New'), ('offer received', 'Offer received'), ('offer accepted', 'Offer Accepted'),
         ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, default='New')

