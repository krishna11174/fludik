odoo.define('contacts_custom.description_onchange.js', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    // Function to open the wizard
    function openWizard(activeId) {
        rpc.query({
            model: 'my.module.my_wizard',
            method: 'default_get',
            args: [{}, {}], // You can pass any additional context if required
        }).then(function (defaults) {
            core.bus.trigger('do-action', {
                action_data: {
                    type: 'ir.actions.act_window',
                    res_model: 'my.module.my_wizard',
                    view_mode: 'form',
                    views: [[false, 'form']],
                    res_id: defaults.id,
                    target: 'new',
                    context: {},
                },
            });
        });
    }

    return { openWizard: openWizard };
});

