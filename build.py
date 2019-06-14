from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    remotes = [("https://api.bintray.com/conan/bincrafters/public-conan", "yes", "bincrafters"),
               ("https://api.bintray.com/conan/conan-community/conan", "yes", "conan-community"),
               ("https://api.bintray.com/conan/appimage-conan-community/public-conan", "yes", "appimage")]

    command = "sudo apt-get -qq update && sudo apt-get -qq install -y gtk-doc-tools"
    builder = ConanMultiPackager(build_policy="outdated", remotes=remotes, docker_entry_script=command)
    builder.add_common_builds(shared_option_name="librsvg:shared")
    builder.run()
