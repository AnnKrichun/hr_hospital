from odoo import models, fields, api

class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Звіт по візитах'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Лікарі')
    patient_ids = fields.Many2many('hr.hospital.patient', string='Пацієнти')
    start_date = fields.Date(string='Початок періоду')
    end_date = fields.Date(string='Кінець періоду')
    done_only = fields.Boolean(string='Лише завершені візити')
    disease_id = fields.Many2one('hr.hospital.disease', string='Хвороба')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')

        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        elif active_model == 'hr.hospital.patient' and active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_generate_report(self):
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
            'name': 'Звіт по візитах',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
