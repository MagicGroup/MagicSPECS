Name:           glpk
Version:        4.47
Release:        2%{?dist}
Summary:        GNU Linear Programming Kit

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://www.gnu.org/software/glpk/glpk.html
Source0:        ftp://ftp.gnu.org/gnu/glpk/glpk-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The GLPK (GNU Linear Programming Kit) package is intended for solving
large-scale linear programming (LP), mixed integer programming (MIP),
and other related problems. It is a set of routines written in ANSI C
and organized in the form of a callable library.

GLPK supports the GNU MathProg language, which is a subset of the AMPL
language.

The GLPK package includes the following main components:

 * Revised simplex method.
 * Primal-dual interior point method.
 * Branch-and-bound method.
 * Translator for GNU MathProg.
 * Application program interface (API).
 * Stand-alone LP/MIP solver. 

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation

%description    doc
Documentation subpackage for %{name}.


%package devel
Summary:        Development headers and files for GLPK
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The glpk-devel package contains libraries and headers for developing
applications which use GLPK (GNU Linear Programming Kit).


%package utils
Summary:        GLPK-related utilities and examples
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description utils
The glpk-utils package contains the standalone solver programs glpksol
and tspsol that use GLPK (GNU Linear Programming Kit).


%package static
Summary:        Static version of GLPK libraries
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
The glpk-static package contains the statically linkable version of
the GLPK (GNU Linear Programming Kit) libraries.


%prep
%setup -q

%build
export LIBS=-ldl
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} libdir=$RPM_BUILD_ROOT%{_libdir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}

%check
make check
## Clean up directories that are included in docs
rm -Rf examples/{.deps,.libs,Makefile*,glpsol,glpsol.o} doc/*.tex

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING README
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS
%{_includedir}/glpk.h

%files utils
%defattr(-,root,root)
%{_bindir}/*

%files static
%defattr(-,root,root)
%{_libdir}/*.a
%exclude %{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc doc examples


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 4.47-2
- 为 Magic 3.0 重建

* Thu Oct 27 2011 Conrad Meyer <konrad@tylerc.org> - 4.47-1
- Bump to latest upstream.

* Sun Apr 24 2011 Conrad Meyer <konrad@tylerc.org> - 4.45-3
- Add %%clean section as per #696792

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 8 2010 Conrad Meyer <konrad@tylerc.org> - 4.45-1
- Bump to latest stable upstream, 4.45.

* Tue Sep 28 2010 Conrad Meyer <konrad@tylerc.org> - 4.44-1
- Bump to latest stable upstream, 4.44.

* Mon Jul 5 2010 Conrad Meyer <konrad@tylerc.org> 4.43-2
- Move header to normal includedir

* Sat Feb 20 2010 Conrad Meyer <konrad@tylerc.org> 4.43-1
- Bump to 4.43.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> 4.42-1
- Bump to 4.42.

* Tue Dec 22 2009 Conrad Meyer <konrad@tylerc.org> 4.41-1
- Bump to 4.41.

* Wed Nov 4 2009 Conrad Meyer <konrad@tylerc.org> 4.40-1
- Bump to 4.40.

* Sat Aug 8 2009 Conrad Meyer <konrad@tylerc.org> 4.39-1
- Bump to 4.39.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Conrad Meyer <konrad@tylerc.org> - 4.36-3
- Split out -doc subpackage.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> 4.36-1
- Bump to 4.36.

* Tue Jan 27 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.35-1
- Update to 4.35.

* Fri Dec 12 2008 Conrad Meyer <konrad@tylerc.org> 4.34-1
- Update to 4.34.

* Thu Sep 25 2008 Conrad Meyer <konrad@tylerc.org> 4.31-1
- Update to 4.31.

* Tue May  6 2008 Quentin Spencer <qspencer@users.sf.net> 4.28-1
- Update to release 4.28.
- Add LIBS definition to configure step so it compiles correctly.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.25-2
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Quentin Spencer <qspencer@users.sf.net> 4.25-1
- Update to release 4.25.

* Fri Sep 14 2007 Quentin Spencer <qspencer@users.sf.net> 4.21-1
- New release. Update license tag to GPLv3.

* Thu Aug 23 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-3
- Rebuild for F8.

* Thu Aug  9 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-2
- Add pre and postun scripts to run ldconfig.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-1
- New release.
- Split static libs into separate package.

* Thu Jun 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.18-1
- New release.

* Wed Mar 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.15-1
- New release. Shared libraries are now supported.

* Tue Dec 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.13-1
- New release.

* Tue Aug 29 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-2
- Rebuild for FC6.

* Tue Jul 25 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-1
- New release.

* Fri May 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.10-1
- New release.

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-2
- Add dist tag

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-1
- New release.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-3
- Remove utils dependency on base package, since it doesn't exist until
  shared libraries are enabled.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-2
- Add -fPIC to compile flags.

* Fri Jul 22 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-1
- First version.
