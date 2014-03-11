%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:		libftdi
Version:	0.19
Release:	3%{?dist}
Summary:	Library to program and control the FTDI USB controller

Group:		System Environment/Libraries
License:	LGPLv2
URL:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/de/produkte/opensource/ftdi/TGZ/%{name}-%{version}.tar.gz
Source1:	no_date_footer.html
Patch0:		libftdi-0.17-multilib.patch
# update to recent libusb
Patch1:		libftdi-0.19-libusb.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libusb-devel, doxygen, boost-devel, python-devel, swig
BuildRequires:	autoconf, automake, libtool
Requires:	pkgconfig, udev
Requires(pre):	shadow-utils


%package devel
Summary:	Header files and static libraries for libftdi
Group:		Development/Libraries
Requires:	libftdi = %{version}-%{release}
Requires:	libusb-devel

%package python
Summary:	Libftdi library Python binding
Group:		Development/Libraries
Requires:	libftdi = %{version}-%{release}

%package c++
Summary:	Libftdi library C++ binding
Group:		Development/Libraries
Requires:	libftdi = %{version}-%{release}

%package c++-devel
Summary:	Libftdi library C++ binding development headers and libraries
Group:		Development/Libraries
Requires:	libftdi-devel = %{version}-%{release}, libftdi-c++ = %{version}-%{release}


%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%description devel
Header files and static libraries for libftdi

%description python
Libftdi Python Language bindings.

%description c++
Libftdi library C++ language binding.

%description c++-devel
Libftdi library C++ binding development headers and libraries
for building C++ applications with libftdi.


%prep
%setup -q
sed -i -e 's/HTML_FOOTER            =/HTML_FOOTER            = no_date_footer.html/g' doc/Doxyfile.in
#kernel does not provide usb_device anymore
sed -i -e 's/usb_device/usb/g' packages/99-libftdi.rules
%patch0 -p1 -b .multilib
%patch1 -p1 -b .libusb


%build
autoreconf -if
%configure --enable-python-binding --enable-libftdipp --disable-static
cp %{SOURCE1} %{_builddir}/%{name}-%{version}/doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find %{buildroot} -name \*\.la -print | xargs rm -f
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
#no man install
install -p -m 644 doc/man/man3/*.3 $RPM_BUILD_ROOT%{_mandir}/man3
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -p -m 644 packages/99-libftdi.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d


# Cleanup examples
rm -f $RPM_BUILD_ROOT/%{_bindir}/simple
rm -f $RPM_BUILD_ROOT/%{_bindir}/bitbang
rm -f $RPM_BUILD_ROOT/%{_bindir}/bitbang2
rm -f $RPM_BUILD_ROOT/%{_bindir}/bitbang_ft2232
rm -f $RPM_BUILD_ROOT/%{_bindir}/bitbang_cbus
rm -f $RPM_BUILD_ROOT/%{_bindir}/find_all
rm -f $RPM_BUILD_ROOT/%{_bindir}/find_all_pp
rm -f $RPM_BUILD_ROOT/%{_bindir}/baud_test
rm -f $RPM_BUILD_ROOT/%{_bindir}/serial_read

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libftdi.so.*
%config(noreplace) %{_sysconfdir}/udev/rules.d/99-libftdi.rules

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_bindir}/libftdi-config
%{_libdir}/libftdi.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/libftdi.pc
%{_mandir}/man3/*

%files python
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING.LIB README
%{python_sitearch}/*

%files c++
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libftdipp.so.*

%files c++-devel
%defattr(-, root, root, -)
%doc doc/html
%{_libdir}/libftdipp.so
%{_includedir}/*.hpp
%{_libdir}/pkgconfig/libftdipp.pc

%pre
getent group plugdev >/dev/null || groupadd -r plugdev
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.19-3
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 0.19-2
- 为 Magic 3.0 重建

* Sat Jun 18 2011 Lucian Langa <cooly@gnome.eu.org> - 0.19-1
- new upstream release

* Tue May 24 2011 Lucian Langa <cooly@gnome.eu.org> - 0.19-1
- new upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Dan Horák <dan[at]danny.cz> - 0.18-4
- fix build with libusb >= 1:0.1.3 (wrapper around libusb1)

* Sun Aug  1 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 01 2010 Lucian Langa <cooly@gnome.eu.org> - 0.18-1
- drop patch0 - fixed upstream
- new upstream release

* Wed Jun 09 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-5
- readd mistakenly dropped parch (fixes multilib issues)

* Wed May 05 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-4
- fix typo in group handling (#581151)

* Thu Mar 11 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-3
- fix incorrect UDEV rule (#563566)

* Sat Jan 16 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-2
- do not package static libfiles (#556068)

* Sun Jan 01 2010 Lucian Langa <cooly@gnome.eu.org> - 0.17-1
- add patch to fix typo in python bindings
- drop multilib patch0 fixed upstream
- new upstream release

* Sat Aug 22 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-7
- add group for udev rule (#517773)

* Fri Jul 31 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-6
- rebuilt with modified patch

* Fri Jul 31 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-5
- fix multilib conflict in libftdi-config (#508498)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-3
- added udev rules
- addedd c++, python bindings

* Tue Jun 30 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-2
- fix doxygen conflict (#508498)

* Fri May 08 2009 Lucian Langa <cooly@gnome.eu.org> - 0.16-1
- new upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-3
- fix tag

* Sun Feb 15 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-2
- add new BR boost-devel

* Sun Feb 15 2009 Lucian Langa <cooly@gnome.eu.org> - 0.15-1
- fix for bug #485600: pick libusb-devel for -devel subpackage
- new upstream release

* Fri Sep 26 2008 Lucian Langa <cooly@gnome.eu.org> - 0.14-2
- require pkgconfig for devel

* Tue Sep 23 2008 Lucian Langa <cooly@gnome.eu.org> - 0.14-1
- new upstream

* Wed Sep 03 2008 Lucian Langa <cooly@gnome.eu.org> - 0.13-1
- initial specfile
