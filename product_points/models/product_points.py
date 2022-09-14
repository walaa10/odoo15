from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class ProductPoints(models.Model):
    _name = 'product.points'
    _description = 'Product Points'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Product', required=True, domain="[('sale_ok', '=', True)]")
    start_date = fields.Date('Start Date', default=fields.Date.today())
    end_date = fields.Date('End Date')
    points = fields.Float('Points')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    Last_change_status_by = fields.Many2one('res.users', 'Last Stage Updated By', default=lambda self: self.env.user)

    def write(self, vals):
        if vals.get('state'):
            vals.update({
                'Last_change_status_by': self.env.user.id
            })
        return super(ProductPoints, self).write(vals)

    @api.onchange('start_date')
    def onchange_start_date(self):
        if self.start_date:
            self.end_date = False

    @api.constrains('end_date')
    def end_date_constrains(self):
        for rec in self:
            if rec.end_date and rec.start_date > rec.end_date:
                raise ValidationError('End date must be greater than start date')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'

    def action_end(self):
        self.state = 'ended'

    def check_end_date(self):
        product_points = self.env['product.points'].search([('state', 'not in', ['ended', 'cancelled']),
                                                            ('end_date', '=', date.today())])
        for rec in product_points:
            rec.action_end()
