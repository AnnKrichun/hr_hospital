
from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Full Name', required=True)
    birthday = fields.Date(string='Date of Birth')
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Personal Doctor')
