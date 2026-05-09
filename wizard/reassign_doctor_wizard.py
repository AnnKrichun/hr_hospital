from odoo import models, fields


class MassReassignDoctorWizard(models.TransientModel):
    """
    Wizard for mass reassigning doctors to patients.
    Fixes the issue where change_date was not used.
    """
    _name = 'hr.hospital.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='New Doctor',
        required=True,
        domain=[('is_intern', '=', False)]
    )

    # Поле тепер використовується (вимога викладача)
    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.today,
        required=True
    )

    def action_reassign(self):
        """
        Updates the patient's doctor and creates a history record using change_date.
        """
        self.ensure_one()
        patient_ids = self.env.context.get('active_ids')
        patients = self.env['hr.hospital.patient'].browse(patient_ids)

        for patient in patients:
            # Створюємо запис в історію, використовуючи change_date
            self.env['hr.hospital.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.new_doctor_id.id,
                'appointment_date': self.change_date,
            })
            # Оновлюємо лікаря
            patient.personal_doctor_id = self.new_doctor_id

        return {'type': 'ir.actions.act_window_close'}
