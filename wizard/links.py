from openerp.osv import osv, fields
from openerp.tools.translate import _

class MageSaleOrderLinkLine(osv.osv_memory):
    _name = 'mage.sale.order.link'
    _columns = {
	'product': fields.many2one('product.product', 'Product'),
	'sale_order_line': fields.many2one('sale.order.line', 'Sale Line'),
	'lines': fields.one2many('mage.sale.order.link.line', 'parent', 'Details'),
    }

    def default_get(self, cr, uid, fields, context=None):
	line_id = context.get('active_id')
	line = self.pool.get('sale.order.line').browse(cr, uid, line_id)
	product = line.product_id
	sale_id = line.order_id.id
	res = []
	for link in product.product_links:
	    res.append({'product': link.linked_product.id,
		'link_type': link.link_type,
	    })

	return {'product': product.id, 'sale_order_line': line_id, 'lines': res}

    def add_items_to_sale(self, cr, uid, ids, context=None):
	wizard = self.browse(cr, uid, ids[0])
	line_obj = self.pool.get('sale.order.line')
	sale_line = wizard.sale_order_line
	for line in wizard.lines:
	    if line.add:
		vals = {
			'product_id': line.product.id,
			'order_id': sale_line.order_id.id,
			'product_uos_qty': line.quantity,
			'product_uom_qty': line.quantity,
		}
		new_line = line_obj.create(cr, uid, vals)
		print 'ID', new_line
#		onchange_vals = line_obj.product_id_change(sale_line.order_id.pricelist_id.id, line.product.id, line.quantity, False, line.quantity, False, line.product.name, sale_line.order_id.partner_id.id, False, True, sale_line.order_id.date_order, False, sale_line.order_id.fiscal_position, False)
#		print 'Onchange Vals', onchange_vals

        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
        view_id = view_ref and view_ref[1] or False,

        return {
            'type': 'ir.actions.act_window',
            'name': _('Sale Order'),
            'res_model': 'sale.order',
            'context': {},
            'res_id': sale_line.order_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }


class MageSaleOrderLinkLine(osv.osv_memory):
    _name = 'mage.sale.order.link.line'
    _columns = {
	'parent': fields.many2one('mage.sale.order.link', 'Parent'),
        'product': fields.many2one('product.product', 'Product'),
        'quantity': fields.float('Quantity'),
	'add': fields.boolean('Add'),
        'link_type': fields.selection([('cross_sell', 'Cross-Sell'),
                ('up_sell', 'Up-Sell'),
                ('related', 'Related')], 'Link Type'),
    }
