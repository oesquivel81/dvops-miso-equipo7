from marshmallow import Schema, fields, validate, ValidationError
import uuid

def validate_uuid(val):
    try:
        uuid.UUID(str(val))
    except Exception:
        raise ValidationError("app_uuid must be a valid UUID")

class BlacklistRequestDTO(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True, validate=validate_uuid)
    blocked_reason = fields.String(required=False, validate=validate.Length(max=255))
