from odoo import http


class EstateController(http.Controller):
    @http.route('/estate/estate_controller/', auth='public')
    def index(self, **kwargs):
        estate_properties = http.request.env['estate.property'].search([])
        for estate in estate_properties:
            print(estate['name'])
        return "Estate Properties"

    @http.route('/estate/estate_properties/', website=False, auth='public')
    def properties(self, **kwargs):
        # estate_properties = http.request.env['estate.property'].search([])
        return http.request.render('estate_property_view_tree', {
            'estates': http.request.env['estate.property'].search([])
        })
    #
    # @http.route('/estate/estate_controller/estates/<model("estate/estate_controller"):obj>/', auth='public')
    # def object(self, obj, **kwargs):
    #     return http.request.render('estate_controller.object', {'object': obj})
