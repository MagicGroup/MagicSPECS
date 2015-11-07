%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-yojson
Version:        1.1.8
Release:        7%{?dist}
Summary:        An optimized parsing and printing library for the JSON format
Summary(zh_CN.UTF-8): 优化的解析和打印 JSON 格式的库

License:        BSD
URL:            http://mjambon.com/yojson.html
Source0:        http://mjambon.com/releases/yojson/yojson-%{version}.tar.gz
# Example JSON files for testing
Source1:        test-valid.json
Source2:        test-invalid.json

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-biniou-devel
BuildRequires:  ocaml-cppo
BuildRequires:  ocaml-easy-format-devel

%global libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Yojson is an optimized parsing and printing library for the JSON
format. It addresses a few shortcomings of json-wheel including 2x
speedup, polymorphic variants and optional syntax for tuples and
variants.

ydump is a pretty-printing command-line program provided with the
yojson package.

The program atdgen can be used to derive OCaml-JSON serializers and
deserializers from type definitions.

%description -l zh_CN.UTF-8
优化的解析和打印 JSON 格式的库。

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


%build
# not SMP-safe
make META all
%if %opt
make opt
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export PREFIX=$RPM_BUILD_ROOT%{_prefix}
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $OCAMLFIND_DESTDIR
make install
magic_rpm_clean.sh

%check
# Against valid JSON
$RPM_BUILD_ROOT%{_bindir}/ydump %{SOURCE1} >/dev/null 2>valid-err.log
[ -z "$(cat valid-err.log)" ]

# Against invalid JSON
[ ! $($RPM_BUILD_ROOT%{_bindir}/ydump %{SOURCE2} 2>/dev/null) ]


%files
%doc LICENSE
%{_libdir}/ocaml/%{libname}/
%if %opt
%{_bindir}/ydump
%exclude %{_libdir}/ocaml/*/*.cmx
%exclude %{_libdir}/ocaml/*/*.o
%endif
%exclude %{_libdir}/ocaml/*/*.mli


%files devel
%doc LICENSE README.md Changes examples
%if %opt
%{_libdir}/ocaml/*/*.cmx
%{_libdir}/ocaml/*/*.o
%endif
%{_libdir}/ocaml/*/*.mli


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.8-7
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 1.1.8-6
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.1.8-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 1.1.8-3
- Removing ExclusiveArch

* Sat Feb  8 2014 Michel Salim <salimma@fedoraproject.org> - 1.1.8-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 1.1.8-1
- Initial package
