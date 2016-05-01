#!/usr/bin/env python
# -*- coding: utf-8 -*-


import marshmallow as ma
from marshmallow.exceptions import ValidationError
from marshmallow.compat import iteritems, PY2
from marshmallow.fields import *


DOC_TYPE = 'type'
OBJ_ID = 'id'


def plain_function(f):
    """Ensure that ``callable`` is a plain function rather than an unbound method."""
    if PY2 and f:
        return f.im_func
    # Python 3 doesn't have bound/unbound methods, so don't need to do anything
    return f


class SchemaOpts(ma.SchemaOpts):

    def __init__(self, meta):
        super(SchemaOpts, self).__init__(meta)
        self.type_ = getattr(meta, 'type_', None)
        self.inflect = plain_function(getattr(meta, 'inflect', None))


class Schema(ma.Schema):
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)

        if not self.opts.type_:
            raise ValueError('Must specify type_ class Meta option')

        if 'id' not in self.fields:
            raise ValueError('Must have an `id` field')

    OPTIONS_CLASS = SchemaOpts

    @ma.post_dump(pass_many=True)
    def format_json_api_response(self, data, many):
        ret = self.format_items(data, many)
        ret = self.wrap_response(ret, many)
        return ret

    def unwrap_item(self, item):
        if 'type' not in item:
            raise ma.ValidationError([
                {
                    'detail': '`data` object must include `type` key.',
                    'pointer': '/data'
                }
            ])
        if item['type'] != self.opts.type_:
            raise ValueError('type error: ' + item['type'] + ', type: ' + self.opts.type_ + ' is necessary')

        payload = self.dict_class()
        if 'id' in item:
            payload['id'] = item['id']
        for key, value in iteritems(item.get('attributes', {})):
            payload[key] = value
        for key, value in iteritems(item.get('relationships', {})):
            payload[key] = value
        return payload

    @ma.pre_load(pass_many=True)
    def unwrap_request(self, data, many):
        if 'data' not in data:
            raise ma.ValidationError('Object must include `data` key.')

        data = data['data']
        if many:
            return [self.unwrap_item(each) for each in data]
        return self.unwrap_item(data)

    def on_bind_field(self, field_name, field_obj):
        if not field_obj.load_from:
            field_obj.load_from = self.inflect(field_name)
        return None

    def _do_load(self, data, many=None, **kwargs):
        many = self.many if many is None else bool(many)
        try:
            result, errors = super(Schema, self)._do_load(data, many, **kwargs)
        except ValidationError as err:  # strict mode
            formatted_messages = self.format_errors(err.messages, many=many)
            err.messages = formatted_messages
            raise err
        else:
            formatted_messages = self.format_errors(errors, many=many)
        return result, formatted_messages

    def inflect(self, text):
        return self.opts.inflect(text) if self.opts.inflect else text

    def format_errors(self, errors, many):
        if not errors:
            return {}
        if isinstance(errors, (list, tuple)):
            return {'errors': errors}

        formatted_errors = []
        if many:
            for index, errors in iteritems(errors):
                for field_name, field_errors in iteritems(errors):
                    formatted_errors.extend([
                        self.format_error(field_name, message, index=index)
                        for message in field_errors
                    ])
        else:
            for field_name, field_errors in iteritems(errors):
                formatted_errors.extend([
                    self.format_error(field_name, message)
                    for message in field_errors
                ])
        return {'errors': formatted_errors}

    def format_error(self, field_name, message, index=None):
        relationship = isinstance(
            self.declared_fields.get(field_name), BaseRelationship)
        if relationship:
            container = 'relationships'
        else:
            container = 'attributes'

        inflected_name = self.inflect(field_name)

        if index:
            pointer = '/data/{}/{}/{}'.format(index, container, inflected_name)
        else:
            pointer = '/data/{}/{}'.format(container, inflected_name)

        if relationship:
            pointer = '{}/data'.format(pointer)

        return {
            'detail': message,
            'source': {
                'pointer': pointer
            }
        }

    def format_item(self, item):
        ret = self.dict_class()
        ret[DOC_TYPE] = self.opts.type_

        # Get the schema attributes so we can confirm `dump-to` values exist
        attributes = {
            (self.fields[field].dump_to or field): field
            for field in self.fields
        }

        for field_name, value in iteritems(item):
            attribute = attributes[field_name]
            if attribute == OBJ_ID:
                ret[OBJ_ID] = value
            elif isinstance(self.fields[attribute], BaseRelationship):
                if 'relationships' not in ret:
                    ret['relationships'] = self.dict_class()
                ret['relationships'][self.inflect(field_name)] = value
            else:
                if 'attributes' not in ret:
                    ret['attributes'] = self.dict_class()
                ret['attributes'][self.inflect(field_name)] = value

        return ret

    def format_items(self, data, many):
        if many:
            return [self.format_item(item) for item in data]
        else:
            return self.format_item(data)

    def wrap_response(self, data, many):
        ret = {'data': data}
        return ret


class BaseRelationship(Field):
    pass


class Relationship(BaseRelationship):
    pass
