# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AcruxChatConversation(models.Model):
    _inherit = 'acrux.chat.conversation'

    tag_ids = fields.Many2many('acrux.chat.conversation.tag', string='Tags')
    note = fields.Text('Note')

    @api.model
    def get_fields_to_read(self):
        out = super().get_fields_to_read()
        out.extend(['tag_ids', 'note'])
        return out

    def build_dict(self, limit, offset=0):
        out = super().build_dict(limit, offset)
        Tags = self.env['acrux.chat.conversation.tag']
        for record in out:
            if record['tag_ids']:
                record['tag_ids'] = Tags.browse(record['tag_ids']).read(['id', 'name', 'color'])
        return out

    def delegate_conversation(self):
        conv_delete_ids = self.read(['id', 'agent_id'])
        self.set_to_new()
        notifications = []
        notifications.append((self[0].get_channel_to_many(), 'delete_taken_conversation', conv_delete_ids))
        notifications.append((self[0].get_channel_to_many(), 'delete_conversation', conv_delete_ids))
        notifications.append((self[0].get_channel_to_many(), 'new_messages', self.build_dict(22)))
        self._sendmany(notifications)
