/// Implement the backend module in Rust.
use dicom_dictionary_std::uids::VERIFICATION;
use dicom_ul::ClientAssociationOptions;
use pyo3::prelude::*;

/// Send `C-ECHO` requests to a DICOM service class provider.
///
/// Args:
///   address (str): The address of the DICOM SCP
///   called_ae_title (str): The called AE title; defaults to "ANY-SCP"
///   calling_ae_title (str): The calling AE title; defaults to "ECHOSCU"
///   message_id (int): The message ID; defaults to 1
#[pyclass(module = "backend", get_all)]
#[derive(Debug)]
struct CEchoRequest {
    address: String,
    called_ae_title: String,
    calling_ae_title: String,
    message_id: u16,
}

#[pymethods]
impl CEchoRequest {
    #[new]
    #[pyo3(
        signature = (
            address,
            /,
            called_ae_title="ANY-SCP".into(),
            calling_ae_title="ECHOSCU".into(),
            message_id=1
        )
    )]
    fn new(
        address: String,
        called_ae_title: String,
        calling_ae_title: String,
        message_id: u16,
    ) -> Self {
        CEchoRequest {
            address,
            called_ae_title,
            calling_ae_title,
            message_id,
        }
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __str__(&self) -> String {
        format!(
            r#"Request(address="{}", called_ae_title="{}", calling_ae_title="{}", message_id="{}")"#,
            self.address, self.called_ae_title, self.calling_ae_title, self.message_id
        )
    }

    /// Send the `C-ECHO` request and return the response's status.
    #[pyo3(text_signature = "() -> int")]
    fn send(&self) -> u8 {
        let association_opt = ClientAssociationOptions::new()
            .with_abstract_syntax(VERIFICATION)
            .calling_ae_title(&self.calling_ae_title)
            .called_ae_title(&self.called_ae_title);

        let association = association_opt.establish_with(&self.address).expect(
            format!(
                "A-ASSOCIATE service should establish association for {:?}",
                self
            )
            .as_str(),
        );

        println!("Association established: {:?}", association);
        0
    }
}

/// Formats the sum of two numbers as string.
#[pyfunction(name = "do_sum", text_signature = "(a: c_uint, b: c_uint) -> str")]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn backend(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<CEchoRequest>()?;
    Ok(())
}
