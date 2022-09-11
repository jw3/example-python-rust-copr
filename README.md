python-rulec
===

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/)

[File Access Policy](https://github.com/linux-application-whitelisting/fapolicyd) rule compiler.

Like [fagenrules](https://github.com/linux-application-whitelisting/fapolicyd/blob/main/init/fagenrules), with validation using the [fapolicy-rules](https://crates.io/crates/fapolicy-rules) crate from [fapolicy-analyzer](https://github.com/ctc-oss/fapolicy-analyzer)

This is mostly a toy project for experimenting with RPM builds using Python+Rust+Copr.

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

## With Copr

```text
dnf copr enable jwass3/example-rust-python
dnf install python-rulec
```

## With Podman

```text
vendor.sh
podman build --security-opt seccomp=unconfined -t rulec:rawhide .
podman run --rm -it rulec:rawhide
```

## License

GPL v3
