# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression


class Conversation(models.Model):
    _inherit = 'acrux.chat.conversation'

    access_helpdesk_team_id = fields.Many2one('helpdesk.team', string='HelpDesk Team Access',
                                              domain="[('company_id', 'in', [company_id, False])]",
                                              ondelete='set null')

    @api.model
    def get_access_agent(self, args):
        ret = super(Conversation, self).get_access_agent(args)
        flag = [x for x in args if x[0] in ['id', 'access_helpdesk_team_id']] if args else False
        if not flag and self.env.user.has_group('whatsapp_connector_access_helpdesk.chat_access_helpdesk_team'):
            domain = ['|', ('chatroom_user_ids', '=', False), ('chatroom_user_ids', 'in', [self.env.user.id])]
            team_ids = self.sudo().env['helpdesk.team'].search_read(domain, ['id'])
            team_ids = [x['id'] for x in team_ids]
            out = []
            if team_ids:
                out = [('access_helpdesk_team_id', 'in', team_ids)]
            else:
                out = [('access_helpdesk_team_id', '=', False)]
            if ret:
                ret = expression.AND([out, ret])
            else:
                ret = out
        return ret

    def parse_notification(self, datas):
        flag = [x for x in datas if x[1] == 'new_messages']
        if flag:
            member_ids = self.sudo().access_helpdesk_team_id.chatroom_user_ids.ids
            datas = self.check_members_ids(datas, member_ids,
                                           'whatsapp_connector_access_helpdesk.chat_access_helpdesk_team')
        return super(Conversation, self).parse_notification(datas)
