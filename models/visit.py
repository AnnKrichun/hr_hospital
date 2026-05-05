from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _rec_name = 'patient_id'

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hr.hospital.visit') or 'New'
            if vals.get('state') == 'done' and not vals.get('visit_date'):
                vals['visit_date'] = fields.Datetime.now()
        return super(HospitalVisit, self).create(vals_list)

    def write(self, vals):
        if vals.get('state') == 'done':
            for rec in self:
                if not rec.visit_date and 'visit_date' not in vals:
                    rec.visit_date = fields.Datetime.now()

        for rec in self:
            if rec.state == 'done':
                forbidden = ['planned_date', 'visit_date', 'personal_doctor_id', 'patient_id']
                if any(field in vals for field in forbidden):
                    raise ValidationError("Не можна змінювати основні дані у завершеному візиті!")
        return super().write(vals)

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

    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
            if not rec.visit_date:
                rec.visit_date = fields.Datetime.now()

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_draft(self):
        for rec in self:
            rec.state = 'planned'
