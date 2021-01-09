from odoo import models, api, fields, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

from datetime import datetime


class StockClosePrint(models.TransientModel):
    _name = 'stock.close.print.wizard'

    close_name = fields.Many2one(comodel_name='stock.close.period',
                                 string=_('Close Period'))


    @api.multi
    def generate_report(self):

        rows = self.env['stock.close.period.line'].search([(
            'close_id', '=', self.close_name.id
        )], order='product_code')
        datas = {
            'ids': rows.ids,
            'model': 'stock.close.period.line',
            'form': {
                'close_name': self.close_name.name,
            }
        }

        return self.env.ref('stock_close_period.report_xlsx_stock_close_print').report_action(self, data=datas, config=False)
