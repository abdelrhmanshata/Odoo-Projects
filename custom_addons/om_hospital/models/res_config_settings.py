from odoo import api, models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_days = fields.Integer(string="Cancel Days",config_parameter="om_hospital.cancel_day")
