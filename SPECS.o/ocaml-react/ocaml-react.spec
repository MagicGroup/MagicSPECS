%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-react
Version: 0.9.4
Release: 8%{?dist}
Summary:        OCaml framework for Functional Reactive Programming (FRP)
Summary(zh_CN.UTF-8): 函数响应式编程 (FRP) 的 OCaml 框架

License:        BSD
URL:            http://erratique.ch/software/react

Source0:        http://erratique.ch/software/react/releases/react-%{version}.tbz
Source1:        react-LICENSE

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc


%description
React is an OCaml module for functional reactive programming (FRP). It
provides support to program with time varying values : applicative
events and signals. React doesn't define any primitive event or
signal, this lets the client chooses the concrete timeline.

React is made of a single, independent, module and distributed under
the new BSD license.

Given an absolute notion of time Rtime helps you to manage a timeline
and provides time stamp events, delayed events and delayed signals.

%description -l zh_CN.UTF-8
函数响应式编程 (FRP) 的 OCaml 框架。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n react-%{version}
cp -p %{SOURCE1} LICENSE
ocaml setup.ml -configure --prefix %{_prefix} --destdir $RPM_BUILD_ROOT


%build
ocaml setup.ml -build 

%if %opt
# Build the tests.
ocamlbuild test/tests.otarget
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocaml setup.ml -install
magic_rpm_clean.sh

%check
%if %opt
./_build/test/test.native
#./_build/test/clock.native
#./_build/test/breakout.native
%endif


%files
%doc LICENSE
%{_libdir}/ocaml/react
%if %opt
%exclude %{_libdir}/ocaml/react/*.cmx
%endif
%exclude %{_libdir}/ocaml/react/*.mli


%files devel
%doc CHANGES README
%if %opt
%{_libdir}/ocaml/react/*.cmx
%endif
%{_libdir}/ocaml/react/*.mli


%changelog
* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 0.9.4-8
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.4-7
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-5
- Remove ocaml_arches macro (RHBZ#1087794).

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com>
- Rebuild for OCaml 4.01.0
- Enable debuginfo
- Add missing ExclusiveArch
- Minor spec file cleanups

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-1
- New upstream version 0.9.4.
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-4
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-3
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-1
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-2
- Initial RPM release.
- Use global instead of define (Till Maas).
