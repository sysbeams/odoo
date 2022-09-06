from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id', 'Real Estate Properties',
                                   domain=[("state", "in", ["new", "offer_received"])])
