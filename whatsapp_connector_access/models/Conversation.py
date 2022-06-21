# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression


class Conversation(models.Model):
    _inherit = 'acrux.chat.conversation'

    access_team_id = fields.Many2one('crm.team', string='CRM Team Access',
                                     domain="[('company_id', 'in', [company_id, False])]",
                                     ondelete='set null')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        domain = self.get_access_agent(args)
        if domain:
            args = expression.AND([domain, args]) if args else domain
        return super(Conversation, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                 access_rights_uid=access_rights_uid)

    @api.model
    def get_access_agent(self, args):
        ret = []
        flag = [x for x in args if x[0] in ['id', 'access_team_id']] if args else False
        if not flag and self.env.user.has_group('whatsapp_connector_access.chat_access_crm_team'):
            domain = ['|', ('chatroom_user_ids', '=', False), ('chatroom_user_ids', 'in', [self.env.user.id])]
            team_ids = self.sudo().env['crm.team'].search_read(domain, ['id'])
            team_ids = [x['id'] for x in team_ids]
            if team_ids:
                ret = [('access_team_id', 'in', team_ids)]
            else:
                ret = [('access_team_id', '=', False)]
        return ret

    def parse_notification(self, datas):
        flag = [x for x in datas if x[1] == 'new_messages']
        if flag:
            member_ids = self.sudo().access_team_id.chatroom_user_ids.ids
            datas = self.check_members_ids(datas, member_ids, 'whatsapp_connector_access.chat_access_crm_team')
        return super(Conversation, self).parse_notification(datas)

    def check_members_ids(self, datas, member_ids, access_group):
        result = []
        users = self.sudo().env.ref('whatsapp_connector.group_chat_basic_extra').users.filtered('acrux_chat_active')
        for data in datas:
            if data[1] == 'new_messages':
                if 'private' in data[0]:
                    user_id = data[0][-1]
                    if user_id not in users.ids:
                        continue
                    if user_id not in member_ids:
                        user = users.filtered(lambda x: x.id == user_id)
                        if user.has_group(access_group):
                            continue
                    result.append(data)
                else:
                    not_members = [x for x in users if x.id not in member_ids]
                    if len(not_members) == 0:
                        result.append(data)
                        continue
                    for user in users:
                        if user.id not in member_ids and user.has_group(access_group):
                            continue
                        result.append([self.get_channel_to_one(user_id=user), data[1], data[2]])
            else:
                result.append(data)
        return result
