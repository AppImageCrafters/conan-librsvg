from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    remotes = [("https://api.bintray.com/conan/bincrafters/public-conan", "yes", "bincrafters"),
               ("https://api.bintray.com/conan/conan-community/conan", "yes", "conan-community"),
               ("https://api.bintray.com/conan/appimage-conan-community/public-conan", "yes", "appimage")]

    builder = ConanMultiPackager(build_policy="outdated", remotes=remotes)
    builder.add_common_builds(shared_option_name="librsvg:shared")
    builder.run()
