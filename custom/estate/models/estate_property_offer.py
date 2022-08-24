

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Properties Offers"

    price = fields.Float('Price')
    property_id = fields.Many2one('estate.property', string='Property')
    buyer_id = fields.Many2one('res.partner', string='Partner')
    active = fields.Boolean('Active', default=False)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)

