from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DoctorHistory(models.Model):
    """
    Model for tracking the history of personal doctors assigned to patients.
    """
    _name = 'hr.hospital.doctor.history'
    _description = 'Personal Doctor History'

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True
    )
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True
    )
    appointment_date = fields.Date(
        string='Appointment Date',
        required=True,
        default=fields.Date.context_today,
        help="Date when the doctor was assigned to the patient"
    )
    change_date = fields.Date(
        string='Change Date',
        help="Date when the doctor was changed or reassigned"
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )

    def _compute_display_name(self):
        """
        Generates a descriptive name for the history record.
        Example: John Doe - Dr. Smith (Specialist) 2024-05-08
        """
        for rec in self:
            category = rec.doctor_id.category_id.name or _('No category')
            rec.display_name = (
                f"{rec.patient_id.name} - {rec.doctor_id.name} "
                f"({category}) {rec.appointment_date}"
            )

    @api.onchange('appointment_date', 'change_date')
    def _onchange_dates(self):
        """
        Provides a real-time warning if the change date is before the appointment date.
        """
        if self.appointment_date and self.change_date:
            if self.change_date < self.appointment_date:
                return {
                    'warning': {
                        'title': _("Date Error"),
                        'message': _("The change date cannot be earlier than the appointment date.")
                    }
                }

    @api.constrains('appointment_date', 'change_date')
    def _check_dates_constrains(self):
        """
        Server-side validation to ensure date logical consistency.
        """
        for record in self:
            if record.appointment_date and record.change_date:
                if record.change_date < record.appointment_date:
                    raise ValidationError(_(
                        "The change date cannot be earlier than the appointment date."
                    ))
