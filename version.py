def main():
    with open("app/templates/base.html", "r") as f:
        data = f.read()
    vidx = data.find("CryptoFinder v0.") + 16
    txt_version = data[vidx:vidx+2]
    version = int(txt_version)
    version += 1
    new_version = str(version)
    if len(new_version) < len(txt_version):
        new_version = "0" + new_version
    data = data.replace(data[vidx:vidx+2], new_version)
    with open("app/templates/base.html", "w") as f:
        f.write(data)
    print(f"Updated version to v0.{new_version}")


if __name__ == "__main__":
    main()
