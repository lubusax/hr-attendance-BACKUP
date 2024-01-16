# Copyright 2023 thingsintouch.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RfidLogAssignEmployee(models.TransientModel):
    _name = "hr.attendance.rfid.log.assign.employee"
    _description = "Assign an employee to a RFID card code"

    hr_attendance_rfid_log_id = fields.Many2one('hr.attendance.rfid.log', "Log", required=True)
    rfid_card_code = fields.Char(readonly=True, string = "RFID Card Code", copy=False)
    employee_id = fields.Many2one('hr.employee', "Employee", required=True)
    warning_message = fields.Char()
    
    def action_assign_employee(self):
        self.employee_id.rfid_card_code = self.rfid_card_code
        self.sudo().hr_attendance_rfid_log_id.employee_id = self.employee_id
        self.sudo().hr_attendance_rfid_log_id.message = "EMPLOYEE ASSIGNED - original error message: "+self.hr_attendance_rfid_log_id.error_message
        self.sudo().hr_attendance_rfid_log_id.employee_assigned = True
        self.sudo().hr_attendance_rfid_log_id.status = "retry"

    @api.onchange("employee_id")
    def on_change_employee_id(self):
        for record in self:
            if record.employee_id.rfid_card_code:
                record.warning_message = "Employee has already a RFID card code assigned. If you continue it will be overwritten."
            else:
                record.warning_message = ""