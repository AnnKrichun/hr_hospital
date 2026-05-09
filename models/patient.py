from odoo import models, fields, api, _

class HospitalPatient(models.Model):
    """
    Model representing patients in the hospital system.
    Inherits common medical fields from hr.hospital.medic.info.
    """
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Hospital Patient'
    _rec_name = 'name'
    _rec_names_search = ['name']

    name = fields.Char(string='Full Name', required=True)

    phone = fields.Char(
        string='Phone',
        help="Patient's primary contact number"
    )
    personal_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Personal Doctor'
    )
    insurance_number = fields.Char(
        string='Insurance Number',
        size=20
    )

    doctor_history_ids = fields.One2many(
        'hr.hospital.doctor.history',
        'patient_id',
        string='Personal Doctor History'
    )
    visit_ids = fields.One2many(
        'hr.hospital.visit',
        'patient_id',
        string='Visit History',
        readonly=True
    )
    visit_count = fields.Integer(
        string='Visit Count',
        compute='_compute_visit_count'
    )

    def _compute_visit_count(self):
        """Calculates the total number of visits for each patient."""
        for rec in self:
            rec.visit_count = self.env['hr.hospital.visit'].search_count([
                ('patient_id', '=', rec.id)
            ])

    @api.depends('name')
    def _compute_display_name(self):
        """Sets the display name, providing a fallback if name is not set."""
        for rec in self:
            rec.display_name = rec.name or _("No Name")

    def action_view_patient_visits(self):
        """
        Action to open a list of all visits for this patient.
        Includes list, form, and calendar views.
        """
        self.ensure_one()
        return {
            'name': _('Patient Visits'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_new_visit(self):
        """Opens a quick creation form for a new patient visit."""
        self.ensure_one()
        return {
            'name': _('Schedule New Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_planned_date': fields.Datetime.now(),
            }
        }
