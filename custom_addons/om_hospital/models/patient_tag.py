from datetime import date
from odoo import api, models, fields, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name", tracking=True)
    active = fields.Boolean(string="Active", default=True, copy=False)
    color_qwe = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ("unique_tag_name", "unique (name,active)", "Name Must be unique"),
        ("unique_sequence", "unique (sequence)", "Sequence Must be unique"),
        (
            "check_sequence",
            "check(sequence > 0)",
            "sequence Must be non zero positive number",
        ),
    ]

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}

        if not default.get("name"):
            default["name"] = _("%s (Copy)", self.name)
            default["sequence"] = self.sequence * 10
        return super(PatientTag, self).copy(default)
