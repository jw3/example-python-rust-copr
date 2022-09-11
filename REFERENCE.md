Development references
===

## General References
- https://whamcloud.github.io/Online-Help/docs/Contributor_Docs/cd_Building_Rust_RPMs.html
- https://doc.rust-lang.org/rustc/command-line-arguments.html#--remap-path-prefix-remap-source-names-in-output
- https://github.com/rpm-software-management/rpm/blob/master/scripts/check-buildroot
- https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
- https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/packaging_and_distributing_software/index
- https://fedoraproject.org/wiki/Packaging:DistTag

## Fedora References
- Similar Python + Rust project
    - https://github.com/pyca/cryptography
    - https://src.fedoraproject.org/rpms/python-cryptography
    - https://mirrors.kernel.org/fedora/development/rawhide/Everything/source/tree/Packages/p/python-cryptography-37.0.2-4.fc37.src.rpm
- https://mirrors.kernel.org/fedora/development/rawhide/Everything/source/tree/Packages/
- https://pagure.io/fedora-rust/rust2rpm
    - https://pagure.io/fedora-rust/rust2rpm/blob/main/f/data
- https://src.fedoraproject.org/rpms/pyproject-rpm-macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/
    - https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/
    - https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/


## RHEL References
- https://access.redhat.com/documentation/en-us/red_hat_developer_tools/1/html/using_rust_1.54.0_toolset/assembly_the-cargo-build-tool#proc_vendoring-rust-project-dependencies_assembly_the-cargo-build-tool

## lock2spec.py

The [lock2spec](lock2spec.py) script creates a set of dependency links for the spec file.

The logic goes like this
1. Parse all dependencies from the `Cargo.lock`
2. Check available Fedora (rawhide) packages for availability, list available packages as `BuildRequires: `
3. Packages not found in Fedora are SourceX using the `crates_source` macro, `SourceX: %{crates_source _}`
4. Allow for overriding some packages to resolve discrepancies
    - the usecase for this was where the Fedora packagers for pyo3 patched it at rpm build time, causing different dependency graph that is found in the official release of pyo3
