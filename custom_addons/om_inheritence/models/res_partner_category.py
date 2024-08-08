from odoo import models, fields, api


class PartnerCategory(models.Model):
    name = "res.partner.category"
    _inherit = ["res.partner.category", "mail.thread"]

    name=fields.Char(tracking=True)