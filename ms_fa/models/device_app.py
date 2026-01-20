import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model


class DeviceApp(Model):
    __tablename__ = "device_app"

    _fillable = [
        "device_id",
        "name",
        "package",
    ]

    id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    device_id = Column(String(36), ForeignKey('device.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=True)
    package = Column(String(255), nullable=True)

    device = relationship("Device", back_populates="apps")

