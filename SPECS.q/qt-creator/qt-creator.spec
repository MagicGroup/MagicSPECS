#define prerelease rc1

# We need avoid oython byte compiler to not crash over template .py file which
# is not a valid python file, only for the IDE
%global _python_bytecompile_errors_terminate_build 0

Name:           qt-creator
Version: 3.5.1
Release: 2%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt
Summary(zh_CN):	Qt 的跨平台轻量级 IDE

Group:          Development/Tools
Group(zh_CN):	开发/工具
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.qt.io/official_releases/qtcreator/%{majorver}/%{version}/qt-creator-opensource-src-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop
Source2:        qt-creator-Magic-privlibs
Source3:        qtcreator.appdata.xml

# Use absolute paths for the specified rpaths, not $ORIGIN-relative paths
# (to fix some /usr/bin/<binary> having rpath $ORIGIN/..)
Patch0:         qt-creator_rpath.patch
# In Fedora, the ninja command is called ninja-build
Patch1:         qt-creator_ninja-build.patch

Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtdoc

# we need qt-devel and gcc-c++ to compile programs using qt-creator
Requires:       qt5-qtbase-devel
Requires:       gcc-c++
Requires:       %{name}-data = %{version}-%{release}


BuildRequires:  qt5-qtbase-devel >= 5.5.0
BuildRequires:  pkgconfig(Qt5Designer) >= 5.5.0
BuildRequires:  pkgconfig(Qt5Script) >= 5.5.0
BuildRequires:  pkgconfig(Qt5XmlPatterns) >= 5.5.0
BuildRequires:  pkgconfig(Qt5X11Extras) >= 5.5.0
BuildRequires:  pkgconfig(Qt5WebKit) >= 5.5.0
BuildRequires:  pkgconfig(Qt5Help) >= 5.5.0
BuildRequires:  desktop-file-utils
BuildRequires:  botan-devel
BuildRequires:  diffutils
BuildRequires:  libappstream-glib
BuildRequires:  llvm-devel
BuildRequires:  clang-devel

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%description -l zh_CN
QT 的跨平台轻量级 IDE。

%package data
Summary:        Application data for %{name}
Summary(zh_CN.UTF-8): %{name} 的应用程序数据
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description data
Application data for %{name}.
%description data -l zh_CN.UTF-8
%{name} 的应用程序数据。

%package translations
Summary:        Translations for %{name}
Summary(zh_CN.UTF-8): %{name} 的翻译
Requires:       %{name}-data = %{version}-%{release}
Requires:       qt5-qttranslations
BuildArch:      noarch

%description translations
Translations for %{name}.
%description translations -l zh_CN.UTF-8
%{name} 的翻译。

%package doc
Summary:        User documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的用户文档
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
User documentation for %{name}.
%description doc -l zh_CN.UTF-8
%{name} 的用户文档。


# long list of private shared lib names to filter out
%include %{SOURCE2}
%global __provides_exclude ^(%{privlibs})\.so
%global __requires_exclude ^(%{privlibs})\.so

%prep
%setup -q -n qt-creator-opensource-src-%{version}%{?prerelease:-%prerelease}
%patch0 -p1
%patch1 -p1

%build
export QTDIR="%{_qt5_prefix}"
export PATH="%{_qt5_bindir}:$PATH"

%qmake_qt5 -r IDE_LIBRARY_BASENAME=%{_lib} USE_SYSTEM_BOTAN=1 CONFIG+=disable_rpath
make %{?_smp_mflags}
make qch_docs %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}/%{_prefix}
make install_inst_qch_docs INSTALL_ROOT=%{buildroot}/%{_prefix}


for i in 16 24 32 48 64 128 256; do
    mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/${i}x${i}/apps
done

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

install -Dpm0644 %{SOURCE3} %{buildroot}%{_datadir}/appdata/qtcreator.appdata.xml
%{_bindir}/appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/qtcreator.appdata.xml

# Output an up-to-date list of Provides/Requires exclude statements.
outfile=__Fedora-privlibs
i=0
sofiles=$(find %{buildroot}%{_libdir}/qtcreator -name \*.so\*|sed 's!^.*/\(.*\).so.*!\1!g'|sort|uniq)
for so in ${sofiles} ; do
    if [ $i == 0 ]; then
        echo "%%global privlibs $so" > $outfile
        i=1
    else
        echo "%%global privlibs %%{privlibs}|$so" >> $outfile
    fi
done
diff -u %{SOURCE2} $outfile || :
cat $outfile


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :



%files
%doc README.md
%license LICENSE.LGPLv3 LICENSE.LGPLv21 LGPL_EXCEPTION.TXT
%{_bindir}/qbs
%{_bindir}/qbs-config
%{_bindir}/qbs-config-ui
%{_bindir}/qbs-qmltypes
%{_bindir}/qbs-setup-*
%{_bindir}/cpaster
%{_bindir}/buildoutputparser
%{_bindir}/qml2puppet
%{_bindir}/qtpromaker
%{_bindir}/qtcreator
%{_bindir}/qtcreator_process_stub
%{_bindir}/sdktool
%{_libdir}/qtcreator
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/appdata/qtcreator.appdata.xml
%{_datadir}/icons/hicolor/*/apps/QtProject-qtcreator.png

%files data
%{_datadir}/qtcreator/
%exclude %{_datadir}/qtcreator/translations

%files translations
%{_datadir}/qtcreator/translations/

%files doc
%doc %{_defaultdocdir}/qtcreator/qtcreator.qch


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.5.1-2
- 更新到 3.5.1

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 3.5.0-1
- 更新到 3.5.0

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.6.1-1
- 更新到 3.5.0


