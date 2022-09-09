.PHONY : clean vendor srpm

clean:
	rm rulec.tar.gz
	rm crates.tar.gz

vendor:
	dnf install -y git rust-packaging python3-devel && python -m pip install -r lock2spec.requirements.txt || true
	cargo check
	git archive HEAD -o rulec.tar.gz --prefix=python3-rulec/
	./vendor.sh

srpm: vendor
	mkdir -p /tmp/rpmbuild/SOURCES
	cp crates.tar.gz rulec.tar.gz /tmp/rpmbuild/SOURCES
	rpmbuild -bs -D "_topdir /tmp/rpmbuild" \$(spec)
	mkdir -p \$(outdir)
	cp -v /tmp/rpmbuild/SRPMS/* \$(outdir)/
