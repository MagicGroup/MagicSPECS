# OCaml has a bytecode backend that works on anything with a C
# compiler, and a native code backend available on a subset of
# architectures.  A further subset of architectures support native
# dynamic linking.
#
# This package contains a single file needed to define some RPM macros
# which are required before any SRPM is built.
#
# See also: https://bugzilla.redhat.com/show_bug.cgi?id=1087794

%global macros_dir %{_rpmconfigdir}/macros.d

Name:           ocaml-srpm-macros
Version:        2
Release:        5%{?dist}

Summary:        OCaml architecture macros
Summary(zh_CN.UTF-8): OCaml 架构的宏
License:        GPLv2+

BuildArch:      noarch

Source0:        macros.ocaml-srpm

# NB. This package MUST NOT Require anything (except for dependencies
# that RPM itself generates).

%description
This package contains macros needed by RPM in order to build
SRPMS.  It does not pull in any other OCaml dependencies.


%prep


%build


%install
mkdir -p $RPM_BUILD_ROOT%{macros_dir}
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT%{macros_dir}/macros.ocaml-srpm


%files
%{macros_dir}/macros.ocaml-srpm


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2-5
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 2-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Move macros to _rpmconfigdir (RHBZ#1093528).

* Tue Apr 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1-1
- New package.
