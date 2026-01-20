import uuid
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model
from ms_fa.helpers.utils import array_search


# Entity dictionary for Mexican states
mx_entities = [
    {"id": "AS", "state": "AGUASCALIENTES"},
    {"id": "BC", "state": "BAJA CALIFORNIA"},
    {"id": "BS", "state": "BAJA CALIFORNIA SUR"},
    {"id": "CC", "state": "CAMPECHE"},
    {"id": "CL", "state": "COAHUILA"},
    {"id": "CM", "state": "COLIMA"},
    {"id": "CS", "state": "CHIAPAS"},
    {"id": "CH", "state": "CHIHUAHUA"},
    {"id": "DF", "state": "CIUDAD DE MEXICO"},
    {"id": "DG", "state": "DURANGO"},
    {"id": "GT", "state": "GUANAJUATO"},
    {"id": "GR", "state": "GUERRERO"},
    {"id": "HG", "state": "HIDALGO"},
    {"id": "JC", "state": "JALISCO"},
    {"id": "MC", "state": "MEXICO"},
    {"id": "MN", "state": "MICHOACAN"},
    {"id": "MS", "state": "MORELOS"},
    {"id": "NT", "state": "NAYARIT"},
    {"id": "NL", "state": "NUEVO LEON"},
    {"id": "OC", "state": "OAXACA"},
    {"id": "PL", "state": "PUEBLA"},
    {"id": "QT", "state": "QUERETARO"},
    {"id": "QR", "state": "QUINTANA ROO"},
    {"id": "SP", "state": "SAN LUIS POTOSI"},
    {"id": "SL", "state": "SINALOA"},
    {"id": "SR", "state": "SONORA"},
    {"id": "TC", "state": "TABASCO"},
    {"id": "TS", "state": "TAMAULIPAS"},
    {"id": "TL", "state": "TLAXCALA"},
    {"id": "VZ", "state": "VERACRUZ"},
    {"id": "YN", "state": "YUCATAN"},
    {"id": "ZS", "state": "ZACATECAS"},
    {"id": "NE", "state": "NACIDO EN EL EXTRANJERO"},
]


class Profile(Model):
    __tablename__ = "profile"

    _fillable = [
        "rfc",
        "curp",
        "home_phone",
        "birthday",
        "entity_birth",
        "gender",
        "grade",
        "marital_status",
        "municipality",
        "street",
        "reference_street",
        "reference_street_other",
        "additional_reference",
        "exterior",
        "interior",
        "neighborhood",
        "zip",
        "department",
        "state",
        "country",
        "monthly_expenditure",
        "income",
        "income_family",
        "count_home",
        "count_income_people",
        "company_name",
        "type_activity",
        "position",
        "time_activity_year",
        "time_activity_month",
        "personal_references",
        "legal_id_front",
        "legal_id_back",
        "proof_of_address",
    ]

    id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    rfc = Column(String(13), unique=True, nullable=True)
    curp = Column(String(18), unique=True, nullable=True)
    home_phone = Column(String(15), nullable=True)
    birthday = Column(DateTime, nullable=True)
    entity_birth = Column(String(255), nullable=True)
    gender = Column(String(50), nullable=True)
    grade = Column(String(60), nullable=True)
    marital_status = Column(String(60), nullable=True)
    municipality = Column(String(60), nullable=True)
    street = Column(String(255), nullable=True)
    reference_street = Column(String(255), nullable=True)
    reference_street_other = Column(String(255), nullable=True)
    additional_reference = Column(String(255), nullable=True)
    exterior = Column(String(62), nullable=True)
    interior = Column(String(62), nullable=True)
    neighborhood = Column(String(255), nullable=True)
    zip = Column(String(5), nullable=True)
    department = Column(String(255), nullable=True)
    state = Column(String(60), nullable=True)
    country = Column(String(60), nullable=True, default="México")
    monthly_expenditure = Column(Float, nullable=True)
    income = Column(Float, nullable=True)
    income_family = Column(Float, nullable=True)
    count_home = Column(Integer, nullable=True)
    count_income_people = Column(Integer, nullable=True)
    company_name = Column(String(255), nullable=True)
    type_activity = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    time_activity_year = Column(Integer, nullable=True)
    time_activity_month = Column(Integer, nullable=True)
    personal_references = Column(JSON, nullable=True)
    available_credit = Column(Float, nullable=True, default=0)
    payment_capacity = Column(Float, nullable=True, default=0)
    second_credit = Column(Boolean, nullable=True, default=False)
    aq_id = Column(String(36), nullable=True)
    kyc_prescoring_id = Column(Integer, nullable=True)
    pay_id = Column(String(60), nullable=True)
    legal_id_front = Column(String(255), nullable=True)
    legal_id_back = Column(String(255), nullable=True)
    proof_of_address = Column(String(255), nullable=True)

    user_id = Column(String(36), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<profile id={self.id} rfc={self.rfc} curp={self.curp}>"

    @property
    def state_name(self):
        item = array_search(mx_entities, "id", self.state)
        return item["state"].capitalize() if item is not None else self.state

    @property
    def entity_birth_name(self):
        item = array_search(mx_entities, "id", self.entity_birth)
        return item["state"].capitalize() if item is not None else self.entity_birth

