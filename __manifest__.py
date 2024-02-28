{
    'name': "Heads Activities",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['mail', 'base','hr'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/heads_report.xml',
        'data/activity.xml',


    ],
    'summary': "heads_activities",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
