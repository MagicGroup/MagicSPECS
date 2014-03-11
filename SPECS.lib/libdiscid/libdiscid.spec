Name:           libdiscid
Version:        0.2.2
Release:        7%{?dist}
Summary:        A Library for creating MusicBrainz DiscIDs

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://musicbrainz.org/doc/libdiscid
Source0:        http://users.musicbrainz.org/~matt/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig

%description
This C library %{name} creates MusicBrainz DiscIDs from audio CDs. It
reads the table of contents (TOC) of a CD and generates an identifier
which can be used to lookup the CD at MusicBrainz. Additionally, it
provides a submission URL for adding the DiscID to the database.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" 
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/discid/

%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.2-7
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.2.2-6
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.2.2-2
- rebuild for pkgconfig deps

* Sat Nov 29 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.2-1
- Update to latest upstream (0.2.2)

* Sat Feb  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.1.1-6
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Fri Nov 16 2007 Alex Lancaster <alexl@users.sourceforge.net> - 0.1.1-5
- Fix description
- devel package Requires: pkgconfig
- save header timestamps

* Fri Nov 16 2007 Alex Lancaster <alexl@users.sourceforge.net> - 0.1.1-4
- Remove unneeded doc directive in -devel package, add COPYING file

* Fri Nov 16 2007 Alex Lancaster <alexl@users.sourceforge.net> - 0.1.1-3
- Fix tarball

* Thu Nov 15 2007 Alex Lancaster <alexl@users.sourceforge.net> - 0.1.1-2
- Update as per packaging guidelines: fix license tag, add docs

* Sun Jul 15 2007 Kyle VanderBeek <kylev@kylev.com> - 0.1.1-1
- Initial version for Fedora 7
