from marshmallow import Schema, fields

class BlacklistResponseDTO(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(required=False)
    ip_address = fields.String(required=True)
    created_at = fields.DateTime(required=True)
