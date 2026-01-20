import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model


class DeviceContact(Model):
    __tablename__ = "device_contact"

    _fillable = [
        "device_id",
        "name",
        "phone",
    ]

    id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    device_id = Column(String(36), ForeignKey('device.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)

    device = relationship("Device", back_populates="contacts")

