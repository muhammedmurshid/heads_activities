from odoo import models, fields, api


class HeadsReport(models.Model):
    _name = "heads.activities"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "heads activities"
    _rec_name = 'display_name'

    department_id = fields.Many2one('hr.department', string='Department', required=1)
    description = fields.Text(string='Description')
    type = fields.Selection(string='Type', selection=[('approval', 'Approval'), ('request', 'Request')], required=1)
    department_head_id = fields.Many2one('hr.employee', string='Department Head')
    state = fields.Selection(string='State', selection=[('draft', 'Draft'), ('in_progress', 'In Progress'),
                                                        ('approved', 'Approved'), ('rejected', 'Rejected'),
                                                        ('completed', 'Completed')], default='draft', tracking=1)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.department_id.name + '-' + 'Requirements'

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.department_id:
            self.department_head_id = self.department_id.manager_id.id

    def action_confirm(self):
        self.activity_schedule('heads_activities.mail_head_activity_for_heads',
                               user_id=self.department_head_id.user_id.id,
                               note=f"A new activity has been added for you.")
        self.state = 'in_progress'

    def action_approve(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.department_head_id.user_id.id), (
                'activity_type_id', '=', self.env.ref('heads_activities.mail_head_activity_for_heads',).id)])
        if activity_id:
            activity_id.action_feedback(feedback=f'Approved.')
        self.state = 'approved'

    def action_reject(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.department_head_id.user_id.id), (
                'activity_type_id', '=', self.env.ref('heads_activities.mail_head_activity_for_heads', ).id)])
        if activity_id:
            activity_id.action_feedback(feedback=f'Rejected.')
        self.state = 'rejected'

    def action_complete(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.department_head_id.user_id.id), (
                'activity_type_id', '=', self.env.ref('heads_activities.mail_head_activity_for_heads', ).id)])
        if activity_id:
            activity_id.action_feedback(feedback=f'Completed.')
        self.state = 'completed'
