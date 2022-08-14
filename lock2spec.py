import toml
import requests as req
from bs4 import BeautifulSoup

rawhide_rust = "https://mirrors.kernel.org/fedora/development/rawhide/Everything/source/tree/Packages/r/"


def required_packages():
    project_name = "example-rulec"
    with open('Cargo.lock') as lock:
        packages = toml.load(lock)["package"]
        required = {}
        for pkg in packages:
            name = pkg["name"]
            if name != project_name:
                version = pkg["version"]
                (major, minor, patch) = version.split(".", 2)
                required[name] = version
        return required


def available_packages():
    soup = BeautifulSoup(req.get(rawhide_rust).text)
    links = soup.find_all('a')

    available = {}
    for link in links:
        if link.text.startswith("rust-"):
            try:
                # rust-zstd-safe-4.1.4-2.fc37.src.rpm
                (name, version) = link.text.split("-", 1)[1].rsplit("-", 1)[0].rsplit("-", 1)
            except:
                continue

            available[name] = version
    return available


if __name__ == '__main__':
    rpms = {}
    crates = {}
    available = available_packages()
    for p, v in required_packages().items():
        if p in available:
            if v == available[p]:
                rpms[p] = f"rust-{p}"
            else:
                print("rpm version didnt match")
                crates[p] = f"%{{crates_source {p} {v}}}"
        else:
            crates[p] = f"%{{crates_source {p} {v}}}"
        # Source1: %{crates_source lmdb-rkv 0.14.0}
        #print(f"Source{i+1}: %{{crates_source {p} {v}}}")

    print("BuildRequires:  rust-packaging")
    for r in rpms.values():
        print(f"BuildRequires: {r}-devel")
    for i, c in enumerate(crates.values()):
        print(f"Source{i + 1}: {c}")
