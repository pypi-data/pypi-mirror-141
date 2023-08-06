from odoo import models, fields, _
import base64


class SendDeliveryNoteWizard(models.TransientModel):
    _name = 'send.delivery.note.wizard'
    _description = 'Send delivery note list by email'

    stock_picking_batch_id = fields.Many2one('stock.picking.batch')

    def send_mail(self):
        report = self.env.ref(
            'biba_ardoak.action_report_picking_batch_delivery_note'
        )
        picking_ids = self.env.context['active_ids']
        report_binary = report._render_qweb_pdf(picking_ids)
        email_to = self.env['ir.config_parameter'].get_param(
            'biba_ardoak.storehouse_email'
        )
        pdf = base64.encodebytes(report_binary[0])
        email_values = {
            'email_to': email_to,
            'attachments': [[_('Delivery Note'), pdf]]
        }
        template_id = self.env.ref(
            'biba_ardoak.delivery_note_mail_template_tree_view'
        ).id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(
            picking_ids[0], email_values=email_values, force_send=True
        )

    def send_mail(self):
        report = self.env.ref(
            'stock.action_report_delivery'
        )
        picking_ids = self.env.context['active_ids']
        report_binary = report._render_qweb_pdf(picking_ids)
        email_to = self.env['ir.config_parameter'].get_param(
            'biba_ardoak.storehouse_email'
        )
        pdf = base64.encodebytes(report_binary[0])
        email_values = {
            'email_to': email_to,
            'attachments': [[_('Delivery Note'), pdf]]
        }
        template_id = self.env.ref(
            'biba_ardoak.delivery_note_mail_template_form_view'
        ).id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(
            picking_ids[0], email_values=email_values, force_send=True
        )
