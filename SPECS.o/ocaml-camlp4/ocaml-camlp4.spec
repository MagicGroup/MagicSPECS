%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

# We're building from the 4.02 branch.  As the releases are
# rather intermittent, build git versions instead.
%global gitcommit cf1935d38ce90b023e2445219f39bd5027db44d5
%global shortcommit cf1935d3

Name:          ocaml-camlp4
Version:       4.02.1
Release:       0.4.git%{shortcommit}%{?dist}

Summary:       Pre-Processor-Pretty-Printer for OCaml
Summary(zh_CN.UTF-8): OCaml 的预处理程序

License:       LGPLv2+ with exceptions

URL:           https://github.com/ocaml/camlp4
Source0:       https://github.com/ocaml/camlp4/archive/%{gitcommit}/camlp4-%{gitcommit}.tar.gz

# This package used to be part of the upstream compiler.  We still
# need to keep it in lock step with the compiler, so whenever a new
# compiler is released we will also update this package also.
BuildRequires: ocaml = %{version}
Requires:      ocaml-runtime = %{version}


%description
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the runtime files.

%description -l zh_CN.UTF-8
这是 OCaml 的一个预处理程序，可以解析源文件并在标准输出上打印出结果。
这个包包含了运行库。

%package devel
Summary:       Pre-Processor-Pretty-Printer for OCaml
Summary(zh_CN.UTF-8): %{name} 的开发包

Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.

This package contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n camlp4-%{gitcommit}


%build
./configure
# Incompatible with parallel builds:
unset MAKEFLAGS
%if !%{native_compiler}
make byte
%else
make all
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
make install \
  BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
  PKGDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
magic_rpm_clean.sh

%files
%doc README.md LICENSE
%dir %{_libdir}/ocaml/camlp4
%{_libdir}/ocaml/camlp4/*.cmi
%{_libdir}/ocaml/camlp4/*.cma
%{_libdir}/ocaml/camlp4/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Filters
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Parsers
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmo
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmi
%dir %{_libdir}/ocaml/camlp4/Camlp4Printers
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmo
%dir %{_libdir}/ocaml/camlp4/Camlp4Top
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmi
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmo


%files devel
%doc LICENSE
%{_bindir}/camlp4*
%{_bindir}/mkcamlp4
%if %{native_compiler}
%{_libdir}/ocaml/camlp4/*.a
%{_libdir}/ocaml/camlp4/*.cmxa
%{_libdir}/ocaml/camlp4/*.cmx
%{_libdir}/ocaml/camlp4/*.o
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Filters/*.o
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Parsers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Printers/*.o
%{_libdir}/ocaml/camlp4/Camlp4Top/*.cmx
%{_libdir}/ocaml/camlp4/Camlp4Top/*.o
%endif


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 4.02.1-0.4.gitcf1935d3
- 为 Magic 3.0 重建

* Wed Mar 04 2015 Liu Di <liudidi@gmail.com> - 4.02.1-0.3.gitcf1935d3
- 为 Magic 3.0 重建

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-0.2.gitcf1935d3
- ocaml-4.02.1 rebuild.
- Update to latest upstream git release from branch 4.02.

* Mon Nov 03 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.8.git87c6a6b0
- Bump version and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.7.git87c6a6b0
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.6.git87c6a6b0
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02.0-0.5.git87c6a6b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.4.git87c6a6b0
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Sat Jul 19 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.3.git87c6a6b0
- OCaml 4.02.0 beta rebuild.

* Wed Jul 16 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.2
- Initial packaging of new out-of-tree ocaml-camlp4.
