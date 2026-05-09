from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'display_name'

    name = fields.Char(string='Disease Name', required=True,
        help="Enter the name of the disease")
    description = fields.Text(string='Description',
        help="Full description of the disease")
    active = fields.Boolean(default=True, string='Active')

    parent_id = fields.Many2one('hr.hospital.disease', string='Parent Category', ondelete='cascade', index=True)
    parent_path = fields.Char(index=True)

    display_name = fields.Char(
        string='Full Name',
        compute='_compute_display_name',
        recursive=True,
        store=True
    )

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for rec in self:
            if rec.parent_id:
                rec.display_name = f"{rec.parent_id.display_name} / {rec.name}"
            else:
                rec.display_name = rec.name

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if self._has_cycle():
            raise ValidationError('Error! You cannot create a recursive hierarchy.')
