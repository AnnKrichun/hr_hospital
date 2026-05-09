from odoo import models, fields, _
from odoo.tools.translate import _


class DiseaseReportWizard(models.TransientModel):
    """
    Wizard for generating medical statistics reports
    filtered by doctors, diseases, and date ranges.
    """
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        help="Filter by specific doctors"
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        help="Filter by specific diseases"
    )
    date_from = fields.Date(
        string='Date From',
        required=True
    )
    date_to = fields.Date(
        string='Date To',
        required=True
    )

    def action_generate_report(self):
        """
        Generates a dynamic view of patient visits based on wizard criteria.
        Returns an action that opens visits in list, pivot, and graph modes.
        """
        self.ensure_one()
        domain = [
            ('visit_date', '>=', self.date_from),
            ('visit_date', '<=', self.date_to)
        ]

        if self.doctor_ids:
            domain.append(('personal_doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        return {
            'name': _('Disease Analysis Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,pivot,graph',
            'domain': domain,
            'context': {
                'group_by': 'disease_id',
                'expand': 1,
                'search_default_disease_id': 1
            },
            'target': 'current',
        }
