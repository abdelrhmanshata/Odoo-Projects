from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _rec_name = "ref"

    # ondelete="restrict" -> can't delete object is connect a fkey
    # ondelete="cascade" -> can't delete object is connect a fkey

    patient_id = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", ondelete="restrict"
    )
    patient_gender = fields.Selection(related="patient_id.gender", readonly=True)

    appointment_time = fields.Datetime(
        string="Appointment Time", default=lambda self: fields.Datetime.now()
    )
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(
        string="Reference", default="Odoo Mates", help="Reference to the patient record"
    )
    prescription = fields.Html(string="Prescription")

    docter_id = fields.Many2one("res.users", string="Docter")

    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Favorite"),
        ],
        default="0",
        string="Priority",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_consultation", "In Consultation"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        string="State",
        required=True,
    )

    pharmacy_line_ids = fields.One2many(
        "appointment.pharmacy.lines", "appointment_id", string="Pharmacy lines"
    )
    hide_sales_price = fields.Boolean(string="Hide Sales Price ")

    @api.onchange("patient_id")
    def onChange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        return {
            "effect": {
                "fadeout": "slow",
                "message": "Click Successfully",
                # 'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/img/smile.svg',
                "type": "rainbow_man",
            }
        }

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_in_consultation(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        # for rec in self:
        #     rec.state = 'cancel'
        action = self.env.ref("om_hospital.cancel_appointment_action").read()[0]
        return action

    def unlink(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(
                    _("You can delete appointment only in 'Draft'  status !")
                )
        return super(HospitalAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one("product.product", required=True)
    price_unit = fields.Float(related="product_id.list_price", string="Price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
