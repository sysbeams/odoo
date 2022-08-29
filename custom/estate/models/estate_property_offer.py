import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Properties Offers"

    price = fields.Float('Price')
    property_id = fields.Many2one('estate.property', string='Property')
    buyer_id = fields.Many2one('res.partner', string='Partner')
    active = fields.Boolean('Active', default=True)
    status = fields.Selection(
        [('new', 'New'), ('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, default='new')
    validity = fields.Integer('Validity (Days)', default=7)
    # date_deadline = fields.Datetime('Deadline Date', compute='_compute_deadline_date',
    #                                 inverse='_inverse_deadline_date')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Property Offered Price must be a positive value'),
    ]

    # @api.depends('create_date', 'validity')
    # def _compute_deadline_date(self):
    #     create_date = fields.Datetime.from_string(self.create_date)
    #     print(create_date)
    #     date = datetime.timedelta(days=self.validity)
    #     print(date)
    #     self.date_deadline = create_date + date
    #
    # @api.depends('create_date', 'validity')
    # def _inverse_deadline_date(self):
    #     for offer in self:
    #         today = datetime.now()
    #         date = datetime.timedelta(days=offer.validity)
    #         offer.date_deadline = today + date

    def action_accept(self):
        for offer in self:
            property_sold = offer.mapped('property_id')
            if offer.status != 'accepted':
                property_sold.buyer_id = self.buyer_id
                property_sold.selling_price = self.price
                property_sold.state = 'offer accepted'
                offer.status = 'accepted'
            else:
                raise UserError('Offer already accepted')
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status != 'accepted':
                offer.status = 'refused'
            else:
                raise UserError('Offer already accepted')
        return True
