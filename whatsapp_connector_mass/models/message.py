# -*- coding: utf-8 -*-

from odoo import models, fields


class AcruxChatMessages(models.Model):
    _inherit = 'acrux.chat.message'

    mailing_id = fields.Many2one('mailing.mailing', 'Marketing', ondelete='set null')
    # should be just one
    mailing_trace_ids = fields.One2many('mailing.trace', 'ws_message_id',
                                        string='Trace')
    mailing_res_id = fields.Integer()

    def message_send(self):
        '''
            :override
            Set mailing trace to sent state.
        '''
        out = super(AcruxChatMessages, self).message_send()
        if out:
            self.mailing_trace_ids.write({'trace_status': 'sent',
                                          'sent_datetime': fields.Datetime.now()})
        return out
