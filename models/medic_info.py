from odoo import models, fields, api
from datetime import date

class MedicInfo(models.AbstractModel):
    """
    Abstract model for common medical information.
    Used as a base for doctors and patients.
    """
    _name = 'hr.hospital.medic.info'
    _description = 'Medical Information'

    blood_type = fields.Selection([
        ('o_plus', 'O(I)+'), ('o_minus', 'O(I)-'),
        ('a_plus', 'A(II)+'), ('a_minus', 'A(II)-'),
        ('b_plus', 'B(III)+'), ('b_minus', 'B(III)-'),
        ('ab_plus', 'AB(IV)+'), ('ab_minus', 'AB(IV)-'),
    ], string='Blood Type')

    gender = fields.Selection([
        ('man', 'Man'),
        ('woman', 'Woman'),
    ], string='Gender')

    birthday = fields.Date(string='Date of Birth')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        help="Automatically calculated age based on the birthday"
    )

    @api.depends('birthday')
    def _compute_age(self):
        """Calculates the current age based on the birth date."""
        today = date.today()
        for rec in self:
            if rec.birthday:
                birth_date = fields.Date.from_string(rec.birthday)
                rec.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                rec.age = 0
