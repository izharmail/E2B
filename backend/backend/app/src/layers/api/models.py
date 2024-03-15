import typing as t

from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError

from app.src.shared import enums
from app.src.shared.enums import NullFlavor


# TODO: check if whole model layer is needed


class Value[T](BaseModel):
    value: T | None = None


class NullableValue[T, N](Value[T]):
    null_flavor: N | None = None

    @model_validator(mode='after')
    def _check_value_and_null_flavor_are_not_present_together(self) -> 'NullableValue':
        if self.null_flavor is not None and self.value is not None:
            raise PydanticCustomError('data_error', 'Null flavor should not be present if value is present')
        return self


class ApiModel(BaseModel):
    id: int | None = None


class ICSR(ApiModel):
    c_1_identification_case_safety_report: t.Optional['C_1_identification_case_safety_report'] = None


# TODO: check if None for Value is needed
class C_1_identification_case_safety_report(ApiModel):
    c_1_1_sender_safety_report_unique_id: Value[str] = Value()
    c_1_2_date_creation: Value[str] = Value()
    c_1_3_type_report: Value[enums.C_1_3_type_report] = Value()
    c_1_4_date_report_first_received_source: Value[str] = Value()
    c_1_5_date_most_recent_information: Value[str] = Value()
    c_1_6_1_additional_documents_available: Value[bool] = Value()
    c_1_6_1_r_documents_held_sender: list['C_1_6_1_r_documents_held_sender'] = []
    c_1_7_fulfil_local_criteria_expedited_report: NullableValue[bool, t.Literal[NullFlavor.NI]] = NullableValue()
    c_1_8_1_worldwide_unique_case_identification_number: Value[str] = Value()
    c_1_8_2_first_sender: Value[enums.C_1_8_2_first_sender] = Value()
    c_1_9_1_other_case_ids_previous_transmissions: NullableValue[t.Literal[True], t.Literal[NullFlavor.NI]] = NullableValue()
    c_1_9_1_r_source_case_id: list['C_1_9_1_r_source_case_id'] = []
    c_1_10_r_identification_number_report_linked: list['C_1_10_r_identification_number_report_linked'] = []
    c_1_11_1_report_nullification_amendment: Value[enums.C_1_11_1_report_nullification_amendment] = Value()
    c_1_11_2_reason_nullification_amendment: Value[str] = Value()


class C_1_6_1_r_documents_held_sender(ApiModel):
    c_1_6_1_r_1_documents_held_sender: Value[str] = Value()


class C_1_9_1_r_source_case_id(ApiModel):
    c_1_9_1_r_1_source_case_id: Value[str] = Value()
    c_1_9_1_r_2_case_id: Value[str] = Value()

class C_1_10_r_identification_number_report_linked(ApiModel):
    c_1_10_r_identification_number_report_linked: Value[str] = Value()
