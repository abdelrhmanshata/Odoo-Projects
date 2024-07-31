from datetime import date
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
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
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        inverse="_inverse_compute_age",
        search="_search_age",
        tracking=True,
    )
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
    appointment_count = fields.Integer(
        string="Appointment Count",
        compute="_compute_appointment_count",
        tracking=True,
        store=True,
    )

    appointment_ids = fields.One2many(
        "hospital.appointment", "patient_id", string="Appointments"
    )

    @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env["hospital.appointment"].search_count(
                [("patient_id", "=", rec.id)]
            )

    @api.constrains("date_of_birth")
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > datetime.date.today():
                raise ValidationError(_("Date of birth cannot be in the future."))

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(
                    _("Cannot delete patient with existing appointments.")
                )

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

    @api.depends("age")
    def _inverse_compute_age(self):
        for rec in self:
            today = date.today()
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        # for rec in self:
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        # return [("date_of_birth", "=", date_of_birth)]

        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [("date_of_birth", ">=", start_of_year),("date_of_birth", "<=", end_of_year)]



    def name_get(self):
        # patient_list = []
        # for record in self:
        #     name = record.ref + " " + record.name
        #     patient_list.append((record.id, name))
        # return patient_list
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]

    def action_GroupBy(self):
        pass
