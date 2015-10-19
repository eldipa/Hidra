define(["underscore", "shortcuts", 'event_handler'], function (_, shortcuts, event_handler) {
    'use strict';

    var Thread = function (id, tracker, obj) {
        this._properties = ["debugger_id", "thread_group_id", "state", "source_fullname", "source_line",  "instruction_address"];

        this.update(obj);
        this.id = id;
        this.tracker = tracker;
        this.EH = event_handler.get_global_event_handler();

    };

    Thread.prototype.update = shortcuts._update_properties;

    Thread.prototype.get_display_name = function () {
        return "Thread "+this.id+" ("+this.state+")";
    };

    Thread.prototype.get_thread_group_you_belong = function () {
        return this.tracker.get_debugger_with_id(this.debugger_id).get_thread_group_with_id(this.thread_group_id);
    };

    Thread.prototype.execute = function (command, args, callback, self_id_argument_position) {
        args = args || [];
        var self_id_argument = "--thread " + this.id;

        if (self_id_argument_position === undefined) {
            args.push(self_id_argument_position);
        }
        else {
            args[self_id_argument_position] = self_id_argument_position;
        }

        shortcuts.gdb_request(callback, 
                this.debugger_id, 
                command,
                args
                );
    };

    return {Thread: Thread};
});