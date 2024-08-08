from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _rec_name = "ref"
    _order = "id desc"

    # ondelete="restrict" -> can't delete object is connect a fkey
    # ondelete="cascade" -> can't delete object is connect a fkey

    name = fields.Char(string="Sequence", default="New", tracking=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Patient",
        ondelete="restrict",
        tracking=1,
    )
    patient_gender = fields.Selection(related="patient_id.gender", readonly=True)

    appointment_time = fields.Datetime(
        string="Appointment Time", default=lambda self: fields.Datetime.now()
    )
    booking_date = fields.Date(
        string="Booking Date", default=fields.Date.context_today, tracking=True
    )
    duration = fields.Float(string="Duration", tracking=25)
    ref = fields.Char(
        string="Reference", default="Odoo Mates", help="Reference to the patient record"
    )
    prescription = fields.Html(string="Prescription")

    docter_id = fields.Many2one("res.users", string="Docter", tracking=10)

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
        tracking=2,
    )

    pharmacy_line_ids = fields.One2many(
        "appointment.pharmacy.lines", "appointment_id", string="Pharmacy lines"
    )
    hide_sales_price = fields.Boolean(string="Hide Sales Price ")

    # operation_id = fields.Many2one("hospital.operation", string="Operation")
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    progress_gauge = fields.Integer(
        string="Progress Gauge", compute="_compute_progress"
    )
    progress_percentpie = fields.Integer(
        string="Progress Percentpie", compute="_compute_progress"
    )

    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )

    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")

    url = fields.Char(string="Url", default="https://www.google.com")

    @api.onchange("patient_id")
    def onChange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        return {
            "type": "ir.actions.act_url",
            "taget": "new",
            # "url": "https://www.google.com",
            "url": self.url,
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
        return {
            "effect": {
                "fadeout": "slow",
                "message": "Done",
                # 'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/img/smile.svg',
                "type": "rainbow_man",
            }
        }

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

    @api.depends("state")
    def _compute_progress(self):
        for rec in self:
            if rec.state == "draft":
                progress = random.randrange(0, 40)
            elif rec.state == "in_consultation":
                progress = random.randrange(40, 80)
            elif rec.state == "done":
                progress = 100
            else:
                progress = 0

            rec.progress = progress
            rec.progress_gauge = progress
            rec.progress_percentpie = progress

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing phone number in patient record!"))

        message = "Hi *%s* ,you *appointment* number is :%s ,Thank you" % (
            self.patient_id.name,
            self.name,
        )
        whatsapp_api = "https://api.whatsapp.com/send?phone=+20%s&text=%s" % (
            self.patient_id.phone,
            message,
        )

        self.message_post(body=message, subject="WhatsApp Messaeg")

        return {"type": "ir.actions.act_url", "target": "new", "url": whatsapp_api}

    def action_notification(self):
        message = "Button Click Successfully"
        # return {
        #     "type": "ir.actions.client",
        #     "tag": "display_notification",
        #     "params": {
        #         "message": message,
        #         "type": "success",
        #         # "type": "warning",
        #         # "type": "danger",
        #         "sticky": True,
        #     },
        # }

        action = self.env.ref("om_hospital.hospital_patient_action")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Click To Open The Patient Record"),
                "message": "%s",
                "type": "success",
                "sticky": True,
                "links": [
                    {
                        "label": self.patient_id.name,
                        "url": f"#action={action.id}&id={self.patient_id.id}&model=hospital.patient",
                    }
                ],
                "next": {
                    "type": "ir.actions.act_window",
                    "res_model": "hospital.patient",
                    "res_id": self.patient_id.id,
                    "views": [(False, "form")],
                },
            },
        }

    def action_send_mail(self):
        return
        # template = self.env.ref("om_hospital.appointment_mail_template")
        # for rec in self:
        #     template.send_mail(rec.id)


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one("product.product", required=True)
    price_unit = fields.Float(
        related="product_id.list_price", string="Price", digits="Product Price"
    )
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    currency_id = fields.Many2one("res.currency", related="appointment_id.currency_id")
    price_subtotal = fields.Monetary(
        "Subtotal",
        compute="_compute_price_subtotal",
        currency_field="currency_id",
    )

    @api.depends("price_unit", "qty")
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.qty * rec.price_unit
