Name:           cloog
%global         tarball_name %{name}
Version:	0.18.4
Release:	1%{?dist}
Epoch:		1
Summary:        The Chunky Loop Generator

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.cloog.org

# This tarball was retrieved directly from the Git source code
# repository of the Cloog project by doing:
#
#    git clone git://repo.or.cz/cloog.git -b cloog-0.18.3 cloog-0.18.3
#    tar -cvf cloog-0.18.3.tar.gz cloog-0.18.3

Source0:        http://www.bastoul.net/cloog/pages/download/cloog-%{version}.tar.gz

BuildRequires:  isl-devel >= 0.12
BuildRequires:  gmp-devel >= 4.1.3
BuildRequires:  texinfo >= 4.12
BuildRequires:  texinfo-tex >= 4.12
BuildRequires:  libtool
Obsoletes:	cloog-ppl cloog-ppl-devel

Requires(post): info
Requires(preun): info

%description
CLooG is a software which generates loops for scanning Z-polyhedra. That is,
CLooG finds the code or pseudo-code where each integral point of one or more
parametrized polyhedron or parametrized polyhedra union is reached. CLooG is
designed to avoid control overhead and to produce a very efficient code.

%package devel
Summary:        Development tools for the Chunky Loop Generator
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       isl-devel >= 0.12, gmp-devel >= 4.1.3

%description devel
The header files and dynamic shared libraries of the Chunky Loop Generator.

%prep
%setup -q -n %{tarball_name}-%{version}

%build

%configure \
    --with-isl=system \
    --with-isl-prefix=%{_prefix}

# Remove the cloog.info in the tarball
# to force the re-generation of a new one
test -f doc/cloog.info && rm doc/cloog.info

# Remove the -fomit-frame-pointer compile flag
# Use system libtool to disable standard rpath
make %{?_smp_mflags} AM_CFLAGS= LIBTOOL=%{_bindir}/libtool
make %{?_smp_mflags} AM_CFLAGS= LIBTOOL=%{_bindir}/libtool -C doc
# cloog.pdf

%install
%make_install INSTALL="%{__install} -p"
# GCC wants the library to be named libcloog.so, as it's what it uses
# at runtime.
rm %{buildroot}%{_libdir}/*/*.cmake
mkdir -p %{buildroot}%{_docdir}/cloog-%{version}
%{__install} -m0644 -p README ChangeLog %{buildroot}%{_docdir}/cloog-%{version}

%clean
rm -rf %{buildroot}

%files
%{_docdir}/cloog-%{version}/README
%{_docdir}/cloog-%{version}/ChangeLog
%{_bindir}/cloog
%{_libdir}/libcloog-isl.so.*

%files devel
%{_includedir}/cloog
%{_libdir}/libcloog-isl.so
%{_libdir}/pkgconfig/cloog-isl.pc
%exclude %{_libdir}/libcloog-isl.a
%exclude %{_libdir}/libcloog-isl.la
#%{_docdir}/cloog-%{version}/cloog.pdf

%post
/sbin/ldconfig
test -f %{_infodir}/%{name}.info \
     && /sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  test -f %{_infodir}/%{name}.info && \
      /sbin/install-info \
          --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%changelog
* Sun Aug 02 2015 Liu Di <liudidi@gmail.com> - 1:0.18.4-1
- 更新到 0.18.4

* Sun Aug 02 2015 Liu Di <liudidi@gmail.com> - 1:0.18.3-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 David Howells <dhowells@redhat.com> - 1:0.18.3-1
      	     	  Dodji Seketeli <dodji@seketeli.org>
- Update to upstream cloog-0.18.3
- Obsoletes the previous cloog-ppl package.
- Requires isl-devel.
- Ship the ChangeLog file.
- Ship the libcloog-isl.so* files.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.15.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.15.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Adam Williamson <awilliam@redhat.com> - 1:0.15.11-8
- rebuild for new libppl

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.15.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.15.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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

