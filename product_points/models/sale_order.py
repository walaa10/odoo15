from odoo import models, fields, api
from datetime import date


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    total_points = fields.Float('Total Points', store=True, compute='compute_total_points')

    @api.depends('order_line.product_points')
    def compute_total_points(self):
        self.total_points = sum((self.order_line.filtered(lambda x: x.product_points)).mapped('product_points'))


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_points = fields.Float('Product Points')

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_product_id(self):
        if self.product_id and self.product_uom_qty:
            self.product_points = sum(self.env['product.points'].search([
                ('product_id', '=', self.product_id.id), ('state', '=', 'confirmed'),
            ]).mapped('points')) * self.product_uom_qty
        else:
            self.product_points = 0.0
