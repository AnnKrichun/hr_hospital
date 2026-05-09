from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    """
    Model representing medical doctors within the hospital system.
    """
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Hospital Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Specialization', help="Doctor's medical field")

    image_1920 = fields.Image(string="Doctor's Photo", max_width=1024, max_height=1024)
    image_128 = fields.Image(
        string="Photo (128x128)",
        related="image_1920",
        max_width=128,
        max_height=128,
        store=True
    )

    category_id = fields.Many2one(
        'hr.hospital.doctor.category',
        string='Category')

    user_id = fields.Many2one('res.users', string='System User')

    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='personal_doctor_id',
        string='Visits'
    )
    is_intern = fields.Boolean(
        string='Is Intern',
        compute='_compute_is_intern',
        store=True
    )
    mentor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)],
        help="Senior doctor who mentors the intern"
    )

    intern_ids = fields.One2many(
        'hr.hospital.doctor',
        'mentor_id',
        string='Interns')

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            'hr_hospital.doctor_category_intern',
            raise_if_not_found=False)
        for rec in self:
            rec.is_intern = (rec.category_id == intern_category)

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError(_("A mentor cannot be an intern!"))
            if rec.mentor_id == rec:
                raise ValidationError(_("A doctor cannot be their own mentor!"))

    def action_create_appointment(self):
        """
        Opens a wizard-like form to quickly record a patient visit.
        """
        self.ensure_one()
        return {
            'name': _('Quick Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_personal_doctor_id': self.id,
                'default_planned_date': fields.Datetime.now(),
            }
        }
