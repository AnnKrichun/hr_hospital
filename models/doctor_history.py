from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DoctorHistory(models.Model):
    _name = 'hr.hospital.doctor.history'
    _description = 'Історія персональних лікарів'

    patient_id = fields.Many2one('hr.hospital.patient', string='Пацієнт', required=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Лікар', required=True)
    appointment_date = fields.Date(
        string='Дата призначення',
        required=True,
        default=fields.Date.context_today
    )
    change_date = fields.Date(string='Дата зміни лікаря')
    active = fields.Boolean(string='Активний', default=True)

    def _compute_display_name(self):
        for rec in self:
            category = rec.doctor_id.category_id.name or _('Без категорії')
            rec.display_name = f"{rec.patient_id.name} - {rec.doctor_id.name} ({category}) {rec.appointment_date}"

    @api.onchange('appointment_date', 'change_date')
    def _onchange_dates(self):
        if self.appointment_date and self.change_date:
            if self.change_date < self.appointment_date:
                return {
                    'warning': {
                        'title': _("Помилка дати"),
                        'message': _("Дата зміни лікаря не може бути раніше ніж дата призначення")
                    }
                }

    @api.constrains('appointment_date', 'change_date')
    def _check_dates_constrains(self):
        for record in self:
            if record.appointment_date and record.change_date:
                if record.change_date < record.appointment_date:
                    raise ValidationError(_("Дата зміни лікаря не може бути раніше ніж дата призначення"))
