vendor:
	cargo check
	git archive HEAD -o rulec.tar.gz --prefix=example-python-rust-copr
	./vendor.sh

srpm: vendor
	mkdir -p /tmp/rpmbuild/SOURCES
	cp crates.tar.gz rulec.tar.gz /tmp/rpmbuild/SOURCES
	rpmbuild -bs -D "_topdir /tmp/rpmbuild" \$(spec)
	mkdir -p \$(outdir)
	cp -v /tmp/rpmbuild/SRPMS/* \$(outdir)/
