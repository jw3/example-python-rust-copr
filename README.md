rulec
===

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/)

Rule compiler for fapolicyd

## Testing build from Podman

1. `podman build --security-opt seccomp=unconfined -t rpm-test:rawhide .`
2. `podman run --rm -it --security-opt seccomp=unconfined rpm-test:rawhide ./build.sh`

## References
- https://docs.fedoraproject.org/en-US/packaging-guidelines/
  - https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/
  - https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
- https://whamcloud.github.io/Online-Help/docs/Contributor_Docs/cd_Building_Rust_RPMs.html
- https://pagure.io/fedora-rust/rust2rpm
  - https://pagure.io/fedora-rust/rust2rpm/blob/main/f/data
- https://src.fedoraproject.org/rpms/pyproject-rpm-macros
- 


## License

GPL v3
