from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        _logger.info(f"Default get executed {res}")
        _logger.info(f".... Context", self.env.context)
        res["date_cancel"] = datetime.date.today()
        res["reason"] = "Test Text"
        if self.env.context.get("active_id"):
            res["appointment_id"] = self.env.context.get("active_id")
        return res

    appointment_id = fields.Many2one(
        "hospital.appointment",
        string="Appointment ID",
        domain=["|", ("state", "=", "draft"), ("priority", "in", ("0", "1", False))],
    )
    reason = fields.Text(string="Reason", default="Test Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        _logger.info(
            f"=================> {self.appointment_id.booking_date}  * {datetime.date.today()}"
        )
        if self.appointment_id.booking_date == datetime.date.today():
            raise ValidationError(
                _("Sorry , cancellation is not allowed on the same day of booking !")
            )
        self.appointment_id.state='cancel'    
        return
