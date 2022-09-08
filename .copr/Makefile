vendor:
	cargo check
	git archive HEAD -o rulec.tar.gz --prefix=example-python-rust-copr
	./vendor.sh

srpm: vendor
	dnf -y install tito
	tito init
	tito build --srpm --output=/tmp/srpm
