# -*- coding: utf-8 -*-
{
    "name": "om_inheritence",
    "summary": "",
    "description": "",
    "author": "Odoo Mates",
    "website": "http://www.yourcompany.com",
    "version": "0.1",
    "depends": ["sale", "sale_stock", "mail"],
    "data": [
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "views/partner_category_view.xml",
    ],
    "demo": [],
    "sequence": -100,
    "application": True,
    # 'installable': True,
    "auto_install": False,
    "license": "LGPL-3",
}
