from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DoctorCategory(models.Model):
    """
    Model for doctor qualification categories (e.g., Intern, Specialist, Professor).
    Used for filtering and classification logic.
    """
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Category'
    _order = 'sequence'

    name = fields.Char(
        string='Category Name',
        required=True,
        help="The name of the qualification level"
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Used to order categories in the interface"
    )

    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Doctors List'
    )

    @api.constrains('name')
    def _check_unique_name(self):
        """
        Ensures that each category has a unique name to avoid duplicates.
        """
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(_("Qualification with the name '%s' already exists!") % record.name)
