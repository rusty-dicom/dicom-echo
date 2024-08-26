/// Implement the backend module in Rust.
// TODO: use dicom_ul::ClientAssociation;
use pyo3::prelude::*;

/// Parameters for the C-STORE request
#[pyclass(module = "backend", get_all)]
#[derive(Debug)]
struct Request {
    address: String,
    called_ae_title: String,
    calling_ae_title: String,
    message_id: u16,
}

#[pymethods]
impl Request {
    #[new]
    fn new(
        address: String,
        called_ae_title: String,
        calling_ae_title: String,
        message_id: u16,
    ) -> Self {
        Request {
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

    fn send(&self) -> u8 {
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
    m.add_class::<Request>()?;
    Ok(())
}
