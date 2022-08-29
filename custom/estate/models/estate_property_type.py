

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Properties Type"

    name = fields.Char('Title')

    _sql_constraints = [
        ('check_type', 'UNIQUE(name)',
         'Type name must be unique'),
    ]


