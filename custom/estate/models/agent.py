from odoo import fields, models


class Agent(models.Model):
    _name = "agent"
    _description = "Agency in charge of Estate"

    name = fields.Char('Agent name', required=True, translate=True)
    location = fields.Char('Agent location', required=True)
    contact = fields.Char('Phone Number', required=True)
    mail = fields.Char('Email', required=True)
