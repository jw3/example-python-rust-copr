rulec
===

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/)

[fapolicyd](https://github.com/linux-application-whitelisting/fapolicyd) rule compiler using the [`fapolicy-rules`](https://crates.io/crates/fapolicy-rules) crate from [fapolicy-analyzer](https://github.com/ctc-oss/fapolicy-analyzer)

This is mostly a toy project for experimenting with building Python+Rust RPMs.

## Sample

```text
#! python -m rulec sample.invalid.rules 
Error: 
   ╭─[sample.rules:1:1]
   │
 1 │ allow perm=any uid=0 trust=x : all
   ·                            ┬  
   ·                            ╰── Expected boolean (0, 1) value
───╯
Error: 
   ╭─[sample.rules:2:1]
   │
 2 │ allow perm=xany uid=1000 trust=1 : all
   ·            ──┬─  
   ·              ╰─── Expected one of 'any', 'open', 'execute'
───╯
Error: 
   ╭─[sample.rules:4:1]
   │
 4 │ xdeny_syslog perm=execute all : all
   · ──────┬─────  
   ·       ╰─────── Unknown Decision
───╯
```

## lock2spec.py

The [lock2spec](lock2spec.py) script creates a set of dependency links for the spec file.

The logic goes like this
1. Parse all dependencies from the `Cargo.lock`
2. Check available Fedora (rawhide) packages for availability, list available packages as `BuildRequires: `
3. Packages not found in Fedora are SourceX using the `crates_source` macro, `SourceX: %{crates_source _}`
4. Allow for overriding some packages to resolve discrepancies
   - the usecase for this was where the Fedora packagers for pyo3 patched it at rpm build time, causing different dependency graph that is found in the official release of pyo3

## Testing build from Podman

1. `podman build --security-opt seccomp=unconfined -t rpm-test:rawhide .`
2. `podman run --rm -it --security-opt seccomp=unconfined rpm-test:rawhide`

## References
- https://docs.fedoraproject.org/en-US/packaging-guidelines/
  - https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/
  - https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
- https://whamcloud.github.io/Online-Help/docs/Contributor_Docs/cd_Building_Rust_RPMs.html
- https://pagure.io/fedora-rust/rust2rpm
  - https://pagure.io/fedora-rust/rust2rpm/blob/main/f/data
- https://src.fedoraproject.org/rpms/pyproject-rpm-macros
- https://mirrors.kernel.org/fedora/development/rawhide/Everything/source/tree/Packages/
- Similar Python + Rust project
  - https://github.com/pyca/cryptography
  - https://src.fedoraproject.org/rpms/python-cryptography
  - https://mirrors.kernel.org/fedora/development/rawhide/Everything/source/tree/Packages/p/python-cryptography-37.0.2-4.fc37.src.rpm
- https://doc.rust-lang.org/rustc/command-line-arguments.html#--remap-path-prefix-remap-source-names-in-output
- https://github.com/rpm-software-management/rpm/blob/master/scripts/check-buildroot

## License

GPL v3
