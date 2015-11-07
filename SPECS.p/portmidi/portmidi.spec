%global _desktopdir %{?_desktopdir:%{_datadir}/applications}
Summary:        Real-time Midi I/O Library
Summary(zh_CN.UTF-8): 实时 Midi I/O 库
Name:           portmidi
Version:        217
Release:        9%{?dist}
License:        MIT
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://portmedia.sourceforge.net/
Source0:        http://downloads.sourceforge.net/portmedia/%{name}-src-%{version}.zip
Source1:        pmdefaults.desktop
# Build fixes:
Patch0:         portmidi-cmake.patch
# Fix multilib conflict RHBZ#831432
Patch1:         portmidi-no_date_footer.patch
Patch2:		portmidi-nojava.patch
Patch3:		portmidi-217-format-security.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
%if 0%{?JAVA}
BuildRequires:  java-devel >= 1.7
BuildRequires:  jpackage-utils
%endif
BuildRequires:  python2-devel
BuildRequires:  doxygen
BuildRequires:  tex(latex)

%description
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the PortMidi
libraries.

%description -l zh_CN.UTF-8
实时 Midi I/O 库。

%package devel
Summary:        Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the header files
and the documentation of PortMidi libraries.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n python-%{name}
Summary:        Python wrapper for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-%{name}
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the python
bindings of PortMidi libraries. It can send and receive MIDI data in
real-time from Python.

%description -n python-%{name} -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%package tools
Summary:          Tools to configure and use %{name}
Summary(zh_CN.UTF-8): %{name} 的配置工具
Group:            Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:         hicolor-icon-theme
%if 0%{?JAVA}
Requires:         java >= 1.7
Requires:         jpackage-utils
%endif
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description tools
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the PortMidi
configuration utility "pmdefaults" and some test applications.

%description tools -l zh_CN.UTF-8
%{name} 的配置工具。

%prep
%setup -q -n %{name}
%if 0%{?JAVA}
%patch0 -p1 -b .buildfix
%endif
%patch1 -p1 -b .no.date
%patch3 -p1

%if ! 0%{?JAVA}
%patch2 -p1
%endif
# ewwww... binaries
rm -f portmidi_cdt.zip */*.exe */*/*.exe

# Fix permissons and encoding issues:
find . -name "*.c" -exec chmod -x {} \;
find . -name "*.h" -exec chmod -x {} \;
for i in *.txt */*.txt */*/*.txt ; do
   chmod -x $i
   sed 's|\r||' $i > $i.tmp
   touch -r $i $i.tmp
   mv -f $i.tmp $i
done

%if 0%{?JAVA}
# Fedora's jni library location is different
sed -i 's|loadLibrary.*|load("%{_libdir}/%{name}/libpmjni.so");|' \
   pm_java/jportmidi/JPortMidiApi.java

# Add shebang, lib and class path
sed -i -e 's|^java|#!/bin/sh\njava \\\
   -Djava.library.path=%{_libdir}/%{name}/|' \
   -e 's|/usr/share/java/|%{_libdir}/%{name}/|' \
   pm_java/pmdefaults/pmdefaults
%endif

%build
%if 0%{?JAVA}
export JAVA_HOME=%{java_home}
%endif
%cmake -DCMAKE_SKIP_BUILD_RPATH=1 -DCMAKE_CACHEFILE_DIR=%{_builddir}/%{name}/build -DVERSION=%{version} .
make %{?_smp_flags}

# Build the doxygen documentation:
doxygen

# Build python modules
PYTHON_VER=$(python -c "from sys import version; print (version[:3])")
PYTHON_INC=$(python -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
pushd pm_python/pyportmidi
   gcc %{optflags} -pthread -fPIC -c -o _pyportmidi.o -I../../pm_common \
       -I../../porttime -I$PYTHON_INC _pyportmidi.c
   gcc -shared -o _pyportmidi.so _pyportmidi.o -lportmidi -lpython$PYTHON_VER \
       -L../../build/Release
popd

%install
%make_install

# Install the test applications:
install -d %{buildroot}%{_libdir}/%{name}
for app in latency midiclock midithread midithru mm qtest sysex test; do
   install -m 0755 build/Release/$app %{buildroot}%{_libdir}/%{name}/
done

%if 0%{?JAVA}
# Fedora's jni library location is different
mv %{buildroot}%{_libdir}/libpmjni.so \
   %{buildroot}%{_libdir}/%{name}/
mv %{buildroot}%{_javadir}/pmdefaults.jar \
   %{buildroot}%{_libdir}/%{name}/
%endif

# pmdefaults icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
%if 0%{?JAVA}
install -pm 644 pm_java/pmdefaults/pmdefaults-icon.png \
   %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
%endif

# desktop file
mkdir -p %{buildroot}%{_desktopdir}/
desktop-file-install \
   --dir=%{buildroot}%{_desktopdir} \
   %{SOURCE1}

# Why don't they install this header file?
install -pm 644 pm_common/pmutil.h %{buildroot}%{_includedir}/

# Install python modules
mkdir -p %{buildroot}%{python_sitearch}/pyportmidi
pushd pm_python/pyportmidi
   install -pm 755 _pyportmidi.so %{buildroot}%{python_sitearch}/pyportmidi/
   install -pm 644 *.py %{buildroot}%{python_sitearch}/pyportmidi/
popd

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

# Remove duplicate library
rm -f %{buildroot}%{_libdir}/libportmidi_s.so
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGELOG.txt license.txt
%{_libdir}/lib*.so.*

%files tools
%if 0%{?JAVA}
%doc pm_java/pmdefaults/README.txt pm_cl/*
%endif
%{_libdir}/%{name}/
#%{_bindir}/pmdefaults
#%{_datadir}/icons/hicolor/128x128/apps/pmdefaults-icon.png
%{_desktopdir}/pmdefaults.desktop

%files -n python-%{name}
%doc pm_python/README_PYTHON.txt
%{python_sitearch}/pyportmidi/

%files devel
%doc README.txt
%doc html
%{_includedir}/*
%{_libdir}/lib*.so

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 217-9
- 为 Magic 3.0 重建

* Wed Jul 29 2015 Liu Di <liudidi@gmail.com> - 217-8
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 217-6
- Fix multilib conflict RHBZ#831432
- Don't bulid PDF doc, as it causes another multilib conflict
- Specfile cleanup. Drop old GCJ-Java and Python bits

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 217-4
- Fix FTBFS due to changes in cmake. RHBZ #715668

* Sat May 14 2011 Daniel Drake <dsd@laptop.org> - 217-3
- move Requires:Java to tools subpackage, its not needed by the main package

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 217-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 09 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 217-1
- Update to 217

* Fri Jul 23 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 200-4
- Fix python module build

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 200-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jan 30 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 200-2
- Remove duplicate library

* Sat Jan 30 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 200-1
- Update to 200.
- Add python subpackage

* Fri Nov 27 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 184-1
- Update to 184. Build system uses cmake now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 131-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 131-3
- Include pmutil.h in the devel package

* Tue Jan 27 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 131-2
- Build and add doxygen documentation
- Preserve some timestamps

* Sun Jan 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 131-1
- New upstream release.

* Sun Dec 07 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 82-1
- Initial release.
