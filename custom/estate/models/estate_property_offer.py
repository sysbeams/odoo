from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Properties Offers"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The Property Offered Price must be a positive value'),
    ]

    price = fields.Float('Price', required=True)
    property_id = fields.Many2one('estate.property', string='Property')
    property_type_id = fields.Many2one(related='property_id.type_id', string='Property Type', store=True)
    buyer_id = fields.Many2one('res.partner', string='Partner')
    active = fields.Boolean('Active', default=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, string='Status')
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline Date', compute='_compute_deadline_date',
                                inverse='_inverse_deadline_date')

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    @api.depends('create_date', 'validity')
    def _inverse_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

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
            if 'accepted' in self.mapped("property_id.offer_ids.status") and property_sold.state == 'sold':
                raise UserError('An offer already has been accepted or property sold')
            else:
                self.write({"status": 'accepted'})
                return self.mapped('property_id').write(
                    {
                        "buyer_id": self.buyer_id,
                        "selling_price": self.price,
                        "state": 'offer accepted',
                    }
                )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused"
            }
        )
