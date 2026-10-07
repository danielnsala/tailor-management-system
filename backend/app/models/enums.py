from enum import Enum


class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    IN_PROGRESS = "IN_PROGRESS"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class JobType(str, Enum):
    CUSTOM_SEWING = "CUSTOM_SEWING"
    ALTERATION = "ALTERATION"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    ZELLE = "ZELLE"


class MeasurementUnit(str, Enum):
    INCHES = "INCHES"
    CENTIMETERS = "CENTIMETERS"


class GalleryItemType(str, Enum):
    PREVIOUS_WORK = "PREVIOUS_WORK"
    INSPIRATION = "INSPIRATION"