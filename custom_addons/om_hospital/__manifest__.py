{
    "name": "Hospital Management",
    "version": "1.0.0",
    "category": "Hospital",
    "author": "AbdElrhman.M.Shata",
    "summary": "Hospital Management is currently unavailable and will be updated soon in the future",
    "description": """ Hospital Management System """,
    "depends": ["mail", "product"],
    "data": [
        "security/ir.model.access.csv",
        
        "data/patient_tag_data.xml",
        "data/patient.tag.csv",
        "data/sequence_data.xml",
        
        "wizard/cancel_appointment_view.xml",
        
        "views/menu.xml",
        "views/patient_view.xml",
        "views/male_patient_view.xml",
        "views/appoinment_view.xml",
        "views/operation_view.xml",
        "views/patient_tag_view.xml",
        "views/odoo_playground_view.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [],
    "sequence": -100,
    "application": True,
    # 'installable': True,
    "auto_install": False,
    "license": "LGPL-3",
}
