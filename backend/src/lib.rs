//! Implement the `dicom_echo.backend` module in Rust.
use dicom_core::{dicom_value, DataElement, VR};
use dicom_dictionary_std::{
    tags,
    uids::{self, VERIFICATION},
};
use dicom_object::{mem::InMemDicomObject, StandardDataDictionary};
use dicom_transfer_syntax_registry::entries::IMPLICIT_VR_LITTLE_ENDIAN;
use dicom_ul::{
    association::ClientAssociationOptions,
    pdu::{PDataValue, PDataValueType, Pdu},
};
use pyo3::prelude::*;

use client_exceptions::Result;

/// By default, specify this AE title for the target SCP.
pub const DEFAULT_CALLED_AE_TITLE: &str = "ANY-SCP";

/// By default, specify this AE title for the SCU sending the `C-ECHO` request.
pub const DEFAULT_CALLING_AE_TITLE: &str = "ECHOSCU";

/// ref: <https://github.com/Enet4/dicom-rs/blob/de7dc5831171202fb20e1928e2c7ff27c5b95f85/echoscu/src/main.rs#L177-L192>
fn create_echo_command(message_id: u16) -> InMemDicomObject<StandardDataDictionary> {
    InMemDicomObject::command_from_element_iter([
        // service
        DataElement::new(tags::AFFECTED_SOP_CLASS_UID, VR::UI, uids::VERIFICATION),
        // command
        DataElement::new(tags::COMMAND_FIELD, VR::US, dicom_value!(U16, [0x0030])),
        // message ID
        DataElement::new(tags::MESSAGE_ID, VR::US, dicom_value!(U16, [message_id])),
        // data set type
        DataElement::new(
            tags::COMMAND_DATA_SET_TYPE,
            VR::US,
            dicom_value!(U16, [0x0101]),
        ),
    ])
}

/// Send a `C-ECHO` message to the given address.
///
/// Reference: [DICOM Standard Part 7, Section 9.1.5](https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5)
#[pyfunction]
#[pyo3(
    signature = (
        address, /,
        called_ae_title=DEFAULT_CALLED_AE_TITLE.into(), calling_ae_title=DEFAULT_CALLING_AE_TITLE.into(),
        message_id=1
    ),
    text_signature = "(address: str, /, called_ae_title: str = DEFAULT_CALLED_AE_TITLE, calling_ae_title: str = DEFAULT_CALLING_AE_TITLE, message_id: int = 1) -> int"
)]
pub fn send(
    address: &str,
    called_ae_title: &str,
    calling_ae_title: &str,
    message_id: u16,
) -> Result<u16> {
    let mut association = ClientAssociationOptions::new()
        .with_abstract_syntax(VERIFICATION)
        .calling_ae_title(calling_ae_title)
        .called_ae_title(called_ae_title)
        .establish_with(address)?;

    let presentation_context = association.presentation_contexts().first().unwrap();
    let dicom_object = create_echo_command(message_id);

    let mut data = Vec::new();
    let transfer_syntax = IMPLICIT_VR_LITTLE_ENDIAN.erased();

    dicom_object
        .write_dataset_with_ts(&mut data, &transfer_syntax)
        .expect("in-memory dicom object should be serialized to byte vector");

    association.send(&Pdu::PData {
        data: vec![PDataValue {
            presentation_context_id: presentation_context.id,
            value_type: PDataValueType::Command,
            is_last: true,
            data,
        }],
    })?;

    let pdu = association.receive()?;

    match pdu {
        Pdu::PData { data } => {
            let data_value = &data[0];
            let v = &data_value.data;
            let obj = InMemDicomObject::read_dataset_with_ts(v.as_slice(), &transfer_syntax)
                .expect("should be able to read the response dataset returned by the SCP");

            let status = obj
                .element(tags::STATUS)
                .expect("response should include the status tag")
                .to_int::<u16>()
                .expect("status tag should be decoded to a u16");
            Ok(status)
        }
        _ => {
            panic!("unexpected response from SCP");
        }
    }
}

#[pymodule]
fn backend(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(send, m)?)?;
    m.add("DEFAULT_CALLED_AE_TITLE", DEFAULT_CALLED_AE_TITLE)?;
    m.add("DEFAULT_CALLING_AE_TITLE", DEFAULT_CALLING_AE_TITLE)?;
    Ok(())
}

pub mod client_exceptions;
