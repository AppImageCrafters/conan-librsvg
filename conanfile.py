from conans import ConanFile, AutoToolsBuildEnvironment, tools
from shutil import copyfile
import os


class LibrsvgConan(ConanFile):
    name = "librsvg"
    version = "2.40.20"
    license = "GPLv2"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/appimage-conan-community/conan-librsvg/issues"
    description = "A library to render SVG images to Cairo surfaces."
    topics = ("svg", "render", "image")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = ("glib/2.40.0@appimage-conan-community/stable", "cairo/1.17.2@appimage-conan-community/stable",
                "pango/1.40.6@appimage-conan-community/stable", "harfbuzz/2.4.0@appimage-conan-community/stable",
                "libxml2/2.9.9@bincrafters/stable")
    generators = "pkg_config"

    def source(self):
        self.run("git clone https://gitlab.gnome.org/GNOME/librsvg.git -b " + self.version)

    def conanArchToSystem(self, conan_arch):
        if conan_arch == "x86":
            return "i386"
        if conan_arch == "x86_64":
            return "amd64"

    def system_requirements(self):
        pkgs_name = None
        system_arch = self.conanArchToSystem(self.settings.arch)
        if tools.os_info.linux_distro == "ubuntu":
            pkgs_name = [
                "make:%s" % system_arch,
                "automake:%s" % system_arch,
                "autoconf:%s" % system_arch,
                "libtool:%s" % system_arch,
                "gettext:%s" % system_arch,
                "itstool:%s" % system_arch,
                "libffi-dev:%s" % system_arch,
                "gtk-doc-tools:%s" % system_arch,
                "libcroco3-dev:%s" % system_arch,
                "libgdk-pixbuf2.0-dev:%s" % system_arch,
                "gobject-introspection:%s" % system_arch
            ]

        if pkgs_name:
            installer = tools.SystemPackageTool()
            for pkg_name in pkgs_name:
                installer.install(pkg_name)

    def import_pkg_config_files(self, pkg):
        for root, dirs, files in os.walk(self.deps_cpp_info[pkg].rootpath):
            for file in files:
                if file.endswith("pc"):
                    print("Importing pkg_config file: %s" % file)
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(self.build_folder, file)
                    copyfile(source_path, target_path)
                    tools.replace_prefix_in_pc_file(target_path, self.deps_cpp_info[pkg].rootpath)

    def build(self):
        for lib in self.deps_cpp_info.deps:
            self.import_pkg_config_files(lib)

        autotools = AutoToolsBuildEnvironment(self)
        new_env = autotools.vars
        new_env["PKG_CONFIG_PATH"] = "%s:%s" % (os.getenv("PKG_CONFIG_PATH"), self.build_folder)
        new_env["PATH"] = "%s:%s" % (os.getenv("PATH"), self.deps_cpp_info["glib"].rootpath + "/bin")
        with tools.environment_append(new_env):
            self.run("NOCONFIGURE=1 librsvg/autogen.sh", run_environment=True)
        autotools.configure(args=['--disable-pixbuf-loader', '--enable-introspection=no'], configure_dir="librsvg")
        autotools.make()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["rsvg-2"]
        self.cpp_info.includedirs = ["include/librsvg-2.0"]
        self.cpp_info.builddirs = ["lib/pkgconfig"]
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
