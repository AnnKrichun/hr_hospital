from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    name = fields.Char(
        string='Номер візиту',
        readonly=True,
        copy=False,
        default='New'
    )

    state = fields.Selection([
        ('planned', 'Заплановано'),
        ('done', 'Завершено'),
        ('cancelled', 'Скасовано')
    ], string='Статус візиту', default='planned', required=True)

    planned_date = fields.Datetime(
        string='Запланована дата та час',
        required=True,
        help="Для відображення графіку прийому лікарів"
    )

    visit_date = fields.Datetime(
        string='Дата та час візиту (факт)',
        default=fields.Datetime.now
    )

    personal_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Лікар',
        required=True
    )

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Пацієнт',
        required=True
    )

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Хвороба'
    )

    summary = fields.Html(
        string='Епікриз / Summary'
    )

    treatment_notes = fields.Text(
        string='Рекомендації щодо лікування'
    )

    active = fields.Boolean(default=True)

    def write(self, vals):
        for rec in self:
            if rec.state == 'done':
                forbidden_fields = ['planned_date', 'visit_date', 'personal_doctor_id', 'patient_id']
                if any(field in vals for field in forbidden_fields):
                    raise ValidationError("Не можна змінювати дату, лікаря або пацієнта у завершеному візиті!")
        return super(HospitalVisit, self).write(vals)

    def unlink(self):
        for rec in self:
           if rec.state == 'done':
               raise ValidationError("Заборонено видаляти завершені візити!")
        return super(HospitalVisit, self).unlink()

    @api.constrains('active')
    def _check_archive_done(self):
        for rec in self:
            if rec.state == 'done' and not rec.active:
                raise ValidationError("Заборонено архівувати завершені візити!")
