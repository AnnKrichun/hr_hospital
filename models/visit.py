from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalVisit(models.Model):
    """
    Model representing patient visits to doctors.
    Includes validation for finished visits and automatic sequencing.
    """
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _rec_name = 'patient_id'

    name = fields.Char(
        string='Visit Number',
        readonly=True,
        copy=False,
        default='New'
    )

    state = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='planned', required=True, tracking=True)

    planned_date = fields.Datetime(
        string='Planned Date',
        required=True,
        help="Scheduled date and time for the doctor's appointment"
    )

    visit_date = fields.Datetime(
        string='Actual Visit Date',
        help="Actual date and time when the visit occurred"
    )

    personal_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True,
        tracking=True
    )

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True,
        tracking=True
    )

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Disease'
    )

    summary = fields.Html(
        string='Summary',
        help="Final diagnosis or medical conclusion"
    )

    treatment_notes = fields.Text(
        string='Treatment Recommendations'
    )

    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Generates visit number and sets actual date if created as 'done'."""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hr.hospital.visit') or 'New'
            if vals.get('state') == 'done' and not vals.get('visit_date'):
                vals['visit_date'] = fields.Datetime.now()
        return super(HospitalVisit, self).create(vals_list)

    def write(self, vals):
        """Prevents modifying critical data in completed visits."""
        if vals.get('state') == 'done':
            for rec in self:
                if not rec.visit_date and 'visit_date' not in vals:
                    rec.visit_date = fields.Datetime.now()

        for rec in self:
            if rec.state == 'done':
                forbidden = ['planned_date', 'visit_date', 'personal_doctor_id', 'patient_id']
                if any(field in vals for field in forbidden):
                    raise ValidationError(_("You cannot modify core data in a completed visit!"))
        return super().write(vals)

    def unlink(self):
        """Restricts deletion of completed visits."""
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_("Deletion of completed visits is prohibited!"))
        return super(HospitalVisit, self).unlink()

    @api.constrains('active')
    def _check_archive_done(self):
        """Prevents archiving visits that are already finished."""
        for rec in self:
            if rec.state == 'done' and not rec.active:
                raise ValidationError(_("Archiving of completed visits is prohibited!"))

    def action_done(self):
        """Sets visit status to 'Done' and records the actual timestamp."""
        for rec in self:
            rec.state = 'done'
            if not rec.visit_date:
                rec.visit_date = fields.Datetime.now()

    def action_cancel(self):
        """Sets visit status to 'Cancelled'."""
        self.write({'state': 'cancelled'})

    def action_draft(self):
        """Resets visit to 'Planned' status."""
        self.write({'state': 'planned'})
