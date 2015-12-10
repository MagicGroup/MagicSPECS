%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:		libftdi
Version:	1.2
Release:	3%{?dist}
Summary:	Library to program and control the FTDI USB controller
Summary(zh_CN.UTF-8): 编程和控制 FTDI USB 控制器的库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2
URL:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/en/developer/libftdi/download/%{name}1-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	libconfuse-devel
BuildRequires:	libusbx-devel
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	systemd

%package devel
Summary:	Header files and static libraries for libftdi
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libftdi = %{version}-%{release}
Requires:	libusb-devel

%package python
Summary:	Libftdi library Python binding
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libftdi = %{version}-%{release}

%package c++
Summary:	Libftdi library C++ binding
Summary(zh_CN.UTF-8): %{name} 的 C++ 绑定
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libftdi = %{version}-%{release}

%package c++-devel
Summary:	Libftdi library C++ binding development headers and libraries
Summary(zh_CN.UTF-8): %{name}-c++ 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libftdi-devel = %{version}-%{release}, libftdi-c++ = %{version}-%{release}


%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%description -l zh_CN.UTF-8
编程和控制 FTDI USB 控制器的库，使用 libusb

%description devel
Header files and static libraries for libftdi

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description python
Libftdi Python Language bindings.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%description c++
Libftdi library C++ language binding.

%description c++ -l zh_CN.UTF-8
%{name} 的 C++ 绑定。

%description c++-devel
Libftdi library C++ binding development headers and libraries
for building C++ applications with libftdi.

%description c++-devel -l zh_CN.UTF-8
%{name}-c++ 的开发包。

%prep
%setup -q -n %{name}1-%{version}

#kernel does not provide usb_device anymore
sed -i -e 's/usb_device/usb/g' packages/99-libftdi.rules
sed -i -e 's/GROUP="plugdev"/TAG+="uaccess"/g' packages/99-libftdi.rules

%build
export CMAKE_PREFIX_PATH=/usr
%{cmake} .
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT/lib/udev/rules.d/
install -p -m 644 packages/99-libftdi.rules $RPM_BUILD_ROOT/lib/udev/rules.d/99-libftdi.rules

find $RPM_BUILD_ROOT -type f -name "*.la" -delete
find $RPM_BUILD_ROOT -type f -name "*.a" -delete

#no man install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -p -m 644 doc/man/man3/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

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
rm -f $RPM_BUILD_ROOT/%{_bindir}/serial_test
rm -rf $RPM_BUILD_ROOT/%{_libdir}/cmake*
rm -rf $RPM_BUILD_ROOT/%{_datadir}/libftdi/examples

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libftdi1.so.*
%config(noreplace) /lib/udev/rules.d/99-libftdi.rules

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_bindir}/libftdi1-config
%{_bindir}/ftdi_eeprom
%{_libdir}/libftdi1.so
%{_includedir}/libftdi1/*.h
%{_libdir}/pkgconfig/libftdi1.pc
%{_mandir}/man3/*

%files python
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING.LIB README
%{python_sitearch}/*

%files c++
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libftdipp1.so.*

%files c++-devel
%defattr(-, root, root, -)
%doc doc/html
%{_libdir}/libftdipp1.so
%{_includedir}/libftdi1/*.hpp
%{_libdir}/pkgconfig/libftdipp1.pc

%pre
getent group plugdev >/dev/null || groupadd -r plugdev
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.2-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.2-2
- 更新到 1.2

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.1-1
- 更新到 1.1

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
