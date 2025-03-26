from odoo import models
import logging

_logger = logging.getLogger(__name__)

class LimpiarBaseWizard(models.TransientModel):
    _name = 'limpieza.base.wizard'
    _description = 'Limpiar Ventas, Compras y Stock'

    def limpiar_base(self):
        env = self.env

        try:
            # Limpieza total por SQL directo (FULL SQL MODE 🔥)
            env.cr.execute("DELETE FROM sale_order_line")
            env.cr.execute("DELETE FROM sale_order")
            env.cr.execute("DELETE FROM stock_move_line")
            env.cr.execute("DELETE FROM stock_move")
            env.cr.execute("DELETE FROM stock_picking")
            env.cr.execute("DELETE FROM stock_inventory_line")
            env.cr.execute("DELETE FROM stock_inventory")
            env.cr.execute("DELETE FROM purchase_order_line")
            env.cr.execute("DELETE FROM purchase_order")
            env.cr.execute("DELETE FROM pos_order_line")
            env.cr.execute("DELETE FROM pos_order")
            env.cr.execute("DELETE FROM account_move_line")
            env.cr.execute("DELETE FROM account_move")
            env.cr.execute("DELETE FROM stock_quant")
        except Exception as e:
            _logger.error(f'Error durante limpieza total por SQL: {e}')

        return {'type': 'ir.actions.act_window_close'}
