from odoo import models, fields, api


class AutomatedSaleOrder(models.Model):
    _inherit = 'product.product'

    sale_count = fields.Integer(compute='compute_count')

    def automated_sale_order(self):
        return {
            'name': "Automatic Sale Order",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'auto.sale',
            'view_id': self.env.ref('automated_sale_order.auto_sale_view_form').id,
            'target': 'new',
            'context': {'product_id': self.id,
                        'price_unit': self.lst_price}
        }

    def get_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('order_line.product_id', '=', self.product_tmpl_id.name)],
            'context': [('create', '=', False)],
        }

    def compute_count(self):
        for record in self:
            record.sale_count = self.env['sale.order'].search_count(
                [('order_line.product_id', '=', self.ids)])
