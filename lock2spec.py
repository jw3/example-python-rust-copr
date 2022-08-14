import toml


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


if __name__ == '__main__':
    print("BuildRequires:  rust-packaging")
    for i, (p, v) in enumerate(required_packages().items()):
        # Source1: %{crates_source lmdb-rkv 0.14.0}
        print(f"Source{i+1}: %{{crates_source {p} {v}}}")
