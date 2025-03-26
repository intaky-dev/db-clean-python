from odoo import models
import logging

_logger = logging.getLogger(__name__)

class LimpiarBaseWizard(models.TransientModel):
    _name = 'limpieza.base.wizard'
    _description = 'Limpiar Ventas, Compras y Stock'

    def limpiar_base(self):
        env = self.env

        try:
            # Limpieza total por SQL directo (ampliado)
            env.cr.execute("DELETE FROM sale_order_option")
            env.cr.execute("DELETE FROM sale_order_line")
            env.cr.execute("DELETE FROM sale_order")
            env.cr.execute("DELETE FROM stock_move_line")
            env.cr.execute("DELETE FROM stock_move")
            env.cr.execute("DELETE FROM stock_picking")
            env.cr.execute("DELETE FROM stock_valuation_layer")
            env.cr.execute("DELETE FROM stock_production_lot")
            env.cr.execute("DELETE FROM stock_tracking")
            env.cr.execute("DELETE FROM stock_quant_package")
            env.cr.execute("DELETE FROM purchase_order_line")
            env.cr.execute("DELETE FROM purchase_order")
            env.cr.execute("DELETE FROM pos_payment")
            env.cr.execute("DELETE FROM pos_order_invoice_rel")
            env.cr.execute("DELETE FROM pos_order_line")
            env.cr.execute("DELETE FROM pos_order")
            env.cr.execute("DELETE FROM pos_session")
            env.cr.execute("DELETE FROM account_payment")
            env.cr.execute("DELETE FROM account_bank_statement_line")
            env.cr.execute("DELETE FROM account_bank_statement")
            env.cr.execute("DELETE FROM account_partial_reconcile")
            env.cr.execute("DELETE FROM account_analytic_line")
            env.cr.execute("DELETE FROM account_tax_cash_basis_transition")
            env.cr.execute("DELETE FROM account_move_line")
            env.cr.execute("DELETE FROM account_move")
            env.cr.execute("DELETE FROM stock_quant")
        except Exception as e:
            _logger.error(f'Error durante limpieza total por SQL: {e}')

        return {'type': 'ir.actions.act_window_close'}
