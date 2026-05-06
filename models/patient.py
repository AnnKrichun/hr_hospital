
from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Patient'
    _rec_name = 'name'
    _rec_names_search = ['name']

    phone = fields.Char(string='Телефон', help="Контактний номер пацієнта")

    name = fields.Char(string='Full Name', required=True)
    personal_doctor_id = fields.Many2one('hr.hospital.doctor', string='Персональний лікар')

    doctor_history_ids = fields.One2many(
        'hr.hospital.doctor.history',
        'patient_id',
        string='Історія персональних лікарів'
    )

    insurance_number = fields.Char(string='Номер страхового поліса', size=20)

    visit_ids = fields.One2many(
        'hr.hospital.visit',
        'patient_id',
        string='Історія візитів',
        readonly=True
    )

    visit_count = fields.Integer(compute='_compute_visit_count')

    def _compute_visit_count(self):
        for rec in self:
            rec.visit_count = self.env['hr.hospital.visit'].search_count([
                ('patient_id', '=', rec.id)
            ])
    @api.depends('name')
    def _compute_display_name(self):
        for rec in self:
          rec.display_name = rec.name or "No Name"

    def action_view_patient_visits(self):
        self.ensure_one()
        return {
            'name': 'Візити пацієнта',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_new_visit(self):
        self.ensure_one()
        return {
            'name': 'Записати на візит',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_planned_date': fields.Datetime.now(),
            }
        }

