#!/usr/bin/env bash

rm -rf vendor
cargo vendor-filterer --platform=x86_64-unknown-linux-gnu
./lock2spec.py
tar cvzf crates.tar.gz -C vendor .
du -sh crates.tar.gz
