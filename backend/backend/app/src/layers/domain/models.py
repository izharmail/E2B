from decimal import Decimal
import typing as t
from uuid import UUID

from app.src.shared import enums
from app.src.shared.enums import NullFlavor as NF
from extensions import pydantic as pde


class DomainModel(pde.PostValidatableModel, pde.SafeValidatableModel):    
    id: int | None = None


class ICSR(DomainModel):
    c_1_identification_case_safety_report: t.Optional['C_1_identification_case_safety_report'] = None
    c_2_r_primary_source_information: list['C_2_r_primary_source_information'] = []
    c_3_information_sender_case_safety_report: t.Optional['C_3_information_sender_case_safety_report'] = None
    c_4_r_literature_reference: list['C_4_r_literature_reference'] = []
    c_5_study_identification: t.Optional['C_5_study_identification'] = None
    d_patient_characteristics: t.Optional['D_patient_characteristics'] = None
    e_i_reaction_event: list['E_i_reaction_event'] = []
    f_r_results_tests_procedures_investigation_patient: list['F_r_results_tests_procedures_investigation_patient'] = []
    g_k_drug_information: list['G_k_drug_information'] = []
    h_narrative_case_summary: t.Optional['H_narrative_case_summary'] = None

    @classmethod
    def _post_validate(cls, processor: pde.PostValidationProcessor) -> None:
        processor.try_validate_fields(
            validate=cls._validate_uuids,
            is_add_error_manually=True
        )

    @staticmethod
    def _validate_uuids(
        processor: pde.PostValidationProcessor,
        e_i_reaction_event: list['E_i_reaction_event'], 
        g_k_drug_information: list['G_k_drug_information']
    ) -> bool:
        is_valid = True

        reaction_ids = set()
        for reaction in e_i_reaction_event:
            if reaction.id:
                reaction_ids.add(reaction.id)
            if reaction.uuid:
                reaction_ids.add(reaction.uuid)

        for k, drug in enumerate(g_k_drug_information):
            for i, link in enumerate(drug.g_k_9_i_drug_reaction_matrix):
                reaction_id = link.g_k_9_i_1_reaction_assessed

                if reaction_id in reaction_ids:
                    continue

                processor.add_error(
                    type=pde.ErrorType.CUSTOM,
                    message='Technical id was not found among possible related entities',
                    loc=('g_k_drug_information', k, 'g_k_9_i_drug_reaction_matrix', i, 'g_k_9_i_1_reaction_assessed'),
                    input=reaction_id
                )
                is_valid = False

        return is_valid


# C_1_identification_case_safety_report


class C_1_identification_case_safety_report(DomainModel):
    c_1_6_1_r_documents_held_sender: list['C_1_6_1_r_documents_held_sender'] = []
    c_1_9_1_r_source_case_id: list['C_1_9_1_r_source_case_id'] = []
    c_1_10_r_identification_number_report_linked: list['C_1_10_r_identification_number_report_linked'] = []

    c_1_1_sender_safety_report_unique_id: str | None = None
    c_1_2_date_creation: str | None = None  # dt
    c_1_3_type_report: enums.C_1_3_type_report | None = None
    c_1_4_date_report_first_received_source: str | None = None  # dt
    c_1_5_date_most_recent_information: str | None = None  # dt

    # c_1_6_additional_available_documents_held_sender
    c_1_6_1_additional_documents_available: bool | None = None

    c_1_7_fulfil_local_criteria_expedited_report: bool | t.Literal[NF.NI] | None = None

    # c_1_8_worldwide_unique_case_identification
    c_1_8_1_worldwide_unique_case_identification_number: str | None = None
    c_1_8_2_first_sender: enums.C_1_8_2_first_sender | None = None

    # c_1_9_other_case_ids
    c_1_9_1_other_case_ids_previous_transmissions: t.Literal[True] | t.Literal[NF.NI] | None = None

    # c_1_11_report_nullification_amendment
    c_1_11_1_report_nullification_amendment: enums.C_1_11_1_report_nullification_amendment | None = None
    c_1_11_2_reason_nullification_amendment: str | None = None


class C_1_6_1_r_documents_held_sender(DomainModel):
    c_1_6_1_r_1_documents_held_sender: str | None = None
    # file: c_1_6_1_r_2_included_documents


class C_1_9_1_r_source_case_id(DomainModel):
    c_1_9_1_r_1_source_case_id: str | None = None
    c_1_9_1_r_2_case_id: str | None = None


class C_1_10_r_identification_number_report_linked(DomainModel):
    c_1_10_r_identification_number_report_linked: str | None = None


# C_2_r_primary_source_information


class C_2_r_primary_source_information(DomainModel):
    # c_2_r_1_reporter_name
    c_2_r_1_1_reporter_title: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None
    c_2_r_1_2_reporter_given_name: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_1_3_reporter_middle_name: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_1_4_reporter_family_name: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None

    # c_2_r_2_reporter_address_telephone
    c_2_r_2_1_reporter_organisation: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_2_reporter_department: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_3_reporter_street: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_4_reporter_city: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_5_reporter_state_province: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_6_reporter_postcode: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None
    c_2_r_2_7_reporter_telephone: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None

    c_2_r_3_reporter_country_code: str | None = None  # st
    c_2_r_4_qualification: enums.C_2_r_4_qualification | t.Literal[NF.UNK] | None = None
    c_2_r_5_primary_source_regulatory_purposes: enums.C_2_r_5_primary_source_regulatory_purposes | None = None


# C_3_information_sender_case_safety_report


class C_3_information_sender_case_safety_report(DomainModel):
    c_3_1_sender_type: enums.C_3_1_sender_type | None = None
    c_3_2_sender_organisation: str | None = None

    # c_3_3_person_responsible_sending_report
    c_3_3_1_sender_department: str | None = None
    c_3_3_2_sender_title: str | None = None
    c_3_3_3_sender_given_name: str | None = None
    c_3_3_4_sender_middle_name: str | None = None
    c_3_3_5_sender_family_name: str | None = None

    # c_3_4_sender_address_fax_telephone_email
    c_3_4_1_sender_street_address: str | None = None
    c_3_4_2_sender_city: str | None = None
    c_3_4_3_sender_state_province: str | None = None
    c_3_4_4_sender_postcode: str | None = None
    c_3_4_5_sender_country_code: str | None = None  # st
    c_3_4_6_sender_telephone: str | None = None
    c_3_4_7_sender_fax: str | None = None
    c_3_4_8_sender_email: str | None = None


# C_4_r_literature_reference


class C_4_r_literature_reference(DomainModel):
    c_4_r_1_literature_reference: str | t.Literal[NF.ASKU, NF.NASK] | None = None
    # file: c_4_r_2_included_documents


# C_5_study_identification

class C_5_study_identification(DomainModel):
    c_5_1_r_study_registration: list['C_5_1_r_study_registration'] = []

    c_5_2_study_name: str | t.Literal[NF.ASKU, NF.NASK] | None = None
    c_5_3_sponsor_study_number: str | t.Literal[NF.ASKU, NF.NASK] | None = None
    c_5_4_study_type_reaction: enums.C_5_4_study_type_reaction | None = None


class C_5_1_r_study_registration(DomainModel):
    c_5_1_r_1_study_registration_number: str | t.Literal[NF.ASKU, NF.NASK] | None = None
    c_5_1_r_2_study_registration_country: str | t.Literal[NF.ASKU, NF.NASK] | None = None  # st


# D_patient_characteristics


class D_patient_characteristics(DomainModel):
    d_7_1_r_structured_information_medical_history: list['D_7_1_r_structured_information_medical_history'] = []
    d_8_r_past_drug_history: list['D_8_r_past_drug_history'] = []
    d_9_2_r_cause_death: list['D_9_2_r_cause_death'] = []
    d_9_4_r_autopsy_determined_cause_death: list['D_9_4_r_autopsy_determined_cause_death'] = []
    d_10_7_1_r_structured_information_parent_meddra_code: list['D_10_7_1_r_structured_information_parent_meddra_code'] = []
    d_10_8_r_past_drug_history_parent: list['D_10_8_r_past_drug_history_parent'] = []

    d_1_patient: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None

    # d_1_1_medical_record_number_source
    d_1_1_1_medical_record_number_source_gp: str | t.Literal[NF.MSK] | None = None
    d_1_1_2_medical_record_number_source_specialist: str | t.Literal[NF.MSK] | None = None
    d_1_1_3_medical_record_number_source_hospital: str | t.Literal[NF.MSK] | None = None
    d_1_1_4_medical_record_number_source_investigation: str | t.Literal[NF.MSK] | None = None

    # d_2_age_information

    d_2_1_date_birth: str | t.Literal[NF.MSK] | None = None  # dt

    # d_2_2_age_onset_reaction

    d_2_2a_age_onset_reaction_num: int | None = None
    d_2_2b_age_onset_reaction_unit: str | None = None  # st

    # d_2_2_1_gestation_period_reaction_foetus
    d_2_2_1a_gestation_period_reaction_foetus_num: int | None = None
    d_2_2_1b_gestation_period_reaction_foetus_unit: str | None = None  # st

    d_2_3_patient_age_group: enums.D_2_3_patient_age_group | None = None

    d_3_body_weight: Decimal | None = None
    d_4_height: int | None = None
    d_5_sex: enums.D_5_sex | t.Literal[NF.MSK, NF.UNK, NF.ASKU, NF.NASK] | None = None
    d_6_last_menstrual_period_date: str | None = None  # dt

    # d_7_medical_history
    d_7_2_text_medical_history: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None
    d_7_3_concomitant_therapies: t.Literal[True] | None = None

    # d_9_case_death
    d_9_1_date_death: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_9_3_autopsy: bool | t.Literal[NF.ASKU, NF.NASK, NF.UNK] | None = None

    # d_10_information_concerning_parent

    d_10_1_parent_identification: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None

    # d_10_2_parent_age_information

    d_10_2_1_date_birth_parent: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt

    # d_10_2_2_age_parent
    d_10_2_2a_age_parent_num: int | None = None
    d_10_2_2b_age_parent_unit: str | None = None  # st

    d_10_3_last_menstrual_period_date_parent: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_10_4_body_weight_parent: Decimal | None = None
    d_10_5_height_parent: int | None = None
    d_10_6_sex_parent: enums.D_10_6_sex_parent | t.Literal[NF.UNK, NF.MSK, NF.ASKU, NF.NASK] | None = None

    # d_10_7_medical_history_parent
    d_10_7_2_text_medical_history_parent: str | None = None


class D_7_1_r_structured_information_medical_history(DomainModel):
    d_7_1_r_1a_meddra_version_medical_history: str | None = None  # st
    d_7_1_r_1b_medical_history_meddra_code: int | None = None
    d_7_1_r_2_start_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt  # dt
    d_7_1_r_3_continuing: bool | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None
    d_7_1_r_4_end_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt  # dt
    d_7_1_r_5_comments: str | None = None
    d_7_1_r_6_family_history: t.Literal[True] | None = None


class D_8_r_past_drug_history(DomainModel):
    d_8_r_1_name_drug: str | t.Literal[NF.UNK, NF.NA] | None = None

    # d_8_r_2_mpid
    d_8_r_2a_mpid_version: str | None = None  # st
    d_8_r_2b_mpid: str | None = None  # st

    # d_8_r_3_phpid
    d_8_r_3a_phpid_version: str | None = None  # st
    d_8_r_3b_phpid: str | None = None  # st

    d_8_r_4_start_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_8_r_5_end_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt

    # d_8_r_6_indication_meddra_code
    d_8_r_6a_meddra_version_indication: str | None = None  # st
    d_8_r_6b_indication_meddra_code: int | None = None

    # d_8_r_7_reaction_meddra_code
    d_8_r_7a_meddra_version_reaction: str | None = None  # st
    d_8_r_7b_reaction_meddra_code: int | None = None


class D_9_2_r_cause_death(DomainModel):
    d_9_2_r_1a_meddra_version_cause_death: str | None = None  # st
    d_9_2_r_1b_cause_death_meddra_code: int | None = None
    d_9_2_r_2_cause_death: str | None = None


class D_9_4_r_autopsy_determined_cause_death(DomainModel):
    d_9_4_r_1a_meddra_version_autopsy_determined_cause_death: str | None = None  # st
    d_9_4_r_1b_autopsy_determined_cause_death_meddra_code: int | None = None
    d_9_4_r_2_autopsy_determined_cause_death: str | None = None


class D_10_7_1_r_structured_information_parent_meddra_code(DomainModel):
    d_10_7_1_r_1a_meddra_version_medical_history: str | None = None  # st
    d_10_7_1_r_1b_medical_history_meddra_code: int | None = None
    d_10_7_1_r_2_start_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_10_7_1_r_3_continuing: bool | t.Literal[NF.MSK, NF.ASKU, NF.NASK, NF.UNK] | None = None
    d_10_7_1_r_4_end_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_10_7_1_r_5_comments: str | None = None


class D_10_8_r_past_drug_history_parent(DomainModel):
    d_10_8_r_1_name_drug: str | None = None

    # d_10_8_r_2_mpid
    d_10_8_r_2a_mpid_version: str | None = None  # st
    d_10_8_r_2b_mpid: str | None = None  # st

    # d_10_8_r_3_phpid
    d_10_8_r_3a_phpid_version: str | None = None  # st
    d_10_8_r_3b_phpid: str | None = None  # st

    d_10_8_r_4_start_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    d_10_8_r_5_end_date: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt

    # d_10_8_r_6_indication_meddra_code
    d_10_8_r_6a_meddra_version_indication: str | None = None  # st
    d_10_8_r_6b_indication_meddra_code: int | None = None

    # d_10_8_r_7_reactions_meddra_code
    d_10_8_r_7a_meddra_version_reaction: str | None = None  # st
    d_10_8_r_7b_reactions_meddra_code: int | None = None


# E_i_reaction_event


class E_i_reaction_event(DomainModel):
    uuid: UUID | None = None

    # e_i_1_reaction_primary_source

    # e_i_1_1_reaction_primary_source_native_language
    e_i_1_1a_reaction_primary_source_native_language: str | None = None
    e_i_1_1b_reaction_primary_source_language: str | None = None  # st

    e_i_1_2_reaction_primary_source_translation: str | None = None

    # e_i_2_1_reaction_meddra_code
    e_i_2_1a_meddra_version_reaction: str | None = None  # st
    e_i_2_1b_reaction_meddra_code: int | None = None

    e_i_3_1_term_highlighted_reporter: enums.E_i_3_1_term_highlighted_reporter | None = None

    # e_i_3_2_seriousness_criteria_event_level
    e_i_3_2a_results_death: t.Literal[True] | t.Literal[NF.NI] | None = None
    e_i_3_2b_life_threatening: t.Literal[True] | t.Literal[NF.NI] | None = None
    e_i_3_2c_caused_prolonged_hospitalisation: t.Literal[True] | t.Literal[NF.NI] | None = None
    e_i_3_2d_disabling_incapacitating: t.Literal[True] | t.Literal[NF.NI] | None = None
    e_i_3_2e_congenital_anomaly_birth_defect: t.Literal[True] | t.Literal[NF.NI] | None = None
    e_i_3_2f_other_medically_important_condition: t.Literal[True] | t.Literal[NF.NI] | None = None

    e_i_4_date_start_reaction: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    e_i_5_date_end_reaction: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt

    # e_i_6_duration_reaction
    e_i_6a_duration_reaction_num: int | None = None
    e_i_6b_duration_reaction_unit: str | None = None  # st

    e_i_7_outcome_reaction_last_observation: enums.E_i_7_outcome_reaction_last_observation | None = None
    e_i_8_medical_confirmation_healthcare_professional: bool | None = None
    e_i_9_identification_country_reaction: str | None = None  # st

    @classmethod
    def _post_validate(cls, processor: pde.PostValidationProcessor) -> None:
        processor.try_validate_fields(
            error_message='Both id and uuid cannot be specified',
            is_add_single_error=True,
            validate=lambda id, uuid:
                id is None or uuid is None
        )


# F_r_results_tests_procedures_investigation_patient


class F_r_results_tests_procedures_investigation_patient(DomainModel):
    f_r_1_test_date: str | t.Literal[NF.UNK] | None = None  # dt  # dt

    # f_r_2_test_name

    f_r_2_1_test_name: str | None = None

    # f_r_2_2_test_name_meddra_code
    f_r_2_2a_meddra_version_test_name: str | None = None  # st
    f_r_2_2b_test_name_meddra_code: int | None = None

    # f_r_3_test_result
    f_r_3_1_test_result_code: enums.F_r_3_1_test_result_code | None = None
    f_r_3_2_test_result_val_qual: Decimal | t.Literal[NF.NINF, NF.PINF] | None = None  # TODO: check how qualifiers are used
    f_r_3_3_test_result_unit: str | None = None  # st
    f_r_3_4_result_unstructured_data: str | None = None

    f_r_4_normal_low_value: str | None = None
    f_r_5_normal_high_value: str | None = None
    f_r_6_comments: str | None = None
    f_r_7_more_information_available: bool | None = None


# G_k_drug_information


class G_k_drug_information(DomainModel):
    g_k_2_3_r_substance_id_strength: list['G_k_2_3_r_substance_id_strength'] = []
    g_k_4_r_dosage_information: list['G_k_4_r_dosage_information'] = []
    g_k_7_r_indication_use_case: list['G_k_7_r_indication_use_case'] = []
    g_k_9_i_drug_reaction_matrix: list['G_k_9_i_drug_reaction_matrix'] = []
    g_k_10_r_additional_information_drug: list['G_k_10_r_additional_information_drug'] = []

    g_k_1_characterisation_drug_role: enums.G_k_1_characterisation_drug_role | None = None

    # g_k_2_drug_identification

    # g_k_2_1_mpid_phpid
    g_k_2_1_1a_mpid_version: str | None = None  # st
    g_k_2_1_1b_mpid: str | None = None  # st
    g_k_2_1_2a_phpid_version: str | None = None  # st
    g_k_2_1_2b_phpid: str | None = None  # st

    g_k_2_2_medicinal_product_name_primary_source: str | None = None
    g_k_2_4_identification_country_drug_obtained: str | None = None  # st
    g_k_2_5_investigational_product_blinded: t.Literal[True] | None = None

    # g_k_3_holder_authorisation_application_number_drug
    g_k_3_1_authorisation_application_number: str | None = None  # st
    g_k_3_2_country_authorisation_application: str | None = None  # st
    g_k_3_3_name_holder_applicant: str | None = None

    # g_k_5_cumulative_dose_first_reaction
    g_k_5a_cumulative_dose_first_reaction_num: Decimal | None = None
    g_k_5b_cumulative_dose_first_reaction_unit: str | None = None  # st

    # g_k_6_gestation_period_exposure
    g_k_6a_gestation_period_exposure_num: Decimal | None = None
    g_k_6b_gestation_period_exposure_unit: str | None = None  # st

    g_k_8_action_taken_drug: enums.G_k_8_action_taken_drug | None = None

    g_k_11_additional_information_drug: str | None = None

    @classmethod
    def _post_validate(cls, processor: pde.PostValidationProcessor):
        processor.try_validate_fields(
            error_message='Cannot have duplicate drug to reaction relations',
            validate=lambda g_k_9_i_drug_reaction_matrix:
                len(g_k_9_i_drug_reaction_matrix) == 
                len(set(x.g_k_9_i_1_reaction_assessed for x in g_k_9_i_drug_reaction_matrix))
        )


class G_k_2_3_r_substance_id_strength(DomainModel):
    g_k_2_3_r_1_substance_name: str | None = None
    g_k_2_3_r_2a_substance_termid_version: str | None = None  # st
    g_k_2_3_r_2b_substance_termid: str | None = None  # st
    g_k_2_3_r_3a_strength_num: Decimal | None = None  # TODO: int or decimal?
    g_k_2_3_r_3b_strength_unit: str | None = None  # st


class G_k_4_r_dosage_information(DomainModel):
    g_k_4_r_1a_dose_num: Decimal | None = None
    g_k_4_r_1b_dose_unit: str | None = None  # st
    g_k_4_r_2_number_units_interval: Decimal | None = None
    g_k_4_r_3_definition_interval_unit: str | None = None  # st
    g_k_4_r_4_date_time_drug: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt
    g_k_4_r_5_date_time_last_administration: str | t.Literal[NF.MSK, NF.ASKU, NF.NASK] | None = None  # dt

    # g_k_4_r_6_duration_drug_administration
    g_k_4_r_6a_duration_drug_administration_num: Decimal | None = None
    g_k_4_r_6b_duration_drug_administration_unit: str | None = None  # st

    g_k_4_r_7_batch_lot_number: str | None = None
    g_k_4_r_8_dosage_text: str | None = None

    # g_k_4_r_9_pharmaceutical_dose_form

    g_k_4_r_9_1_pharmaceutical_dose_form: str | t.Literal[NF.ASKU, NF.NASK, NF.UNK] | None = None
    g_k_4_r_9_2a_pharmaceutical_dose_form_termid_version: str | None = None  # st
    g_k_4_r_9_2b_pharmaceutical_dose_form_termid: str | None = None  # st

    # g_k_4_r_10_route_administration
    g_k_4_r_10_1_route_administration: str | t.Literal[NF.ASKU, NF.NASK, NF.UNK] | None = None
    g_k_4_r_10_2a_route_administration_termid_version: str | None = None  # st
    g_k_4_r_10_2b_route_administration_termid: str | None = None  # st

    # g_k_4_r_11_parent_route_administration
    g_k_4_r_11_1_parent_route_administration: str | t.Literal[NF.ASKU, NF.NASK, NF.UNK] | None = None
    g_k_4_r_11_2a_parent_route_administration_termid_version: str | None = None  # st
    g_k_4_r_11_2b_parent_route_administration_termid: str | None = None  # st


class G_k_7_r_indication_use_case(DomainModel):
    g_k_7_r_1_indication_primary_source: str | t.Literal[NF.ASKU, NF.NASK, NF.UNK] | None = None

    # g_k_7_r_2_indication_meddra_code
    g_k_7_r_2a_meddra_version_indication: str | None = None  # st
    g_k_7_r_2b_indication_meddra_code: int | None = None


class G_k_9_i_drug_reaction_matrix(DomainModel):
    g_k_9_i_2_r_assessment_relatedness_drug_reaction: list['G_k_9_i_2_r_assessment_relatedness_drug_reaction'] = []

    # This field stores id of related reaction
    g_k_9_i_1_reaction_assessed: int | UUID

    # g_k_9_i_3_interval_drug_administration_reaction
    g_k_9_i_3_1a_interval_drug_administration_reaction_num: Decimal | None = None
    g_k_9_i_3_1b_interval_drug_administration_reaction_unit: str | None = None  # st
    g_k_9_i_3_2a_interval_last_dose_drug_reaction_num: Decimal | None = None
    g_k_9_i_3_2b_interval_last_dose_drug_reaction_unit: str | None = None  # st

    g_k_9_i_4_reaction_recur_readministration: enums.G_k_9_i_4_reaction_recur_readministration | None = None


class G_k_9_i_2_r_assessment_relatedness_drug_reaction(DomainModel):
    g_k_9_i_2_r_1_source_assessment: str | None = None
    g_k_9_i_2_r_2_method_assessment: str | None = None
    g_k_9_i_2_r_3_result_assessment: str | None = None


class G_k_10_r_additional_information_drug(DomainModel):
    g_k_10_r_additional_information_drug: enums.G_k_10_r_additional_information_drug | None = None


# H_narrative_case_summary


class H_narrative_case_summary(DomainModel):
    h_3_r_sender_diagnosis_meddra_code: list['H_3_r_sender_diagnosis_meddra_code'] = []
    h_5_r_case_summary_reporter_comments_native_language: list['H_5_r_case_summary_reporter_comments_native_language'] = []

    h_1_case_narrative: str | None = None
    h_2_reporter_comments: str | None = None

    h_4_sender_comments: str | None = None


class H_3_r_sender_diagnosis_meddra_code(DomainModel):
    h_3_r_1a_meddra_version_sender_diagnosis: str | None = None  # st
    h_3_r_1b_sender_diagnosis_meddra_code: int | None = None


class H_5_r_case_summary_reporter_comments_native_language(DomainModel):
    h_5_r_1a_case_summary_reporter_comments_text: str | None = None
    h_5_r_1b_case_summary_reporter_comments_language: str | None = None  # st
