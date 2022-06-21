odoo.define('whatsapp_connector_tags.acrux_chat', function(require) {
"use strict";

var AcruxChatAction = require('whatsapp_connector.acrux_chat').AcruxChatAction


/**
 * @class
 * @name AcruxChatAction
 * @extends AcruxChatAction
 */
AcruxChatAction.include({

    /**
     * Hace trabajos de render
     *
     * @private
     * @returns {Promise} Para indicar que termino
     */
    _initRender: function() {
        return this._super().then(() => {
            this.$('li#tab_conv_info').removeClass('d-none')
        });
    },

    /**
     * @override
     */
    destroy: function() {
        // por si acaso que se queda el popup con la descripcion
        // se elimina 
        $('.acrux-note-popover').remove()
        return this._super.apply(this, arguments);
    },

});

return AcruxChatAction;
});
