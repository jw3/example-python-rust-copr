use fapolicy_rules::db::Entry;
use fapolicy_rules::db::Entry::{Invalid, InvalidSet};
use fapolicy_rules::{load, read};
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use std::collections::BTreeMap;
use std::path::PathBuf;

mod error;
mod rule_check;

#[pyfunction]
fn validate_rules_at(rules_path: &str) -> PyResult<()> {
    let rule_source = load::rules_from_disk(rules_path)
        .map_err(|e| PyRuntimeError::new_err(format!("{:?}", e)))?;

    let contents: BTreeMap<PathBuf, Vec<String>> =
        rule_source
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

    let db =
        read::load_rules_db(rules_path).map_err(|e| PyRuntimeError::new_err(format!("{:?}", e)))?;

    if db.iter().any(|(_, (_, e))| !is_valid(e)) {
        return Err(PyRuntimeError::new_err("Rule validation failed"));
    }

    for (_, (_, e)) in db.iter() {
        println!("{}", e);
    }
    Ok(())
}

fn is_valid(def: &Entry) -> bool {
    !matches!(def, Invalid { .. } | InvalidSet { .. })
}

#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_rules_at, m)?)?;
    Ok(())
}
