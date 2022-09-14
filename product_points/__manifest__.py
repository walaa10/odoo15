# -*- coding: utf-8 -*-
{
    'name': "Product Points",
    'summary': """ Product Points """,
    'description': """
        This Module Add points to products in sale order lines 
        and add total points in sale order related to the sum of each product points 
    """,
    'author': "Walaa Mustafa",
    'version': '15.0',
    'depends': ['product', 'sale_management'],
    'data': [
        'security/product_point_group.xml',
        'security/product_points_rules.xml',
        'security/ir.model.access.csv',
        'views/product_points_menu.xml',
        'views/product_points_view.xml',
        'views/sale_order_view.xml',
        'data/product_point_data.xml',
        'report/product_point_template.xml',
        'report/report.xml',
    ],
}
