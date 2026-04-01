from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DECIMAL,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Identifier(Base):
    __tablename__ = "Identifiers"

    identifier_name = Column(String(255), primary_key=True)
    description = Column(Text, nullable=True)
    identifier_type = Column(String(255), nullable=True)

    ownerships = relationship(
        "Ownership",
        back_populates="identifier",
        cascade="all, delete-orphan",
    )

    outgoing_relationships = relationship(
        "RelationshipModel",
        foreign_keys="RelationshipModel.from_identifier_name",
        back_populates="from_identifier",
        cascade="all, delete-orphan",
    )

    incoming_relationships = relationship(
        "RelationshipModel",
        foreign_keys="RelationshipModel.to_identifier_name",
        back_populates="to_identifier",
        cascade="all, delete-orphan",
    )

    identifier_characteristics = relationship(
        "IdentifierCharacteristic",
        back_populates="identifier",
        cascade="all, delete-orphan",
    )


class Country(Base):
    __tablename__ = "Countries"

    name = Column(String(255), primary_key=True)
    iso_code = Column(String(255), nullable=True)
    short_code = Column(String(255), nullable=True)

    consumer_units = relationship(
        "ConsumerUnit",
        back_populates="country",
        cascade="all, delete-orphan",
    )


class ConsumerUnit(Base):
    __tablename__ = "ConsumerUnits"

    number_of_consumers = Column(Integer, primary_key=True)
    country_name = Column(String(255), ForeignKey("Countries.name"), primary_key=True)

    country = relationship("Country", back_populates="consumer_units")


class Ownership(Base):
    __tablename__ = "Ownership"

    identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name"),
        primary_key=True,
    )
    user_id_tnumber = Column(String(255), primary_key=True)

    originator_first_name = Column(String(255), nullable=True)
    originator_last_name = Column(String(255), nullable=True)
    user_id_intranet = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    owner_first_name = Column(String(255), nullable=True)
    owner_last_name = Column(String(255), nullable=True)

    identifier = relationship("Identifier", back_populates="ownerships")


class RelationshipModel(Base):
    __tablename__ = "Relationships"

    from_identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name"),
        primary_key=True,
    )
    to_identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name"),
        primary_key=True,
    )
    relationship_name = Column(String(255), nullable=True)

    from_identifier = relationship(
        "Identifier",
        foreign_keys=[from_identifier_name],
        back_populates="outgoing_relationships",
    )
    to_identifier = relationship(
        "Identifier",
        foreign_keys=[to_identifier_name],
        back_populates="incoming_relationships",
    )


class Characteristic(Base):
    __tablename__ = "Characteristics"

    master_name = Column(String(255), primary_key=True)
    name = Column(String(255), primary_key=True)

    specifics = Column(String(255), nullable=True)
    action_required = Column(String(255), nullable=True)
    report_type = Column(String(255), nullable=True)
    data_type = Column(String(255), nullable=True)

    lower_routine_release_limit = Column(DECIMAL(10, 2), nullable=True)
    lower_limit = Column(DECIMAL(10, 2), nullable=True)
    lower_target = Column(DECIMAL(10, 2), nullable=True)
    target = Column(DECIMAL(10, 2), nullable=True)
    upper_target = Column(DECIMAL(10, 2), nullable=True)
    upper_limit = Column(DECIMAL(10, 2), nullable=True)
    upper_routine_release_limit = Column(DECIMAL(10, 2), nullable=True)

    test_frequency = Column(Integer, nullable=True)
    precision = Column(Integer, nullable=True)
    engineering_unit = Column(String(255), nullable=True)

    identifier_characteristics = relationship(
        "IdentifierCharacteristic",
        back_populates="characteristic",
        cascade="all, delete-orphan",
    )


class IdentifierCharacteristic(Base):
    __tablename__ = "IdentifierCharacteristics"

    identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name"),
        primary_key=True,
    )
    master_name = Column(String(255), primary_key=True)
    characteristic_name = Column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["master_name", "characteristic_name"],
            ["Characteristics.master_name", "Characteristics.name"],
        ),
    )

    identifier = relationship("Identifier", back_populates="identifier_characteristics")
    characteristic = relationship("Characteristic", back_populates="identifier_characteristics")