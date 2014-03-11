Name:           soundtouch
Version:        1.4.0
Release:        7%{?dist}
Summary:        Audio Processing library for changing Tempo, Pitch and Playback Rates
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.surina.net/soundtouch/
Source0:        http://www.surina.net/soundtouch/%{name}-%{version}.tar.gz
Patch0:         soundtouch-1.4.0-x86_64-asm-broken.patch
Patch1:         soundtouch-1.4.0-mmx-sse-compile-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gcc-c++

%description
SoundTouch is a LGPL-licensed open-source audio processing library for
changing the Tempo, Pitch and Playback Rates of audio streams or
files. The SoundTouch library is suited for application developers
writing sound processing tools that require tempo/pitch control
functionality, or just for playing around with the sound effects.

The SoundTouch library source kit includes an example utility
SoundStretch which allows processing .wav audio files from a
command-line interface.


%package devel
Summary:  Libraries, includes, etc to develop soundtouch applications
Group:    Development/Libraries
Requires: soundtouch = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop soundtouch applications.


%prep
%setup -q -n %{name}
%patch0 -p1
# soundtouch contains mmx / sse versions of the stretching algorithm.
# to compile these -msse / -mmmx is needed. In x86 we make sure with this patch
# the needed -msse / -mmmx only gets passed when compiling the relevant
# object files so that these instructions do not get used in other object
# files. On non x86 we simply sed the -msse2 out of the original makefiles
%ifarch %{ix86}
%patch1 -p1
%else
sed -i 's|-O3 -msse2||' source/SoundTouch/Makefile.*
%endif
sed -i 's|-O3||' source/SoundStretch/Makefile.*
# set correct version for .so build
%define ltversion %(echo %{version} | tr '.' ':')
sed -i 's/-rpath $(libdir)/-rpath $(libdir) -version-number %{ltversion}/' \
  source/SoundTouch/Makefile.in
# cleanup a bit
chmod -x README.html source/SoundTouch/RateTransposer.cpp
sed -i 's|\r||g' README.html source/SoundTouch/RateTransposer.cpp


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
# Don't use rpath!   
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# remove redundant installed docs
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc/%{name}

# pkgconfig compat links for compat with older (API compatible) releases
# dunno why upstream keeps changing the pkgconfig name
ln -s soundtouch-1.4.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libSoundTouch.pc
ln -s soundtouch-1.4.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/soundtouch-1.0.pc

# soundtouch installs an autoheader generated header file which could very
# well conflict with other autoheader generated header files, so we override
# this with our own version which contains only the bare minimum:
echo '#define FLOAT_SAMPLES 1' \
  > $RPM_BUILD_ROOT%{_includedir}/soundtouch/soundtouch_config.h
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig 


%files
%defattr(-,root,root,-)
%doc COPYING.TXT README.html
%{_bindir}/soundstretch
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}
%{_datadir}/aclocal/%{name}.m4


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.4.0-7
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 1.4.0-6
- 为 Magic 3.0 重建

* Wed Feb 08 2012 Liu Di <liudidi@gmail.com> - 1.4.0-5
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Hans de Goede <hdegoede@redhat.com> 1.4.0-1
- New upstream release 1.4.0

* Sat Dec 20 2008 Hans de Goede <hdegoede@redhat.com> 1.3.1-11
- Fix compilation with libtool 2.x

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.1-10
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-9
- Fix compilation with gcc 4.3

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-8
- Rebuild for buildId
- Update license tag for new license guidelines compliance

* Mon Feb 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-7
- Fix building with automake-1.10

* Tue Aug 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-6
- FE6 Rebuild

* Wed Aug  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-5
- Patch makefiles so that our RPM_OPT_FLAGS get used instead of the custom
  upstream CFLAGS.

* Mon Jul 31 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-4
- Add Requires: pkgconfig to -devel subpackage
- Replace installed autoheader generated header file with our own version
  which contains only the nescesarry soundtouch specific defines, thus avoiding
  possible conflicts with other autoheader generated headers.

* Mon Jul 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.3.1-3
- Add BR libtool

* Mon Jul 31 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-2
- Add BR: automake, because upstream uses symlinks to instead of copies of some
  needed automake files.

* Sat Jul 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.1-1
- New upstream version 1.3.1
- Minor specfile cleanups for livna submission.
- Give the .so a proper version instead of 0.0.0
- Don't use rpath in soundstretch binary

* Thu Aug 26 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.2.1-1
- initial build.
