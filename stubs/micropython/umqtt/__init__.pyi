"""Type stubs for umqtt package."""

from umqtt.simple import MQTTClient as SimpleMQTTClient
from umqtt.robust import MQTTClient as RobustMQTTClient

__all__ = ['SimpleMQTTClient', 'RobustMQTTClient']
