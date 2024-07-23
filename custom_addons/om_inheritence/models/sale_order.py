from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one("res.users", string="Confirmed User")

    def action_confirm(self):
        print("Successfully confirmed")
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id

    @api.model
    def create(self, vals):
        _logger.info(f"Creating sale order with vals: {vals}")
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        _logger.info(f"Writing sale order with vals: {vals}")
        return super(SaleOrder, self).write(vals)
