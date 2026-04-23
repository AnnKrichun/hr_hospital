{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Module for hospital automation',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'data/disease_data.xml',
        
        'data/demo_data.xml',

        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/menu.xml',

    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,

}