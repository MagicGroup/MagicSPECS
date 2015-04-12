%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%global dlnode  822

Name:           ocaml-bin-prot
Version:        2.0.9
Release:        10%{?dist}
Summary:        Read and write OCaml values in a type-safe binary protocol
Summary(zh_CN.UTF-8): 使用类型安全的二进制协议读取和写入 OCaml 值
License:        LGPLv2+ with exceptions

URL:            http://forge.ocamlcore.org/projects/bin-prot
Source0:        http://forge.ocamlcore.org/frs/download.php/%{dlnode}/bin_prot-%{version}.tar.gz

# Remove -Werror from flags.
Patch1:         ocaml-bin-prot-2.0.9-remove-Werror.patch
# Update integer types for ocaml 4.02
Patch2:         %{name}-2.0.9-fix-ints.patch

BuildRequires:  ocaml >= 3.12.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-type-conv >= 3.0.4
BuildRequires:  chrpath


%description
This library contains functionality for reading and writing OCaml
values in a type-safe binary protocol. These functions are extremely
efficient and provide users with a convenient and safe way of
performing I/O on any extensionally defined data type. This means that
functions, objects, and values whose type is bound through a
polymorphic record field are not supported, but everything else is.

As of now, there is no support for cyclic or shared values. Cyclic
values will lead to non-termination whereas shared values, besides
requiring significantly more space when encoded, may lead to a
substantial increase in memory footprint when they are read back in.

%description -l zh_CN.UTF-8
使用类型安全的二进制协议读取和写入 OCaml 值。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n bin_prot-%{version}
%patch1 -p1
%patch2 -p1

%build
ocaml setup.ml -configure --prefix %{_prefix} \
      --libdir %{_libdir} \
      --libexecdir %{_libexecdir} \
      --exec-prefix %{_exec_prefix} \
      --bindir %{_bindir} \
      --sbindir %{_sbindir} \
      --mandir %{_mandir} \
      --datadir %{_datadir} \
      --localstatedir %{_localstatedir} \
      --sharedstatedir %{_sharedstatedir} \
      --destdir $RPM_BUILD_ROOT
ocaml setup.ml -build


%check
ocaml setup.ml -test


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocaml setup.ml -install

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
magic_rpm_clean.sh

%files
%doc COPYRIGHT LICENSE LICENSE.Tywith
%{_libdir}/ocaml/bin_prot
%if %opt
%exclude %{_libdir}/ocaml/bin_prot/*.a
%exclude %{_libdir}/ocaml/bin_prot/*.cmxa
%endif
%exclude %{_libdir}/ocaml/bin_prot/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc Changelog README.txt
%if %opt
%{_libdir}/ocaml/bin_prot/*.a
%{_libdir}/ocaml/bin_prot/*.cmxa
%endif
%{_libdir}/ocaml/bin_prot/*.mli


%changelog
* Wed Mar 04 2015 Liu Di <liudidi@gmail.com> - 2.0.9-10
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.0.9-9
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.9-8
- Remove -Werror from compiler flags.  Fixes FTBFS (RHBZ#1106613).
- Move configure into build section (instead of prep).
- Use global instead of define.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 2.0.9-6
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.0.9-3
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Richard W.M. Jones <rjones@redhat.com> - 2.0.9-1
- New upstream version 2.0.9.
- Recompile for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 2.0.7-1
- New upstream version 2.0.7.
- Rebuild for OCaml 3.12.1.

* Wed Sep 28 2011 Michael Ekstrand <michael@elehack.net> - 2.0.6-1
- New upstream version from forge.ocamlcore.org (#741484)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.24-1
- New upstream version 1.2.24.
- Fix upstream URL.
- Rebuild for OCaml 3.12.0.

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.21-1
- New upstream version 1.2.21.
- Change %%define to %%global.
- Use upstream RPM 4.8 OCaml dependency generator.

* Mon Nov  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.20-2
- The final license of the code is LGPLv2+ with the OCaml linking
  exception.  It was derived from earlier BSD code.
- Don't duplicate the license files across base and -devel packages.
- Add note to spec about inclusion of *.ml file in -devel package.

* Mon Oct 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.20-1
- New upstream version 1.2.20.

* Sat Sep  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.18-1
- New upstream version 1.2.18.

* Fri May 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-3
- Force signed chars when compiling, as per comment from upstream author.
- Remove the part in the description which says this is only
  supported on little endian architectures.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-2
- Remove ExclusiveArch, but add a Fedora README file warning about
  shortcomings on non-x86 architectures.
- Added missing dependency ocaml-type-conv.
- Move *.ml file to devel package.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-1
- Initial RPM release.
