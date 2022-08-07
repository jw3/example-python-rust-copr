use pyo3::prelude::*;

use pyo3::{wrap_pyfunction, PyResult, Python};

#[pyfunction]
fn hello() {
    println!("rust")
}

#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    Ok(())
}
