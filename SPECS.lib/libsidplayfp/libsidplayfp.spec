Name:           libsidplayfp
Version: 1.8.2
Release: 2%{?dist}
Summary:        SID chip music module playing library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://sourceforge.net/projects/sidplay-residfp/
Source0:        http://downloads.sourceforge.net/sidplay-residfp/%{name}-%{version}.tar.gz
BuildRequires:  doxygen
%if 0%{?fedora} >= 18
# Obsolete old sidplay1 libsidplay
Obsoletes:      libsidplay < 1.36.60-6
Provides:       libsidplay = 1.36.60-6
%endif
%if 0%{?fedora} >= 19
# Obsolete old sidplay2 based sidplay (sidplayfp is a continuation of sidplay2)
Obsoletes:      sidplay-libs < 2.1.1-15
Provides:       sidplay-libs = 2.1.1-15
%endif

%description
This library provides support for playing SID music modules originally
created on Commodore 64 and compatibles. It contains a processing engine
for MOS 6510 machine code and MOS 6581 Sound Interface Device (SID)
chip output. It is used by music player programs like SIDPLAY and
several plug-ins for versatile audio players.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} >= 18
# Obsolete old sidplay1 libsidplay
Obsoletes:      libsidplay-devel < 1.36.60-6
Provides:       libsidplay-devel = 1.36.60-6
%endif
%if 0%{?fedora} >= 19
# Obsolete old sidplay2 based sidplay (sidplayfp is a continuation of sidplay2)
Obsoletes:      sidplay-libs-devel < 2.1.1-15
Provides:       sidplay-libs-devel = 2.1.1-15
%endif

%description devel
These are the files needed for compiling programs that use %{name}.


%package devel-doc
Summary:        API documentation for %{name}
Group:          Development/Libraries
BuildArch:      noarch

%description devel-doc
This package contains API documentation for %{name}.


%prep
%setup -q
chmod -x builders/residfp-builder/residfp/resample/SincResampler.cpp
chmod -x builders/residfp-builder/residfp/WaveformGenerator.cpp
chmod -x builders/residfp-builder/residfp/Integrator.h


%build
%configure --disable-static
make %{_smp_mflags} all doc


%install
%make_install INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README TODO
%{_libdir}/libsidplayfp.so.3*
%{_libdir}/libstilview.so.0*

%files devel
%{_libdir}/libsidplayfp.so
%{_libdir}/libstilview.so
%{_includedir}/sidplayfp/
%{_includedir}/stilview/
%{_libdir}/pkgconfig/*.pc

%files devel-doc
%doc docs/html


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.8.2-2
- 更新到 1.8.2

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.4.2-1
- 更新到 1.4.2

* Wed May  1 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.1-4
- Also Obsoletes/Provides the old sidplay1 based libsidplay

* Mon Apr 29 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.1-3
- Add Obsoletes/Provides sidplay-libs[-devel]

* Thu Apr 11 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.1-2
- Some minor style changes
- Fix rpmlint warnings about executable files in debuginfo sub-package
- Add a -devel-doc sub-package

* Mon Apr  8 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.1-1
- Initial RPM packaging for Fedora.
