odoo.define('whatsapp_connector.basic_fields', function(require) {
"use strict";

var core = require('web.core');
var InputField = require('web.basic_fields').InputField;
var registry = require('web.field_registry');
var _t = core._t;

/**
 * Widget para seleccionar color.
 *
 * @class
 * @name RecordPicker
 * @extends web.basic_fields.InputField
 */
var RecordPicker = InputField.extend({
    className: 'o_record_picker_field',
    supportedFieldTypes: ['char'],
    description: "",

    /**
     * @override
     * @see InputField.init
     */
    init: function() {
        this._super.apply(this, arguments);
        this.tagName = 'div';
    },

    /**
     * @override
     * @private
     * @see InputField._renderReadonly
     */
    _renderReadonly: function() {
        this.$el.empty()
        this.$el.css('display', 'inline-flex')
        this.$el.append(`<span>${this.value}</span>`)
        this.$buttonView = $(`
            <button type="button" class="btn btn btn-primary" style="margin-left: 1em;">
                <i class="fa fa-fw o_button_icon fa-eye"></i>
                <span>${_t('View Record')}</span>
            </button>
        `)
        this.$buttonView.click(() => this.openRecord())
        this.$el.append(this.$buttonView)
    },

    /**
     * @override
     * @private
     * @see InputField._renderEdit
     */
    _renderEdit: function() {
        this.$el.empty()
        this.$el.css('display', 'inline-flex')
        this.$input = $('<input/>')
        this._prepareInput(this.$input);
        this.$input.css("maxWidth", "4em");
        this.$input.attr({ readonly: 'readonly' });
        this.$el.append(this.$input)
        this.$buttonSelect = $(`
            <button type="button" class="btn btn btn-primary" style="margin-left: 1em;">
                <i class="fa fa-fw o_button_icon fa-search"></i>
                <span>${_t('Select a Record')}</span>
            </button>
        `)
        this.$buttonSelect.click(() => this.openSelector())
        this.$el.append(this.$buttonSelect)
    },

    /**
     * Abre el wizard para seleccionar
     */
    openSelector: function() {
        if (!this.nodeOptions?.model_field) {
            return this.call('crash_manager', 'show_warning', {message: _t('You must set options with "model_field" in your xml.')})
        }
        if (!this.getParent()?.state?.data[this.nodeOptions.model_field]) {
            return this.call('crash_manager', 'show_warning', {message: _t('You must select your model first.')})
        }
        const context = _.extend({ chatroom_wizard_search: true }, this.record.context);
        const action = {
            type: 'ir.actions.act_window',
            view_type: 'form',
            view_mode: 'list',
            res_model: this.getParent()?.state?.data[this.nodeOptions?.model_field],
            views: [[false, 'list']],
            target: 'new',
            context: context,
            flags: {
                action_buttons: false,
                withBreadcrumbs: false,
            }
        }
        return this.do_action(action).then(action =>
            action.controllers.list.then(result =>
                result.widget._chatroomSelectRecord = (record) => {
                    if (record) {
                        this.$input.val(record.data.id.toString())
                        this._onChange()
                    }
                }
            )
        )
    },

    /**
     * Abre el registro 
     */
    openRecord: function() {
        if (!this.nodeOptions?.model_field) {
            return this.call('crash_manager', 'show_warning', {message: _t('You must set options with "model_field" in your xml.')})
        }
        if (!this.getParent()?.state?.data[this.nodeOptions.model_field]) {
            return this.call('crash_manager', 'show_warning', {message: _t('You must select your model first.')})
        }
        if (!this.value) {
            return this.call('crash_manager', 'show_warning', {message: _t('You must select a record before view.')})
        }
        const action = {
            type: 'ir.actions.act_window',
            view_type: 'form',
            view_mode: 'form',
            res_model: this.getParent()?.state?.data[this.nodeOptions?.model_field],
            views: [[false, 'form']],
            target: 'new',
            context: this.record.context,
            res_id: parseInt(this.value),
            flags: {
                mode: 'readonly'
            }
        }
        return this.do_action(action)
    }
})

registry.add('record_picker', RecordPicker);

return {
    RecordPicker: RecordPicker,
}

})
