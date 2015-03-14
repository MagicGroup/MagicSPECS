%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-easy-format
Version:        1.0.2
Release:        6%{?dist}
Summary:        High-level and functional interface to the Format module
Summary(zh_CN.UTF-8): 格式化棋块的高级的函数化的接口

License:        BSD
URL:            http://mjambon.com/easy-format.html
Source0:        http://mjambon.com/releases/easy-format/easy-format-%{version}.tar.gz

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc

%global libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
This module offers a high-level and functional interface to the Format
module of the OCaml standard library. It is a pretty-printing
facility, i.e. it takes as input some code represented as a tree and
formats this code into the most visually satisfying result, breaking
and indenting lines of code where appropriate.

Input data must be first modeled and converted into a tree using 3
kinds of nodes:

    atoms
    lists
    labeled nodes

Atoms represent any text that is guaranteed to be printed as-is. Lists
can model any sequence of items such as arrays of data or lists of
definitions that are labeled with something like "int main", "let x
=" or "x:".

%description -l zh_CN.UTF-8
格式化棋块的高级的函数化的接口。

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
sed -i.add-debuginfo 's/ocamlopt/ocamlopt -g/;s/ocamlc \(-[co]\)/ocamlc -g \1/' Makefile


%build
# not thread safe - intermittent build failures as per 1.0.2
# see http://www.cmake.org/pipermail/cmake/2010-January/034746.html
# for similar problem
%global _smp_mflags %{nil}
%if %opt
make %{?_smp_mflags}
%else
make %{?_smp_mflags} all
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
make install
magic_rpm_clean.sh

%check
make test


%files
%doc LICENSE
%{_libdir}/ocaml/%{libname}/
%if %opt
%exclude %{_libdir}/ocaml/*/*.cmx
%exclude %{_libdir}/ocaml/*/*.o
%endif
%exclude %{_libdir}/ocaml/*/*.mli


%files devel
%doc LICENSE README.md Changes
%if %opt
%{_libdir}/ocaml/*/*.cmx
%{_libdir}/ocaml/*/*.o
%endif
%{_libdir}/ocaml/*/*.mli


%changelog
* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 1.0.2-6
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.0.2-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-3
- Remove ocaml_arches (see rhbz#1087794).

* Tue Jan 21 2014 Michel Salim <salimma@fedoraproject.org> - 1.0.2-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 1.0.2-1
- Initial package
