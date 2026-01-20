import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model


class Device(Model):
    __tablename__ = "device"

    _fillable = [
        "user_id",
        "device_id",
        "mark",
        "model",
        "carrier",
        "os",
        "nfc",
        "app_version",
    ]

    id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    device_id = Column(String(255), nullable=True, default=None)
    mark = Column(String(255), nullable=True, default=None)
    model = Column(String(255), nullable=True, default=None)
    carrier = Column(String(255), nullable=True, default=None)
    os = Column(String(255), nullable=True, default=None)
    nfc = Column(Boolean, nullable=True, default=False)
    app_version = Column(String(255), nullable=True, default=None)
    user_id = Column(String(36), ForeignKey('user.id', ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="devices")
    apps = relationship("DeviceApp", back_populates="device")
    contacts = relationship("DeviceContact", back_populates="device")

