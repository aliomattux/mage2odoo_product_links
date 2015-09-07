#Module designed not copy/pasted but basically looked at and written from
#OCA product links module If you want clearer copyright, contact me

from openerp.osv import osv, fields

class ProductLink(osv.osv):
    _name = 'product.link'

#    @api.model
 #   def get_link_type_selection(self):
  #      # selection can be inherited and extended
   #     return [('cross_sell', 'Cross-Sell'),
    #            ('up_sell', 'Up-Sell'),
     #           ('related', 'Related')]

    _columns = {
	'product_tmpl_id': fields.many2one('product.template', 'Parent Product'),
	'linked_product': fields.many2one('product.product', 'Linked Product'),
	'link_type': fields.selection([('cross_sell', 'Cross-Sell'),
                ('up_sell', 'Up-Sell'),
                ('related', 'Related')], 'Link Type'),
    
    }



class ProductTemplate(osv.osv):
    _inherit = 'product.template'
    _columns = {
	'product_links': fields.one2many('product.link', 'product_tmpl_id', 'Product Links'),
    }
