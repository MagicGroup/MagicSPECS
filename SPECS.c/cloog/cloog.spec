Name:           cloog
%define         tarball_name %{name}-ppl
Version:        0.15.11
Release:        5%{?dist}
Epoch:		1
Summary:        The Chunky Loop Generator

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.cloog.org
Source0:        ftp://gcc.gnu.org/pub/gcc/infrastructure/%{tarball_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{tarball_name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:		cloog-ppl-0.15.11-ppl-verfix.patch

BuildRequires:  ppl-devel >= 0.10
BuildRequires:  gmp-devel >= 4.1.3
BuildRequires:  texinfo >= 4.12
BuildRequires:  libtool

Requires(post): info
Requires(preun): info

%description
CLooG is a software which generates loops for scanning Z-polyhedra. That is,
CLooG finds the code or pseudo-code where each integral point of one or more
parametrized polyhedron or parametrized polyhedra union is reached. CLooG is
designed to avoid control overhead and to produce a very efficient code.

%package ppl
Summary: Parma Polyhedra Library backend (ppl) based version of the Cloog binaries
Group: Development/Libraries
%description ppl
The dynamic shared libraries of the Chunky Loop Generator

%package ppl-devel
Summary:        Development tools for the ppl based version of Chunky Loop Generator
Group:          Development/Libraries
Requires:       %{name}-ppl = %{epoch}:%{version}-%{release}
Requires:       ppl-devel >= 0.10, gmp-devel >= 4.1.3
%description ppl-devel
The header files and dynamic shared libraries of the Chunky Loop Generator.

%prep
%setup -q -n %{tarball_name}-%{version}
%patch0 -p1 -b .verfix

%build
%configure --with-ppl

# Remove the cloog.info in the tarball
# to force the re-generation of a new one
test -f doc/cloog.info && rm doc/cloog.info

# Remove the -fomit-frame-pointer compile flag
# Use system libtool to disable standard rpath
make %{?_smp_mflags} AM_CFLAGS= LIBTOOL=%{_bindir}/libtool


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p" install
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files ppl
%defattr(-,root,root,-)
%doc README LICENSE
%{_infodir}/cloog.info*gz
%{_bindir}/cloog
%{_libdir}/libcloog.so.*

%files ppl-devel
%defattr(-,root,root,-)
%{_includedir}/cloog
%{_libdir}/libcloog.so
%exclude %{_libdir}/libcloog.a
%exclude %{_libdir}/libcloog.la

%post ppl
/sbin/ldconfig
test -f %{_infodir}/%{name}.info \
     && /sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun ppl
if [ $1 = 0 ] ; then
  test -f %{_infodir}/%{name}.info && \
      /sbin/install-info \
          --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun ppl -p /sbin/ldconfig

%changelog
* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 1:0.15.11-5
- roll back to 0.15.11

* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 0.16.1-4
- undo hacks

* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 0.16.1-3
- put the hacky provides in the right place

* Mon Dec  3 2012 Tom Callaway <spot@fedoraproject.org> - 0.16.1-2
- hack to get the compilers built (will go away)

* Fri Nov 30 2012 Tom Callaway <spot@fedoraproject.org> - 0.16.1-1
- update to 0.16.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.11-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.11-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15.11-2.1
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15.11-2
- rebuilt once again with new gmp

* Tue Oct 18 2011  <dodji@redhat.com> - 0.15.11-1
- Update to cloog 0.15.11

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 0.15.9-2.1
- rebuild with new gmp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010  <dodji@redhat.com> - 0.15.9-1
- Long overdue update to upstream revision 0.15.9
- Upstream fixes:
  http://gcc.gnu.org/PR43012
  Memory leaks
  Use top_builddir, not undefined builddir
  Uninitialised configure variables
  Compilation with -Wc++-compat
  Import cloog_domain_scatter from cloog trunk.
- Remove unused git_revision macro.
- Upate download URL to ftp://gcc.gnu.org/pub/gcc/infrastructure

* Mon Mar 01 2010 Dodji Seketeli <dodji@redhat.com> - 0.15-7-1
- Add README and LICENSE file to package
- Escape '%%' character in the changelog

* Sat Aug 15 2009 Dodji Seketeli <dodji@redhat.com> - 0.15.7-1
- Update to new upstream version (0.15.7)
- Do not build from git snapshot anymore. Rather, got the tarball from
  ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-ppl-0.15.7.tar.gz
- The upstream tarball is named cloog-ppl, not cloog. Adjusted thusly.
- Use system libtool to disable standard rpath
- Do not try to touch the info file if it's not present. Closes #515929.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.10.gitb9d79
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Dodji Seketeli <dodji@redhat.com> - 0.15-0.9.gitb9d79
- Update to new upstream git snapshot.
- Update some comments in the spec file.

* Thu Apr 09 2009 Dodji Seketeli <dodji@redhat.com> - 0.15-0.8.git1334c
- Update to new upstream git snapshot
- Drop the cloog.info patch as now upstreamed
- No need to add an argument to the --with-ppl
  configure switch anymore as new upstream fixed this

* Wed Apr 08 2009 Dodji Seketeli <dodji@redhat.org> - 0.15-0.7.gitad322
- Add BuildRequire texinfo needed to regenerate the cloog.info doc

* Wed Apr 08 2009 Dodji Seketeli <dodji@redhat.org> - 0.15-0.6.gitad322
- Remove the cloog.info that is in the tarball
  That forces the regeneration of a new cloog.info with
  suitable INFO_DIR_SECTION, so that install-info doesn't cry
  at install time.
- Slightly changed the patch to make install-info actually
  install the cloog information in the info directory file.
- Run install-info --delete in %%preun, not in %%postun,
  otherwise the info file is long gone with we try to
  run install-info --delete on it.

* Mon Apr 06 2009 Dodji Seketeli <dodji@redhat.org> - 0.15-0.5.gitad322
- Added patch to fix #492794
- Need to add an argument to the --with-ppl switch now.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.4.gitad322
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Dodji Seketeli <dodji@redhat.org> 0.15-0.3.gitad322
- Updated to upstream git hash foo
- Generate cloog-ppl and cloog-ppl-devel packages instead of cloog and
  cloog-devel.

* Mon Dec 01 2008 Dodji Seketeli <dodji@redhat.com> 0.15-0.2.git57a0bc
- Updated to upstream git hash 57a0bcd97c08f44a983385ca0389eb624e66e3c7
- Remove the -fomit-frame-pointer compile flag

* Wed Sep 24 2008 Dodji Seketeli <dodji@redhat.com> 0.15-0.1.git95753
- Initial version from git hash 95753d83797fa9a389c0c07f7cf545e90d7867d7

