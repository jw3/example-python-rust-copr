rulec
===

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/)

[fapolicyd](https://github.com/linux-application-whitelisting/fapolicyd) rule compiler using the [`fapolicy-rules`](https://crates.io/crates/fapolicy-rules) crate from [fapolicy-analyzer](https://github.com/ctc-oss/fapolicy-analyzer)

This is mostly a toy project for experimenting with building Python+Rust RPMs.

## Sample

```text
#! python -m rulec sample.rules 
Error: 
   ╭─[sample.rules:1:1]
   │
 1 │ allow perm=any uid=0 trust=x : all
   ·          
   ·           Expected boolean (0, 1) value
───╯
Error: 
   ╭─[sample.rules:2:1]
   │
 2 │ allow perm=xany uid=1000 trust=1 : all
   ·       
   ·        Expected one of 'any', 'open', 'execute'
───╯
Error: 
   ╭─[sample.rules:4:1]
   │
 4 │ xdeny_syslog perm=execute all : all
   · ──────┬─────  
   ·       ╰─────── Unknown Decision
───╯
```

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
- 


## License

GPL v3
