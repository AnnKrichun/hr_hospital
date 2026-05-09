from odoo import models, fields, api, _

class VisitReportWizard(models.TransientModel):
    """
    Wizard for generating visit reports filtered by various criteria
    like doctors, patients, dates, and visit status.
    """
    _name = 'visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        help="Filter by selected doctors"
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
        help="Filter by selected patients"
    )
    start_date = fields.Date(
        string='Start Date'
    )
    end_date = fields.Date(
        string='End Date'
    )
    done_only = fields.Boolean(
        string='Completed Visits Only',
        default=False
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease'
    )

    @api.model
    def default_get(self, fields_list):
        """
        Automatically populates doctors or patients if the wizard
        is launched from their respective views.
        """
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')

        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        elif active_model == 'hr.hospital.patient' and active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_generate_report(self):
        """
        Builds a domain and returns an action to display filtered visits.
        """
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('personal_doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.start_date:
            domain.append(('planned_date', '>=', self.start_date))
        if self.end_date:
            domain.append(('planned_date', '<=', self.end_date))
        if self.done_only:
            domain.append(('state', '=', 'done'))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'name': _('Visit Analysis Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
