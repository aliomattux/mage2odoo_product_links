from openerp.osv import osv, fields

class MageSetup(osv.osv):
    _inherit = 'mage.setup'
    _columns = {
	'import_links_with_products': fields.boolean('Import Links with Products'),
    }
