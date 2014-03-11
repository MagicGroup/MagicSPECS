Name:		libotf
Version:	0.9.12
Release:	4%{?dist}
Summary:	A Library for handling OpenType Font

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.m17n.org/libotf/
Source0:	 http://www.m17n.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc chrpath freetype-devel libXaw-devel
Requires:	freetype

%description 
The library "libotf" provides the following facilites.
Read Open Type Layout Tables from OTF file. Currently these tables are
supported; head, name, cmap, GDEF, GSUB, and GPOS.  Convert a Unicode
character sequence to a glyph code sequence by using the above tables.
The combination of libotf and the FreeType library (Ver.2) realizes
CTL (complex text layout) by OpenType fonts. This library is currently
used by the m17n library. It seems that the probject Free Type Layout
provides the similar (or better) facility as this library, but
currently they have not yet released their library. So, we have
developed this one.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig

%description	devel
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
for file in $RPM_BUILD_ROOT/usr/bin/*; do chrpath -d $file || true; done

(cd example && make clean && rm -rf .deps && rm Makefile)
rm $RPM_BUILD_ROOT/usr/bin/libotf-config

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.*
%{_bindir}/otfdump
%{_bindir}/otflist
%{_bindir}/otftobdf
%{_bindir}/otfview

%files devel
%defattr(-,root,root,-)
%doc example
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.12-4
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.9.12-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.9.12-2
- 为 Magic 3.0 重建

* Wed Oct 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.9.12-1
- Update to 0.9.12

* Wed May 19 2010 Neal Becker <ndbecker2@gmail.com> - 0.9.11-1
- Update to 0.9.11

* Sat Oct 24 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-3
- Add BR libXaw-devel (BR 530586)

* Fri Oct  9 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-2
- Remove libotf-config (just just pkg-config instead)
- Remove example/Makefile to fix multilib conflict

* Tue Aug 25 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-1
- Update to 0.9.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug  8 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Mon Apr 14 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-4
- Remove .deps from example

* Fri Mar 28 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-3
- Change to LGPLv2+
- Add examples

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-2
- Cleanup suggestions from panemade at gmail dot com

* Tue Mar 25 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-1
- Initial

