import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Properties Offers"
    _order = "price desc"

    price = fields.Float('Price')
    property_id = fields.Many2one('estate.property', string='Property')
    property_type_id = fields.Many2one(related='property_id.type_id', string='Property Type', store=True)
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

    @api.model
    def create(self, vals_list):
        property_sold = self.env['estate.property'].browse(vals_list['property_id'])
        if self.check_property_state(property_sold, vals_list['price']):
            property_sold.update_property_state(property_sold.id, 'offer received')
        return super(EstatePropertyOffer, self).create(vals_list)

    def check_property_state(self, property_sold, offer_price):
        if property_sold.state == 'offer received':
            if property_sold.best_offer > offer_price:
                raise UserError('offer bid lower than previous bid')
            else:
                return True
        return True

    def action_accept(self):
        for offer in self:
            property_sold = offer.mapped('property_id')
            if property_sold.state != 'sold':
                property_sold.buyer_id = self.buyer_id
                property_sold.selling_price = self.price
                property_sold.state = 'offer accepted'
                offer.status = 'accepted'
            else:
                raise UserError('Property sold')
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
