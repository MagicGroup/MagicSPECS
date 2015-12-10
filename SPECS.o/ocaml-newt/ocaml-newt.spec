%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-newt
Version:        0.9
Release:        23%{?dist}
Summary:        OCaml library for using newt text mode window system
Summary(zh_CN.UTF-8): 使用 newt 文本模式窗口系统的 OCaml 库
License:        LGPLv2+ with exceptions

URL:            http://et.redhat.com/~rjones/ocaml-newt/
Source0:        http://et.redhat.com/~rjones/ocaml-newt/%{name}-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  chrpath
BuildRequires:  ocaml-camlidl-devel
#BuildRequires:  newt-devel > 0.52.7
BuildRequires:  newt-devel


%description
This is a set of OCaml bindings to newt.

The newt windowing system is a terminal-based window and widget
library designed for writing applications with a simple, but
user-friendly, interface.  While newt is not intended to provide the
rich feature set advanced applications may require, it has proven to
be flexible enough for a wide range of applications (most notably, the
Red Hat installation process).

%description -l zh_CN.UTF-8
使用 newt 文本模式窗口系统的 OCaml 库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
Requires:       newt-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
# Parallel builds don't work.
unset MAKEFLAGS
./configure --libdir=%{_libdir}
# Dependencies are broken in the upstream package.
make newt_int.mli
rm -f .depend
make depend

make all
%if %opt
make opt
%endif
make doc


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so
magic_rpm_clean.sh

%files
%doc COPYING.LIB
%{_libdir}/ocaml/newt
%if %opt
%exclude %{_libdir}/ocaml/newt/*.a
%exclude %{_libdir}/ocaml/newt/*.cmxa
%exclude %{_libdir}/ocaml/newt/*.cmx
%endif
%exclude %{_libdir}/ocaml/newt/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.LIB README examples/*.ml html
%if %opt
%{_libdir}/ocaml/newt/*.a
%{_libdir}/ocaml/newt/*.cmxa
%{_libdir}/ocaml/newt/*.cmx
%endif
%{_libdir}/ocaml/newt/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 0.9-23
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.9-22
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.9-21
- 为 Magic 3.0 重建

* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 0.9-20
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9-19
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9-17
- OCaml 4.01.0 rebuild.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.9-14
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9-12
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9-11
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9-9
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9-8
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9-6
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-4
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-3
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-2
- Rebuild for OCaml 3.10.2

* Tue Mar 18 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9-1
- New upstream release 0.9.

* Tue Mar 18 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7-1
- New upstream release 0.7.
- Move configure into the build section.

* Fri Mar 14 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6-1
- New upstream release 0.6.

* Thu Mar 13 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4-1
- Initial RPM release.
