{
    'name': 'Hospital Management',
    'version': '1.1',
    'category': 'Human Resources',
    'summary': 'Module for hospital automation',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/doctor_category_data.xml',
        'data/disease_data.xml',
        'data/sequence.xml',
        'views/menu.xml',
        'views/doctor_category_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'demo/demo_data.xml',
        'demo/doctor_history_demo.xml',
        'demo/doctor_demo.xml',
        'demo/disease_demo.xml',
        'wizard/reassign_doctor_wizard_views.xml',
        'wizard/visit_report_wizard_views.xml',
        'wizard/disease_report_wizard_view.xml',
        'report/hr_hospital_doctor_reports.xml',
        'report/hr_hospital_doctor_templates.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'auto_install': False,


}