from odoo import models

class LimpiarBaseWizard(models.TransientModel):
    _name = 'limpieza.base.wizard'
    _description = 'Limpiar Ventas, Compras y Stock'

    def limpiar_base(self):
        env = self.env

        # Ventas
        ventas = env['sale.order'].search([])
        for v in ventas:
            # Prevenir errores al eliminar líneas: setear cantidades en 0
            for line in v.order_line:
                line.product_uom_qty = 0
                line.qty_delivered = 0
                line.qty_invoiced = 0

            if v.state != 'cancel':
                v.action_cancel()
            v.unlink()

        # Compras
        compras = env['purchase.order'].search([])
        for c in compras:
            if c.state != 'cancel':
                c.button_cancel()
            c.unlink()

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
            if order.picking_id and order.picking_id.state not in ('done', 'cancel'):
                order.picking_id.button_cancel()
                order.picking_id.unlink()
            if order.account_move:
                order.account_move.button_cancel()
                order.account_move.unlink()
            order.unlink()

        return {'type': 'ir.actions.act_window_close'}

