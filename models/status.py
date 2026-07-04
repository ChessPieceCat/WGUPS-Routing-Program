'''STATUS = {
	AT_HUB,
	LOADED,
	ON_ROUTE,
	DELIVERED
}'''
from enum import Enum


class Status(Enum):
    AT_HUB = 'AT_HUB'
    LOADED = 'LOADED'
    ON_ROUTE = 'ON_ROUTE'
    DELIVERED = 'DELIVERED'