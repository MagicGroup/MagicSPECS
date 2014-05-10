Name:           libicns
Version:        0.8.1
Release:        5%{?dist}
Summary:        Library for manipulating Macintosh icns files

Group:          System Environment/Libraries
# libicns, icns2png and icontainer2icns are under LGPLv2+
# png2icns is under GPLv2+
License:        LGPLv2+ and GPLv2+
URL:            http://icns.sourceforge.net/
Source0:        http://downloads.sourceforge.net/icns/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libpng-devel
BuildRequires:  jasper-devel

%description
libicns is a library providing functionality for easily reading and 
writing Macintosh icns files


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Utilities for %{name}
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description    utils
icns2png - convert Mac OS icns files to png images
png2icns - convert png images to Mac OS icns files
icontainer2icns - extract icns files from icontainers 


%prep
%setup -q


%build
%configure --disable-static
# disable rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LGPL-2 COPYING.LGPL-2.1 NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc src/apidocs.*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%doc README


%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 0.8.1-5
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Andrea Musuruane <musuruan@gmail.com> - 0.8.1-1
- Updated to new upstream 0.8.1

* Sat Feb 04 2012 Andrea Musuruane <musuruan@gmail.com> - 0.8.0-1
- Updated to new upstream 0.8.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Andrea Musuruane <musuruan@gmail.com> - 0.7.1-4
- Fixed FTBFS for new libpng

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.7.1-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 01 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.1-1
- Updated to new upstream 0.7.1

* Sun Aug 23 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.0-3
- Updated to new upstream 0.7.0 that was released without bumping the version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.0-1
- Updated to upstream 0.7.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 07 2009 Andrea Musuruane <musuruan@gmail.com> - 0.6.2-1
- Updated to upstream 0.6.2

* Mon Jan 05 2009 Andrea Musuruane <musuruan@gmail.com> - 0.6.1-1
- Updated to upstream 0.6.1

* Sat Dec 20 2008 Andrea Musuruane <musuruan@gmail.com> - 0.6.0-2
- Fixed Source0 URL
- Added missing 'Requires: pkgconfig' to devel package

* Sat Dec 13 2008 Andrea Musuruane <musuruan@gmail.com> - 0.6.0-1
- First release for Fedora

