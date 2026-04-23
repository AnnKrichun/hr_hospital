from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease Type'

    name = fields.Char(
        string='Назва захворювання',
        required=True,
        help="Введіть офіційну назву хвороби"
    )

    description = fields.Text(
        string='Опис',
        help="Додаткова інформація про симптоми або характер перебігу"
    )


    active = fields.Boolean(
        default=True,
        string='Активно'
    )
