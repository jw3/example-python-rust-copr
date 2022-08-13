rulec
===

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jwass3/example-rust-python/package/python-rulec/)

Rule compiler for fapolicyd

## Testing build from Podman

1. `podman build --security-opt seccomp=unconfined -t rpm-test:rawhide .`
2. `podman run --rm -it --security-opt seccomp=unconfined rpm-test:rawhide ./build.sh`

## License

GPL v3
