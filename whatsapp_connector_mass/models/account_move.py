# -*- coding: utf-8 -*-
from odoo import models


# only O15
class AccountMove(models.Model):
    _inherit = 'account.move'
    _mailing_enabled = True

    def _mailing_get_default_domain(self, mailing):
        return [('state', '!=', 'cancel'), '|', '|', '|',
                ('move_type', '=', 'out_invoice'),
                ('move_type', '=', 'out_refund'),
                ('move_type', '=', 'in_invoice'),
                ('move_type', '=','in_refund')]
