odoo.define('dev_job_position_request.DashboardElc', function (require) {
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var web_client = require('web.web_client');
   var session = require('web.session');
   var ajax = require('web.ajax');
   var _t = core._t;
   var rpc = require('web.rpc');
   var self = this;
   var DashboardSheet1 = AbstractAction.extend({
       contentTemplate : 'DashboardElc',

       events: {
            'click .elc_tran_prob': 'tran_prob_pen',
            'click .elc_prob_to_conf': 'prob_to_conf_pen',
            'click .elc_prob_ext': 'prob_ext_pen',
            'click .elc_transfers': 'transfers_pen',
            'click .elc_promotion': 'promotion_pen',
            'click .elc_increments': 'increments_pen',
            'click .elc_re_designation': 're_designation_pen',

            'click .elc_tran_prob_app': 'tran_prob_app',
            'click .elc_prob_to_conf_app': 'prob_to_conf_app',
            'click .elc_prob_ext_app': 'prob_ext_app',
            'click .elc_transfers_app': 'transfers_app',
            'click .elc_promotion_app': 'promotion_app',
            'click .elc_increments_app': 'increments_app',
            'click .elc_re_designation_app': 're_designation_app',

            'click .disp_emp_incident': 'emp_incident',
            'click .disp_emp_man_incident_pen': 'emp_man_incident_pen',
            'click .disp_emp_man_incident_close': 'emp_man_incident_close',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardEmployeeElc'];
       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardSheet1');
           return this._super().then(function() {
               self.render_dashboards();
           });
       },
       willStart: function(){
           var self = this;
           return this._super()
       },
       render_dashboards: function() {
           var self = this;
           this.fetch_data()
           var templates = []
           var templates = ['DashboardEmployeeElc'];
           _.each(templates, function(template) {
               self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
           });
       },
       fetch_data: function() {
           var self = this
//          fetch data to the tiles
           var def1 = this._rpc({
               model: 'employee.life.cycle',
               method: "get_data",
           })
           .then(function (result) {
               $('#initial_no_tran_prob').append('<span>' + result.total_tran_prob + '</span>');
               $('#initial_no_prob_to_conf').append('<span>' + result.total_prob_to_conf + '</span>');
               $('#initial_no_prob_ext').append('<span>' + result.total_prob_ext + '</span>');
               $('#initial_no_transfers').append('<span>' + result.total_transfers + '</span>');
               $('#initial_no_promotion').append('<span>' + result.total_promotion + '</span>');
               $('#initial_no_increments').append('<span>' + result.total_increments + '</span>');
               $('#initial_no_re_designation').append('<span>' + result.total_re_designation + '</span>');

               $('#final_no_tran_prob').append('<span>' + result.final_tran_prob + '</span>');
               $('#final_no_prob_to_conf').append('<span>' + result.final_prob_to_conf + '</span>');
               $('#final_no_prob_ext').append('<span>' + result.final_prob_ext + '</span>');
               $('#final_no_transfers').append('<span>' + result.final_transfers + '</span>');
               $('#final_no_promotion').append('<span>' + result.final_promotion + '</span>');
               $('#final_no_increments').append('<span>' + result.final_increments + '</span>');
               $('#final_no_re_designation').append('<span>' + result.final_re_designation + '</span>');

               $('#total_no_tran_prob').append('<span>' + (result.total_tran_prob + result.final_tran_prob)+ '</span>');
               $('#total_no_prob_to_conf').append('<span>' +( result.total_prob_to_conf + result.final_prob_to_conf )+ '</span>');
               $('#total_no_prob_ext').append('<span>' + (result.total_prob_ext + result.final_prob_ext )+ '</span>');
               $('#total_no_transfers').append('<span>' + (result.total_transfers + result.final_transfers ) + '</span>');
               $('#total_no_promotion').append('<span>' + (result.total_promotion + result.final_promotion )+ '</span>');
               $('#total_no_increments').append('<span>' + (result.total_increments + result.final_increments )+ '</span>');
               $('#total_no_re_designation').append('<span>' + (result.total_re_designation + result.final_re_designation )+'</span>');

               $('#total_no_incident').append('<span>' + result.total_incident+'</span>');
               $('#total_no_incident_progress').append('<span>' + result.total_incident_progress+'</span>');
               $('#total_no_incident_approved').append('<span>' + result.total_incident_approved+'</span>');
           });
       },

       view_page: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'employee.life.cycle',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

       view_sheet: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'employee.disciplinary',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

       view_sheet1: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'manage.incident',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

        emp_incident : function () {
            var self = this;
            var name =  _t("Number Incidents");
            var domain = [];
            self.view_sheet1(domain,name);
        },

        emp_man_incident_pen : function () {
            var self = this;
            var name =  _t("Incidents In pending");
            var domain = [['state', '=', 'in_progress']];
            self.view_sheet1(domain,name);
        },

        emp_man_incident_close : function () {
            var self = this;
            var name =  _t("Incidents In Closed");
            var domain = [['state', '=', 'closed']];
            self.view_sheet1(domain,name);
        },

       tran_prob_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','tran_prob']];
            self.view_page(domain,name);
        },

        prob_to_conf_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','prob_to_conf']];
            self.view_page(domain,name);
        },

        prob_ext_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','prob_ext']];
            self.view_page(domain,name);
        },

        transfers_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','transfers']];
            self.view_page(domain,name);
        },

        promotion_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','promotion']];
            self.view_page(domain,name);
        },

        increments_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','increments']];
            self.view_page(domain,name);
        },

        re_designation_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','re_designation']];
            self.view_page(domain,name);
        },

        tran_prob_app : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','tran_prob']];
            self.view_page(domain,name);
        },

        prob_to_conf_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','prob_to_conf']];
            self.view_page(domain,name);
        },

        prob_ext_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','prob_ext']];
            self.view_page(domain,name);
        },

        transfers_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','transfers']];
            self.view_page(domain,name);
        },

        promotion_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','promotion']];
            self.view_page(domain,name);
        },

        increments_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','increments']];
            self.view_page(domain,name);
        },

        re_designation_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','re_designation']];
            self.view_page(domain,name);
        },

    });
   core.action_registry.add('employee_dashboard_elc', DashboardSheet1);
   return DashboardSheet1;
});