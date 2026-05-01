from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Кваліфікація лікарів'
    _order = 'sequence'

    name = fields.Char(string='Назва', required=True)
    sequence = fields.Integer(string='Послідовність', default=10)

    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Список лікарів'
    )

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError("Кваліфікація з назвою '%s' вже існує!" % record.name)
