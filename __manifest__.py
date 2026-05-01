{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Module for hospital automation',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'data/disease_data.xml',
        'data/doctor_category_data.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/doctor_category_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'demo/demo_data.xml',
        'wizard/reassign_doctor_wizard_views.xml',
        'wizard/visit_report_wizard_views.xml',

    ],
    'demo': [
        'demo/doctor_history_demo.xml',
    ],
    'installable': True,
    'auto_install': False,

}