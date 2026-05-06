from odoo import models, fields, api

class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Візард звіту по хворобах'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Лікарі')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Хвороби')
    date_from = fields.Date(string='З', required=True)
    date_to = fields.Date(string='По', required=True)

    def action_generate_report(self):
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
            'name': 'Звіт по хворобах',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,pivot,graph',
            'domain': domain,
            'context': {'group_by': 'disease_id', 'expand': 1},
            'target': 'current',
        }
