# This file is part of product_oneclick_training module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Bool
from trytond.model.fields import depends

__all__ = ['ProductOneClickView', 'ProductOneClick']
__metaclass__ = PoolMeta


class ProductOneClickView:
    __name__ = 'product.oneclick.view'
    training = fields.Boolean('Training')
    training_start_date = fields.Date('Start Date',
        states={
            'required': Bool(Eval('training')),
            },
        depends=['training'])
    training_end_date = fields.Date('End Date',
        states={
            'required': Bool(Eval('training')),
            },
        depends=['training'])
    training_registration = fields.Date('Registration Date',
        states={
            'required': Bool(Eval('training')),
            },
        depends=['training'],
        help='Last day to registration')
    training_place = fields.Many2One('party.address', 'Place')
    training_seats = fields.Integer('Seats')
    training_note = fields.Text('Training Note')
    
    @depends('training_start_date', 'training_registration', 'training_end_date')
    def on_change_training_start_date(self):
        res = {}
        if not self.training_end_date and self.training_start_date:
            res['training_end_date'] = self.training_start_date
        if not self.training_registration and self.training_start_date:
            res['training_registration'] = self.training_start_date
        return res

    @classmethod
    def view_attributes(cls):
        return super(ProductOneClickView, cls).view_attributes() + [
            ('//page[@id="esale"]', 'states', {
                    'invisible': Not(Bool(Eval('training'))),
                    })]


class ProductOneClick:
    __name__ = 'product.oneclick'

    @classmethod
    def get_template_values(self, vals):
        values = super(ProductOneClick, self).get_template_values(vals)
        if vals.training:
            values['training'] = vals.training
        return values

    @classmethod
    def get_product_values(self, vals):
        values = super(ProductOneClick, self).get_product_values(vals)
        if vals.training:
            values['training_start_date'] = vals.training_start_date or None
            values['training_end_date'] = vals.training_end_date or None
            values['training_registration'] = vals.training_registration or None
            values['training_place'] = vals.training_place or None
            values['training_seats'] = vals.training_seats or None
            values['training_note'] = vals.training_note or None
        return values
