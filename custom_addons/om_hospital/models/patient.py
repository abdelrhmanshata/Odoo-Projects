from datetime import date
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth", tracking=True)
    ref = fields.Char(string="Reference", default="Odoo Mates")
    age = fields.Integer(string="Age", compute="_compute_age", tracking=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        string="Gender",
        tracking=True,
        default="male",
    )
    active = fields.Boolean(string="Active", default=True)

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many("patient.tag", string="Tags")
    appointment_count = fields.Integer(string="Appointment Count")

    @api.constrains("date_of_birth")
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > datetime.date.today():
                raise ValidationError(_("Date of birth cannot be in the future."))

    @api.model
    def create(self, vals):
        _logger.info(f"Creating sale order with vals: {vals}")
        vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        _logger.info(f"Writing sale order with vals: {vals}")
        if not self.ref and not vals.get("ref"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).write(vals)

   
    @api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    def name_get(self):
        # patient_list = []
        # for record in self:
        #     name = record.ref + " " + record.name
        #     patient_list.append((record.id, name))
        # return patient_list
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]
