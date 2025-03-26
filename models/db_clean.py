from odoo import models
import logging

_logger = logging.getLogger(__name__)

class LimpiarBaseWizard(models.TransientModel):
    _name = 'limpieza.base.wizard'
    _description = 'Limpiar Ventas, Compras y Stock'

    def limpiar_base(self):
        env = self.env

        # Ventas
        try:
            # Cancelar órdenes primero por si hay restricciones activas
            env['sale.order'].search([('state', '!=', 'cancel')]).action_cancel()

            # Borrado forzado vía SQL (orden y líneas)
            env.cr.execute("DELETE FROM sale_order_line")
            env.cr.execute("DELETE FROM sale_order")
        except Exception as e:
            _logger.warning(f'Error al eliminar órdenes de venta por SQL: {e}')
                _logger.warning(f'No se pudo eliminar la orden {v.name}: {e}')

        # Compras
        compras = env['purchase.order'].search([])
        for c in compras:
            try:
                if c.state != 'cancel':
                    c.button_cancel()
                # Eliminar líneas de compra
                c.order_line.unlink()
                # Eliminar la orden de compra
                c.unlink()
            except Exception as e:
                _logger.warning(f'No se pudo eliminar la orden de compra {c.name}: {e}')

        # Ajustes de inventario
        ajustes = env['stock.inventory'].search([])
        ajustes.unlink()

        # Transferencias
        movimientos = env['stock.picking'].search([])
        for m in movimientos:
            if m.state not in ('cancel', 'done'):
                m.button_cancel()
            m.unlink()

        # Movimientos de stock huérfanos
        env['stock.move.line'].search([]).unlink()
        env['stock.move'].search([]).unlink()

        # Stock final
        env['stock.quant'].search([]).unlink()

        # Ventas desde PdV
        pos_orders = env['pos.order'].search([])
        for order in pos_orders:
            try:
                if order.picking_id and order.picking_id.state not in ('done', 'cancel'):
                    order.picking_id.button_cancel()
                    order.picking_id.unlink()
                if order.account_move:
                    order.account_move.button_cancel()
                    order.account_move.unlink()
                # Eliminar líneas de PdV
                order.lines.unlink()
                order.unlink()
            except Exception as e:
                _logger.warning(f'No se pudo eliminar la venta PdV {order.name}: {e}')

        return {'type': 'ir.actions.act_window_close'}
