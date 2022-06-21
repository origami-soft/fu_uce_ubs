# -*- coding: utf-8 -*-
from odoo import models
import traceback
import logging
_logger = logging.getLogger(__name__)


class AcruxChatConversation(models.Model):
    _inherit = 'acrux.chat.conversation'

    def get_to_current(self):
        out = super(AcruxChatConversation, self).get_to_current()
        self.env['acrux.chat.bot'].bot_clean(self.id)
        return out

    def new_message_hook(self, message_id, limit, data, last_sent):
        limit, send_bus = super(AcruxChatConversation, self).new_message_hook(message_id, limit, data, last_sent)
        if message_id.contact_id.status != 'current':
            rollback = False
            try:
                messages = self.env['acrux.chat.bot']._bot_get(message_id)
                for mess in messages:
                    rollback = True
                    self.env.cr.commit()  # commit time
                    message_id.contact_id.send_message(mess, check_access=False)
                    limit += 1
            except Exception as e:
                if rollback:
                    self.env.cr.rollback()
                _logger.warning("BOT error: %s" % self)
                _logger.exception(e)
                self.env['acrux.chat.bot.log'].sudo().create({
                    'conversation_id': message_id.contact_id.id,
                    'text': message_id.text,
                    'bot_log': traceback.format_exc(),
                })

        return limit, send_bus

    def search_partner_bot(self, domain=False):
        self.ensure_one()
        ResPartner = self.env['res.partner']
        if not domain:
            domain = [('company_id', 'in', [self.connector_id.company_id.id, False]),
                      ('conv_standard_numbers', 'like', self.number)]
        return ResPartner.search(domain)
