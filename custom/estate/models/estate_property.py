from docutils.parsers import null

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties definition"
    _order = "id desc"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Estate description')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    postcode = fields.Char('PostCode')
    date_availability = fields.Date('Available From', copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    seller_id = fields.Many2one('res.users', string='Seller', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Partner')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer received', 'Offer received'), ('offer accepted', 'Offer Accepted'),
         ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, default='New', string='Status')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float('Best Offer', compute='_compute_best_offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Property Expected Price must be a positive value'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The Property Selling Price must be a positive value')
    ]

    @api.ondelete(at_uninstall=False)
    def check_property_state(self):
        for record in self:
            if (record.state != 'new') and (record.state != 'canceled'):
                print(record.state)
                raise UserError('This property cannot be deleted')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        record_offers = self.mapped("offer_ids")
        self.best_offer = self.compute_best_price_from_offers(record_offers)

    def compute_best_price_from_offers(self, offers):
        best_price = 0
        if len(offers):
            prices = []
            for record_offer in offers:
                prices.append(record_offer.price)
                best_price = max(prices)
        return best_price

    def update_property_state(self, property_id, state):
        print(property_id)
        property_offered = self.env['estate.property'].search([
            ('id', '=', property_id)
        ])
        print(property_offered)
        property_offered.write({'state': state})

    @api.constrains('selling_price')
    def check_price(self):
        for record in self:
            if record.selling_price < (0.09 * record.expected_price) and (record.state == 'offer accepted'):

                raise ValidationError('selling price cannot be lower than 90% of the expected price.')

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
                record_offers = self.mapped("offer_ids")
                if record_offers is not None:
                    for record_offer in record_offers:
                        if record_offer.status != 'accepted':
                            record_offer.status = 'refused'
            else:
                raise UserError('This property is canceled! it cannot be sold')
        return True

    def action_cancel(self):
        for record in self:
            if record.state != 'sold' and record.state != 'offer accepted':
                record.state = 'canceled'
            else:
                raise UserError('This property is sold! it cannot be canceled')
        return True
