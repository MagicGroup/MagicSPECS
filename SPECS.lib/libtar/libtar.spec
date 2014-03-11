Summary:        Tar file manipulation API
Name:           libtar
Version:        1.2.11
Release:        13%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://www.feep.net/libtar/
Source0:        ftp://ftp.feep.net/pub/software/libtar/libtar-%{version}.tar.gz
Patch0:         http://ftp.debian.org/debian/pool/main/libt/libtar/libtar_1.2.11-4.diff.gz
Patch1:         libtar-1.2.11-missing-protos.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  zlib-devel libtool

%description
libtar is a C library for manipulating tar archives. It supports both
the strict POSIX tar format and many of the commonly-used GNU
extensions.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -z .deb
%patch1 -p1
# set correct version for .so build
%define ltversion %(echo %{version} | tr '.' ':')
sed -i 's/-rpath $(libdir)/-rpath $(libdir) -version-number %{ltversion}/' \
  lib/Makefile.in


%build
cp /usr/share/libtool/config/config.sub /usr/share/libtool/config/ltmain.sh autoconf
#autoreconf -fisv
%configure --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool
# Without this we get no debuginfo and stripping
chmod +x $RPM_BUILD_ROOT%{_libdir}/libtar.so.%{version}
rm $RPM_BUILD_ROOT%{_libdir}/*a


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYRIGHT TODO README ChangeLog*
%{_bindir}/%{name}
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libtar.h
%{_includedir}/libtar_listhash.h
%{_libdir}/lib*.so
%{_mandir}/man3/*.3*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.11-13
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 1.2.11-12
- 为 Magic 3.0 重建

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-11
- Fix missing prototype compiler warnings

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.11-10
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-9
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-8
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-7
- Taking over as maintainer since Anvil has other priorities
- Add a bunch of patches from Debian, which build a .so instead of a .a
  and fix a bunch of memory leaks.
- Reinstate a proper devel package as we now build a .so

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.2.11-6.fc5
- Modified URL and added one in Source0

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.11-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:1.2.11-0.fdr.3
- Merged devel and main packages
- Package provide now libtar-devel

* Tue Jul  8 2003 Dams <anvil[AT]livna.org>
- Initial build.
