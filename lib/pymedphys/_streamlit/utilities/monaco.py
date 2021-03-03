# pylint: disable = pointless-statement, pointless-string-statement
# pylint: disable = no-value-for-parameter, expression-not-assigned
# pylint: disable = too-many-lines, redefined-outer-name

import os
import pathlib

from pymedphys._imports import streamlit as st

from pymedphys._monaco import patient as mnc_patient
from pymedphys._streamlit.utilities import exceptions as _exceptions

from . import exceptions, misc


def monaco_tel_files_picker(
    config,
    patient_id="",
    key_namespace="",
    advanced_mode=False,
    site=None,
    plan_selection_text="",
):
    (
        monaco_site,
        monaco_directory,
        patient_id,
        plan_directory,
        patient_directory,
    ) = monaco_patient_directory_picker(
        config, patient_id, key_namespace, advanced_mode, site
    )

    patient_name = read_monaco_patient_name(str(patient_directory))

    st.write(f"Patient Name: `{patient_name}`")

    all_tel_paths = list(plan_directory.glob("**/*tel.1"))
    all_tel_paths = sorted(all_tel_paths, key=os.path.getmtime, reverse=True)

    plan_names_to_choose_from = [
        str(path.relative_to(plan_directory)) for path in all_tel_paths
    ]

    if len(plan_names_to_choose_from) == 0:
        if patient_id != "":
            st.write(
                _exceptions.NoRecordsFound(
                    f"No Monaco plans found for patient ID {patient_id}"
                )
            )
        return {"patient_id": patient_id}

    if plan_selection_text != "":
        st.write(plan_selection_text)

    selected_monaco_plan = st.radio(
        "Select a Monaco plan",
        plan_names_to_choose_from,
        key=f"{key_namespace}_monaco_plans",
    )

    tel_paths = []

    if selected_monaco_plan is not None:
        current_plans = list(
            monaco_directory.glob(f"*~{patient_id}/plan/{selected_monaco_plan}")
        )
        current_plans = [path.resolve() for path in current_plans]
        if len(current_plans) != 1:
            st.write("Plans found:", current_plans)
            raise ValueError("Exactly one plan should have been found")
        tel_paths += current_plans

    return monaco_site, monaco_directory, patient_name, selected_monaco_plan, tel_paths


def monaco_patient_directory_picker(
    config, patient_id="", key_namespace="", advanced_mode_local=False, site=None
):
    monaco_site, monaco_directory = misc.get_site_and_directory(
        config,
        "Monaco Plan Location",
        "monaco",
        default=site,
        key=f"{key_namespace}_monaco_site",
    )

    if advanced_mode_local:
        st.write(monaco_directory.resolve())

    patient_id = st.text_input(
        "Patient ID", patient_id, key=f"{key_namespace}_patient_id"
    )
    if advanced_mode_local:
        patient_id

    if patient_id == "":
        st.stop()

    plan_directories = list(monaco_directory.glob(f"*~{patient_id}/plan"))
    if len(plan_directories) == 0:
        if patient_id != "":
            st.write(
                exceptions.NoRecordsFound(
                    f"No Monaco plan directories found for patient ID {patient_id}"
                )
            )
            st.stop()

        return {"patient_id": patient_id}
    elif len(plan_directories) > 1:
        raise ValueError(
            "More than one patient plan directory found for this ID, "
            "please only have one directory per patient. "
            "Directories found were "
            f"{', '.join([str(path.resolve()) for path in plan_directories])}"
        )

    plan_directory = plan_directories[0]
    patient_directory = pathlib.Path(plan_directory).parent

    return monaco_site, monaco_directory, patient_id, plan_directory, patient_directory


@st.cache
def read_monaco_patient_name(monaco_patient_directory):
    return mnc_patient.read_patient_name(monaco_patient_directory)
