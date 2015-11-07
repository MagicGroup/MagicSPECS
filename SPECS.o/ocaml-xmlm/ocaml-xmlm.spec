%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-xmlm
Version:        1.2.0
Release:        8%{?dist}
Summary:        A streaming XML codec
Summary(zh_CN.UTF-8): 流式 XML 编码器

License:        BSD
URL:            http://erratique.ch/software/xmlm
Source0:        http://erratique.ch/software/xmlm/releases/xmlm-%{version}.tbz
# Ensure source files are included in generated debuginfo subpackage
Patch0:         xmlm-1.2.0-debug.patch
# Example XML files for testing
Source1:        test-valid.xml
Source2:        test-invalid.xml

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib

%global libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Xmlm is an OCaml streaming codec to decode and encode the XML data
format. It can process XML documents without a complete in-memory
representation of the data.

%description -l zh_CN.UTF-8
流式 XML 编码器。

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
%setup -q -n %{libname}-%{version}
%patch0 -p1 -b .debug


%build
%if %{opt}
./pkg/build true
%else
./pkg/build false
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $OCAMLFIND_DESTDIR/%{libname}

%if %{opt}
install -m 755 -p _build/test/xmltrip.native $RPM_BUILD_ROOT%{_bindir}/xmltrip
install -m 644 -p _build/src/xmlm.{a,cmxa} $OCAMLFIND_DESTDIR/%{libname}/
install -m 755 -p _build/src/xmlm.cmxs $OCAMLFIND_DESTDIR/%{libname}/
%else
install -m 755 -p _build/test/xmltrip.byte $RPM_BUILD_ROOT%{_bindir}/xmltrip
%endif
install -m 644 -p _build/pkg/META _build/src/xmlm.{cm?,mli} $OCAMLFIND_DESTDIR/%{libname}/
magic_rpm_clean.sh

%check
# Against valid XML
$RPM_BUILD_ROOT%{_bindir}/xmltrip -p %{SOURCE1} 2>valid-err.log
[ -z "$(cat valid-err.log)" ]

# Against invalid XML - stderr should contain the word expected
$RPM_BUILD_ROOT%{_bindir}/xmltrip -p %{SOURCE2} 2>invalid-err.log
grep expected invalid-err.log >/dev/null

%files
# LICENSE not bundled
%doc README.md
%{_bindir}/xmltrip
%{_libdir}/ocaml/xmlm/
%if %opt
%exclude %{_libdir}/ocaml/*/*.a
%exclude %{_libdir}/ocaml/*/*.cmxa
%exclude %{_libdir}/ocaml/*/*.cmxs
%exclude %{_libdir}/ocaml/*/*.cmx
%endif
%exclude %{_libdir}/ocaml/*/*.mli


%files devel
# LICENSE not bundled
%doc CHANGES.md _build/test/examples.ml _build/test/xhtml.ml doc
%if %opt
%{_libdir}/ocaml/*/*.a
%{_libdir}/ocaml/*/*.cmxa
%{_libdir}/ocaml/*/*.cmxs
%{_libdir}/ocaml/*/*.cmx
%endif
%{_libdir}/ocaml/*/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.2.0-8
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 1.2.0-7
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.2.0-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 1.2.0-4
- Removing ExclusiveArch

* Fri Feb 14 2014 Michel Salim <salimma@fedoraproject.org> - 1.2.0-3
- Include source files in -debuginfo

* Sat Feb  8 2014 Michel Salim <salimma@fedoraproject.org> - 1.2.0-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 1.2.0-1
- Initial package
