from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class MedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Медична інформація'

    blood_type = fields.Selection([
        ('o_plus', 'O(I)+'), ('o_minus', 'O(I)-'),
        ('a_plus', 'A(II)+'), ('a_minus', 'A(II)-'),
        ('b_plus', 'B(III)+'), ('b_minus', 'B(III)-'),
        ('ab_plus', 'AB(IV)+'), ('ab_minus', 'AB(IV)-'),
    ], string='Група крові')

    gender = fields.Selection([
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
    ], string='Стать')

    birthday = fields.Date(string='Дата народження')

    age = fields.Integer(
        string='Вік',
        compute='_compute_age',
        store=False
        )

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birthday:
                birth_date = fields.Date.from_string(rec.birthday)
                rec.age = today.year - birth_date.year - (
                        (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                rec.age = 0
