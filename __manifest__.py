{
    'name': 'Hospital Management',
    'version': '1.1',
    'category': 'Human Resources',
    'summary': 'Module for hospital automation',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/disease_data.xml',
        'data/doctor_category_data.xml',
        'data/sequence.xml',
        'demo/demo_data.xml',
        'demo/doctor_history_demo.xml',
        'demo/doctor_demo.xml',
        'demo/disease_demo.xml',
        'views/menu.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/doctor_category_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'wizard/reassign_doctor_wizard_views.xml',
        'wizard/visit_report_wizard_views.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,


}