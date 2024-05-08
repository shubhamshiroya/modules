odoo.define('donation_app.CalendarPopup', function (require) {
"use strict";
var CalendarPopover = require('web.CalendarPopover');
var session = require('web.session')
    var CalendarRenderer_accept_var = CalendarPopover.include({

        events: _.extend({}, CalendarPopover.prototype.events, {
            'click .oe-accepted-booking': '_onClickAccept',
            'click .oe-Rejected-booking': '_onClickReject',
        }),

        async calendarbookingbtn() {
            var self = this;
            var user_id_rec = session.uid
            var fields = ['name','users'];
            var found = 0;
            var v1 = await this._rpc({
                model: 'res.groups',
                method: 'search_read',
                args: [[['name', '=', 'Priest']],fields],
            });
            for (var j = 0; j < v1[0].users.length; j++){
                    if (v1[0].users[j]==session.uid) {
                        found=1;
                    }
                }
            if (self.modelName == 'calendar.booking'){
                if(found==1){
                return [$(".accept_button").show(),$(".reject_button").show(),$(".o_cw_popover_delete").hide(),$(".o_cw_popover_edit").hide()]
                }
                else if(found==0){
                return [$(".accept_button").hide(),$(".reject_button").hide(),$(".o_cw_popover_delete").hide(),$(".o_cw_popover_edit").hide()]
            }

            } else {
                return [$(".accept_button").hide(),$(".reject_button").hide(),$(".o_cw_popover_delete").show(),$(".o_cw_popover_edit").show()]
            }

            if(self.modelName=='calendar.booking' && found==1){
                return [$(".accept_button").show(),$(".reject_button").show(),$(".o_cw_popover_delete").hide(),$(".o_cw_popover_edit").hide()]
            }
            else if(self.modelName=='calendar.booking' && found==0){
                return [$(".accept_button").hide(),$(".reject_button").hide(),$(".o_cw_popover_delete").hide(),$(".o_cw_popover_edit").hide()]
            }
            else if(self.modelName=='calendar.management' && (found==0 | found==1)){
                return [$(".accept_button").hide(),$(".reject_button").hide()]
            }
        },
        _onClickAccept: function (ev) {
            ev.preventDefault();
            var self = this;
            var state ='accept';
            var c = this.event.extendedProps.record;
            c['state']='accept'
            this._rpc({
                model: 'calendar.booking',
                method: 'button_accept',
                args: [parseInt(this.event.id)],

            }).then(function () {
                self.event.extendedProps.record.state = state;
                self.$('.o_cw_popover_accept_rec').removeClass('btn-primary').addClass('fa-check text-success');
            });
        },
        _onClickReject: function (ev) {
            ev.preventDefault();

            var self = this;
            var state ='reject';
            var c = this.event.extendedProps.record;
            c['state']='reject'
            this._rpc({
                model: 'calendar.booking',
                method: 'button_reject',
                args: [parseInt(this.event.id)],
            }).then(function () {
                self.event.extendedProps.record.state = state;
                self.$('.o_cw_popover_reject_rec').removeClass('btn-primary').addClass('fa-times text-danger o_iban_fail');
            });
        var c = this.event.extendedProps.record;
            c['state']='accept'

            },
    })
    return CalendarRenderer_accept_var;
});