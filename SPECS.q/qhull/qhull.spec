Summary: General dimension convex hull programs
Summary(zh_CN.UTF-8): 一般维度的凸包程序
Name: qhull
Version:	2012.1
Release:	3%{?dist}
License: Qhull
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://www.qhull.org/download/qhull-%{version}-src.tgz

Patch1:	qhull-2012.1-fix-format-security.patch

URL: http://www.qhull.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%description -l zh_CN.UTF-8
一般维度的凸包程序。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development files for qhull
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name} = %{version}-%{release}

%description devel
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
%{cmake} -DMAN_INSTALL_DIR=%{_mandir}/man1 \
	  -DDOC_INSTALL_DIR=%{_docdir}/%{name}-%{version} \
 	  .
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.{a,la}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%_bindir/*
%_libdir/*.so.*
%_mandir/man1/*

%files devel
%defattr(-,root,root)
%_libdir/*.so
%_includedir/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2012.1-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2012.1-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 2012.1-1
- 更新到 2012.1

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2011.1-16
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 02 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2003.1-14
- Apply upstream's qh_gethash patch
- Silence %%setup.
- Remove rpath.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2003.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2003.1-11
- fix license tag

* Tue Mar 04 2008 Ralf Corsépius <rc040203@freenet.de> - 2003.1-10
- Add qhull-2003.1-alias.patch (BZ 432309)
  Thanks to Orion Poplawski (orion@cora.nwra.com).

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 2003.1-9
- Rebuild for gcc43.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 2003.1-8
- Mass rebuild.

* Wed Jun 20 2007 Ralf Corsépius <rc040203@freenet.de> - 2003.1-7
- Remove *.la.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 2003.1-6
- Mass rebuild.

* Fri Feb 17 2006 Ralf Corsépius <rc040203@freenet.de> - 2003.1-5
- Disable static libs.
- Fixup some broken links in doc.
- Add %%{?dist}.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2003.1-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Aug 08 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.2
- Use default documentation installation scheme.

* Fri Jul 16 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.1
- Initial Fedora RPM.
