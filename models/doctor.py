from odoo import models, fields,api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Спеціалізація')

    category_id = fields.Many2one('hr.hospital.doctor.category', string='Категорія')
    user_id = fields.Many2one('res.users', string='Користувач системи')

    is_intern = fields.Boolean(string='Лікар є інтерном', compute='_compute_is_intern', store=True)
    mentor_id = fields.Many2one('hr.hospital.doctor', string='Ментор',
                                domain=[('is_intern', '=', False)])  # Обмеження на вибір у формі

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

