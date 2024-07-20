from odoo import fields,models,api

class CancelAppointmentWizard(models.TransientModel):
    _name="cancel.appointment.wizard"
    _description="Cancel Appointment Wizard"
    
    appointment_id = fields.Many2one('hospital.appointment',string="Appointment ID")
    reason = fields.Text(string="Reason")
    
    
    def action_cancel(self):
        return

