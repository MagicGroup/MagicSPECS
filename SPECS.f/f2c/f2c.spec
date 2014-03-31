Name:           f2c
Summary:        A Fortran 77 to C/C++ conversion program
Version:        20110801
Release:        4%{?dist}
License:        MIT
Group:          Development/Languages
URL:            http://netlib.org/f2c/
Source:         ftp://netlib.org/f2c.tar
# Patch makefile to build a shared library
Patch:          f2c-20110801.patch
BuildRequires:  unzip
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:       %{name}-libs = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

%package libs
Summary:    Dynamic libraries from %{name}
Group:      Development/Libraries

%description libs
Dynamic libraries from %{name}.

%prep
%setup -q -n %{name}
mkdir libf2c
pushd libf2c
unzip ../libf2c.zip
popd
%patch

%build
cp src/makefile.u src/Makefile
cp libf2c/makefile.u libf2c/Makefile
make -C src %{?_smp_mflags} CFLAGS="%{optflags}" f2c
make -C libf2c %{?_smp_mflags} CFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}
install -D -p -m 644 f2c.h %{buildroot}%{_includedir}/f2c.h
install -D -p -m 755 src/f2c %{buildroot}%{_bindir}/f2c
install -D -p -m 644 src/f2c.1t %{buildroot}%{_mandir}/man1/f2c.1
install -D -p -m 755 libf2c/libf2c.so.0.23 %{buildroot}%{_libdir}/libf2c.so.0.23
ln -s libf2c.so.0.23 %{buildroot}%{_libdir}/libf2c.so.0
ln -s libf2c.so.0.23 %{buildroot}%{_libdir}/libf2c.so

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc f2c.ps f2c.pdf readme changes src/README
%{_bindir}/f2c
%{_mandir}/man1/f2c.1*
%{_includedir}/f2c.h
%{_libdir}/libf2c.so

%files libs
%defattr(-,root,root,-)
%doc permission disclaimer src/Notice
%{_libdir}/libf2c.so.*


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110801-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110801-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Carl Byington <carl@five-ten-sg.com> 20110801-1
- update to newer upstream version
- patch from Jaroslav Škarvada for 4 byte ints on x86_64

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090411-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090411-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 07 2010 Carl Byington <carl@five-ten-sg.com> 20090411-6
- Subpackage Licensing, move Notice to -libs.

* Sun Dec 05 2009 Carl Byington <carl@five-ten-sg.com> 20090411-5
- fully versioned provides

* Sat Dec 05 2009 Carl Byington <carl@five-ten-sg.com> 20090411-4
- remove -devel subpackage, merge it into the main package which
  provides -devel and requires -libs.

* Sat Dec 05 2009 Carl Byington <carl@five-ten-sg.com> 20090411-3
- remove patch backups
- add comment for patch purpose

* Thu Dec 03 2009 Carl Byington <carl@five-ten-sg.com> 20090411-2
- add symlink to fix rpmlint error
- remove unnecessary parts of the patch, which enables building a
  shared library.
- main package now requires -devel since that is needed to be useful.
- summary changed to specify this only works on F77 code.
- %%files use explicit libf2c rather than * wildcard

* Wed Dec 02 2009 Carl Byington <carl@five-ten-sg.com> 20090411-1
- update to newer upstream version
- add .pdf documentation also
- trim changelog
- move all the license related files into -libs, and both the
  main package and -devel require -libs, to avoid either duplicating
  files or installing any package without the license files.

* Sun Nov 25 2009 Carl Byington <carl@five-ten-sg.com> 20031026-3.0.3
- don't install the static library.
- preserve the alpha architecture patch and ifdef in the spec file
  even if it is not used by fedora.
- split off -libs and -devel packages.
- full version/release in requires

* Wed Nov 25 2009 Carl Byington <carl@five-ten-sg.com> 20031026-3.0.2
- convert to fedora compatible spec file.

* Sat Jun 14 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 20031026-3.0.1
- Fix not utf-8 specfile entries.

