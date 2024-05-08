{
    'name': 'Student Registration',
    'version': '1.0',
    'depends': ['sale'],
    'author': 'shubham',
    'category': 'General',
    'sequence': -10,
    'description': """ Add registration data and make archive and unarchive record and test it's visible in tree view or not""",
    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
    ],


    'installable': True,
    'application': True,

}
