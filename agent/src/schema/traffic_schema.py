from marshmallow import Schema, fields


class TrafficSchema(Schema):
    vehicle_count = fields.Int()