use fapolicy_rules::load;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use std::collections::BTreeMap;
use std::path::PathBuf;

mod rule_check;

#[pyfunction]
fn validate_rules_at(rules_path: &str) -> PyResult<()> {
    let contents: BTreeMap<PathBuf, Vec<String>> = load::rules_from_disk(rules_path)
        .map_err(|e| PyRuntimeError::new_err(format!("{:?}", e)))?
        .into_iter()
        .fold(BTreeMap::new(), |mut x, (p, t)| {
            if !x.contains_key(&p) {
                x.insert(p.clone(), vec![]);
            }
            x.get_mut(&p).unwrap().push(t);
            x
        });

    for (file, _) in contents {
        rule_check::report_for_file(file)
            .map_err(|e| PyRuntimeError::new_err(format!("{:?}", e)))?;
    }
    Ok(())
}

#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_rules_at, m)?)?;
    Ok(())
}
