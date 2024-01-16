# Copyright 2023 - thingsintouch.com
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models

class RfidAttendanceLog(models.Model):
    _name = "hr.attendance.rfid.log"
    _description = "HR Attendance RFID Logging"
    _order = "id desc"

    state = fields.Selection(
        selection=[("success", "Success"), ("failed", "Failed"), ("modified", "Modified"), ("retry", "Retry"), ("ignore", "Ignore"), ("succes_after_retry", "Success after Retry") ],
        readonly=True
    )
    rfid_card_code = fields.Char(readonly=True, string = "RFID Card Code", copy=False) #hr.employee.base.rfid_card_code 
    employee_name = fields.Char(readonly=True) # hr.employee.base.name
    employee_id = fields.Many2one('hr.employee', 
                                  ondelete='cascade', 
                                  index=True)
    error_message = fields.Char(readonly=True)
    logged = fields.Boolean(readonly=True) 
    action = fields.Selection(
        selection=[("check_in", "check in"), ("check_out", "check out"), ("FALSE", "Not Defined (in or out)")], readonly=True
    )
    timestamp = fields.Datetime(string="RFID-Timestamp", default=fields.Datetime.now, required=True)
    iot_device_id = fields.Many2one('iot.device', 
                                  ondelete='cascade', 
                                  index=True)
    employee_assigned = fields.Boolean(compute="_compute_employee_assigned")

    @api.depends("error_message")
    def  _compute_employee_assigned(self):
        for record in self:
            record.employee_assigned = False if "No employee found with card" in record.error_message else True

    def action_open_wizard_assign_employee(self):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "hr_attendance_rfid_log",
            "action_hr_rfid_log_assign_employee"
        )
        action["context"] = {
            "default_rfid_card_code": self.rfid_card_code,
            "default_hr_attendance_rfid_log_id": self.id
        }
        return action
    
    def set_to_retry_state(self):
        self.sudo().state = "retry"
        #self.env["hr.employee"].sudo().register_attendance(self.rfid_card_code)
    
    def set_to_ignore_state(self):
        self.sudo().state = "ignore"    
