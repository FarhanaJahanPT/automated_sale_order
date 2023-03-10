from odoo import models, fields, api


class AutoSaleOrder(models.Model):
    _name = 'auto.sale'
    _description = 'Automatic Sale Order'

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    product_uom_qty = fields.Float(string='Total Quantity', default=1)
    price_unit = fields.Float(string='Unit Price')
    product_id = fields.Many2one('product.product')

    def default_get(self, fields):
        print(fields,'aaaa')
        res = super(AutoSaleOrder, self).default_get(fields)
        print(res,'bbbb')
        print(self._context.get)
        res['product_id'] = self._context.get('product_id')
        print(self._context.get('price_unit'))
        res['price_unit'] = self._context.get('price_unit')
        return res

    def action_sale_conform(self):

        print('ccc')
        print(self.product_id.id)
        print(self.product_uom_qty)

        search = self.env['sale.order'].search([('state', '=', 'draft'), ('partner_id', '=', self.customer_id.id)])

        print(search, 'dd')
        print(self.product_id)
        if search:

            print('in search', search)

            for order in search:
                order.write({
                    'order_line': [(0, 0, {
                        'product_id': self.product_id.id,
                        'product_uom_qty': self.product_uom_qty,
                        'price_unit': self.price_unit
                    })]
                })
                print(self.price_unit, self.product_id)


        else:
            self.env['sale.order'].create({
                'order_line': [(0, 0, {
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.product_uom_qty,
                    'price_unit': self.price_unit
                })]
            })

    def action_cancel(self):
        print('bb')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    auto_sale_id = fields.Many2one('auto.sale')

    def merge_duplicate_product_lines(self, res):

        for line in res.order_line:
            if line.id in res.order_line.ids:
                line_ids = res.order_line.filtered(lambda m: m.product_id.id == line.product_id.id)

        quantity = 0
        price = 0
        for qty in line_ids:
            quantity += qty.product_uom_qty
            price = qty.price_unit
        line_ids[0].write({'product_uom_qty': quantity,
                           'price_unit': price})
        line_ids[1:].unlink()

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.merge_duplicate_product_lines(res)

        return res

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self.merge_duplicate_product_lines(self)
        return res
