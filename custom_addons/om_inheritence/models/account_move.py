from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    so_confirmed_user_id = fields.Many2one("res.users", string="So confirmed user")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    line_number = fields.Integer(string="line number")
