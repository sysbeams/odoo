
from odoo import fields, models, api, _


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Properties Type"
    _order = "name"

    name = fields.Char('Title')
    property_ids = fields.One2many('estate.property', 'type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_counts = fields.Integer('Offer Counts', compute='_compute_offer_counts')
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('check_type', 'UNIQUE(name)',
         'Type name must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_counts(self):
        record_offers = self.mapped("offer_ids")
        if record_offers is not None:
            self.offer_counts = len(record_offers)
        else:
            self.offer_counts = 0

    def action_offer_list(self):
        return {
            'name': _('Offers'),
            'view_mode': 'list',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {}
        }
