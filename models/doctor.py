from odoo import models, fields,api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Спеціалізація')

    image_1920 = fields.Image(string="Фото лікаря", max_width=1024, max_height=1024)
    image_128 = fields.Image(string="Фото (128x128)", related="image_1920", max_width=128, max_height=128, store=True)

    category_id = fields.Many2one('hr.hospital.doctor.category', string='Категорія')
    user_id = fields.Many2one('res.users', string='Користувач системи')

    is_intern = fields.Boolean(string='Лікар є інтерном', compute='_compute_is_intern', store=True)
    mentor_id = fields.Many2one('hr.hospital.doctor', string='Ментор',
                                domain=[('is_intern', '=', False)])  # Обмеження на вибір у формі

    intern_ids = fields.One2many('hr.hospital.doctor', 'mentor_id', string='Інтерни')

    @api.depends('category_id')
    def _compute_is_intern(self):
        for rec in self:
             rec.is_intern = rec.category_id and "інтерн" in rec.category_id.name.lower()

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError("Ментор не може бути інтерном!")
            if rec.mentor_id == rec:
                raise ValidationError("Лікар не може бути ментором самому собі!")

    def action_create_appointment(self):
        self.ensure_one()
        return {
            'name': 'Швидкий запис до лікаря',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_personal_doctor_id': self.id,
                'default_planned_date': fields.Datetime.now(),
            }
        }
