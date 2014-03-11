Name: enca
Summary: Character set analyzer and detector
Version: 1.13
Release: 4%{?dist}
License: GPLv2
Group: Applications/Text
Source: http://dl.cihar.com/enca/enca-%{version}.tar.bz2
URL: http://gitorious.org/enca
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Enca is an Extremely Naive Charset Analyser. It detects character set and
encoding of text files and can also convert them to other encodings using
either a built-in converter or external libraries and tools like libiconv,
librecode, or cstocs.

Currently, it has support for Belarussian, Bulgarian, Croatian, Czech,
Estonian, Latvian, Lithuanian, Polish, Russian, Slovak, Slovene, Ukrainian,
Chinese and some multibyte encodings (mostly variants of Unicode)
independent on the language.

This package also contains shared Enca library other programs can make use of.

Install %{name} if you need to cope with text files of dubious origin
and unknown encoding and convert them to some reasonable encoding.


%package devel
Summary: Header files and libraries for %{name} charset analyzer
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains the static libraries and header files
for writing programs using the Extremely Naive Charset Analyser library,
and its API documentation.

Install %{name}-devel if you are going to create applications using the Enca
library.


%prep
%setup -q


%build

%configure \
	--disable-dependency-tracking \
	--without-librecode \
	--disable-external \
	%{!?_with_static:--disable-static} \
	--disable-gtk-doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT HTML_DIR=/tmp/html

rm -rf $RPM_BUILD_ROOT/tmp/html
rm -rf $RPM_BUILD_ROOT/%{_libexecdir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libenca.so.*
%{_mandir}/*/*
%doc AUTHORS COPYING FAQ README THANKS TODO

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%doc devel-docs/html/*.html README.devel


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.13-4
- 为 Magic 3.0 重建

* Thu Nov 17 2011 Liu Di <liudidi@gmail.com> - 1.13-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 29 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.13-1
- update to 1.13

* Tue Aug 25 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.10-1
- Update to 1.10
- Change urls for new upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9-4
- Autorebuild for GCC 4.3

* Thu Aug 16 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to GPLv2

* Fri Sep  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-3
- rebuild for FC6

* Tue Feb 14 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-2
- rebuild for FC5

* Mon Dec 19 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-1
- upgrade to 1.9

* Mon Nov 28 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.8-1
- upgrade to 1.8
- update description

* Fri Sep 16 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.7-4
- clenup in docs
- Accepted for Fedora Extra (review by Ville Skytta <ville.skytta@iki.fi>)

* Thu Sep  9 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.7-3
- build static libs conditionally
- disable external converters (#167820)

* Thu Sep  8 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.7-2
- more cleanups (#167820)

* Thu Sep  8 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.7-1
- spec cleanups for Fedora Extra
- avoid build with librecode, use just glibc's iconv 
- avoid any gtk dependencies, html docs are already present in the source

* Mon May 17 2004 David Necas (Yeti) <yeti@physics.muni.cz>
- doubled percents in changelog

* Mon Dec 22 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- moved wrappers to libexec

* Thu Nov  6 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- added b-piconv
- fixed HTML doc install paths

* Tue Oct 14 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- testing whether $RPM_BUILD_ROOT is not /
- updated for new HTML doc location
- changed make -> %%__make, rm -> %%__rm

* Sat Aug  2 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- cleaning $RPM_BUILD_ROOT in %%install

* Sat Jun 28 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- removed --disable-gtk-doc, no longer needed

* Fri Jun 20 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- added enca.pc to devel package

* Sat Jun 14 2003 David Necas (Yeti) <yeti@physics.muni.cz>
- updated description
- added --disable-gtk-doc

* Mon Dec 23 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- added libenca.so

* Fri Dec 20 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- fixed URL and Source to trific.ath.cx

* Mon Oct 21 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- added FAQ to docs

* Thu Oct 10 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- removed twice-listed %%{docdir}/html

* Sat Sep 21 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- added b-umap

* Sun Sep 15 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- added enconv

* Thu Aug 29 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- removed bzip2-devel buildprereq

* Sat Aug 24 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- added postinstall and postuninstall scriptlets

* Wed Aug 21 2002 David Necas (Yeti) <yeti@physics.muni.cz>
- updated to enca-0.10.0-pre2
- added libenca
- split into enca and enca-devel
- removed cache
- fixed HTML_DIR

* Tue Jul 10 2001 David Necas (Yeti) <yeti@physics.muni.cz>
- changed rpm macros in Source and URL to autoconf macros to ease debian/
  stuff generation

* Sun May 20 2001 David Necas (Yeti) <yeti@physics.muni.cz>
- added BuildPrereq: bzip2-devel

* Wed May  2 2001 David Necas (Yeti) <yeti@physics.muni.cz>
- changed group to standard (but much less appropriate) Applications/Text
- rpm macros are used instead of autoconf macros (after the first definition)

* Sun Mar 11 2001 David Necas (Yeti) <yeti@physics.muni.cz>
- added defattr, doc attributes
- uses global configure cache
- heavy use of predefined directories
- configure moved to build section as is usual

* Sun Feb 25 2001 David Necas (Yeti) <yeti@physics.muni.cz>
- updated to enca-0.9.0pre4 (including files and descriptions)
- added sed dependency

* Sun Oct 25 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- updated to enca-0.7.5

* Sun Oct 11 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- removed redundant Provides: enca

* Sun Oct  1 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- updated to enca-0.7.1
- man page forced to be intstalled to ${prefix}/share/man

* Tue Sep 26 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- updated to enca-0.7.0
- spec autogenerated by configure

* Tue Sep 19 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- fixed not installing bcstocs

* Wed Sep 13 2000 David Necas (Yeti) <yeti@physics.muni.cz>
- first packaged (0.6.2)

