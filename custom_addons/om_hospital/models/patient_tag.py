from datetime import date
from odoo import api, models,fields
 
class PatientTag(models.Model):
    _name="patient.tag"
    _description="Patient Tag"
    
    name = fields.Char(string="Name", tracking=True)
    active = fields.Boolean(string="Active",default=True)
    color_qwe = fields.Integer(string="Color")  
    color_2 = fields.Char(string="Color 2")                      