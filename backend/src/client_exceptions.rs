//! Map [`dicom_ul::association::client::Error`] to Python exceptions.
//!
//! Reference: [Foreign Rust error types | Error handling — PyO3 user guide]
//!
//! [`dicom_ul::association::client::Error`]: dicom_ul::association::client::Error
//! [Foreign Rust error types | Error handling — PyO3 user guide]: https://pyo3.rs/v0.22.2/function/error-handling#foreign-rust-error-types

use dicom_ul::association::client::Error as ClientError;

use pyo3::exceptions::{PyConnectionError, PyValueError};
use pyo3::PyErr;

/// Use composition to wrap the [`ClientError`] type in a struct that implements [`PyErr`].
pub struct Error {
    source: ClientError,
}

impl From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        match err.source {
            ClientError::Rejected { .. } => PyValueError::new_err(err.source.to_string()),
            _ => PyConnectionError::new_err(err.source.to_string()),
        }
    }
}

impl From<ClientError> for Error {
    fn from(other: ClientError) -> Self {
        Self { source: other }
    }
}

/// This type automatically converts a [`ClientError`] to a Python exception when used by a function.
pub type Result<T, E = Error> = std::result::Result<T, E>;
