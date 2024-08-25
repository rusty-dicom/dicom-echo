use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
#[pyo3(name = "do_sum")]
#[pyo3(text_signature = "(a: c_uint, b: c_uint) -> str")]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn backend(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
