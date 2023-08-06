# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from growingio_tracker.data_parser import DataParser
from growingio_tracker.version import VERSION
from .event_v3_pb2 import CUSTOM, LOGIN_USER_ATTRIBUTES
from .event_v3_pb2 import ResourceItem, EventV3Dto, EventV3List


class ProtobufParser(DataParser):

    def __init__(self):
        super(ProtobufParser, self).__init__()

    def get_bytes(self, messages, stm=None):
        return self.protobuf(messages)

    def get_headers(self):
        return {'content-type': 'application/protobuf'}

    def get_type(self, type):
        if type == "CUSTOM":
            return CUSTOM
        elif type == "LOGIN_USER_ATTRIBUTES":
            return LOGIN_USER_ATTRIBUTES
        else:
            return CUSTOM

    def protobuf(self, messages):
        events = []
        for message in messages:
            event = EventV3Dto()
            # event message
            if hasattr(message, 'event_type') and message.event_type is not None:
                event.event_type = self.get_type(message.event_type)
            if hasattr(message, 'event_time') and message.event_time is not None:
                event.timestamp = message.event_time
            if hasattr(message, 'event_name') and message.event_name is not None:
                event.event_name = message.event_name
            if hasattr(message, 'anonymous_id') and message.anonymous_id is not None:
                event.device_id = message.anonymous_id
            if hasattr(message, 'login_user_key') and message.login_user_key is not None:
                event.user_key = message.login_user_key
            if hasattr(message, 'login_user_id') and message.login_user_id is not None:
                event.user_id = message.login_user_id
            if hasattr(message, 'attributes') and message.attributes is not None:
                for k, v in message.attributes.items():
                    event.attributes[str(k)] = str(v)
            # item message
            item = ResourceItem()
            if hasattr(message, 'key') and message.key is not None:
                item.key = message.key
            if hasattr(message, 'id') and message.id is not None:
                item.id = message.id
            if hasattr(message, 'attrs') and message.attrs is not None:
                for k, v in message.attrs.items():
                    item.attributes[str(k)] = str(v)

            if item.key is not None and item.id is not None:
                event.resource_item.CopyFrom(item)

            # common
            if hasattr(message, 'data_source_id'): event.data_source_id = message.data_source_id
            if hasattr(message, 'product_id'): event.project_key = message.product_id

            event.sdk_version = VERSION
            event.platform = 'python'

            events.append(event)
        event_list = EventV3List()
        event_list.values.extend(events)
        return event_list.SerializeToString()
