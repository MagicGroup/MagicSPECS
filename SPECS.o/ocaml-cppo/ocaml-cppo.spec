%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-cppo
Version: 1.1.2
Release: 1%{?dist}
Summary:        Equivalent of the C preprocessor for OCaml programs
Summary(zh_CN.UTF-8): 相当于 C 预处理器的 OCaml 程序

License:        BSD
URL:            http://mjambon.com/cppo.html
Source0:        http://mjambon.com/releases/cppo/cppo-%{version}.tar.gz

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
%if !%{opt}
Requires:       ocaml >= 3.10.0
%endif

%define libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Cppo is an equivalent of the C preprocessor targeted at the OCaml
language and its variants.

The main purpose of cppo is to provide a lightweight tool for simple
macro substitution (＃define) and file inclusion (＃include) for the
occasional case when this is useful in OCaml. Processing specific
sections of files by calling external programs is also possible via
＃ext directives.

The implementation of cppo relies on the standard library of OCaml and
on the standard parsing tools Ocamllex and Ocamlyacc, which contribute
to the robustness of cppo across OCaml versions.

%description -l zh_CN.UTF-8
相当于 C 预处理器的 OCaml 程序。

%prep
%setup -q -n %{libname}-%{version}
sed -i.add-debuginfo \
    's/ocamlopt/ocamlopt -g/;s/ocamlc \(-[co]\)/ocamlc -g \1/' \
    Makefile


%build
%if %opt
make %{?_smp_mflags} opt
%else
make %{?_smp_mflags} all
%endif


%install
%{__install} -d $RPM_BUILD_ROOT%{_bindir}
%{__install} -p cppo $RPM_BUILD_ROOT%{_bindir}/
magic_rpm_clean.sh

%check
make test


%files
%doc LICENSE Changes
%{_bindir}/cppo


%changelog
* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 1.1.2-1
- 更新到 1.1.2

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.3-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 0.9.3-3
- Removing ExclusiveArch

* Mon Jan 27 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-1
- Initial package
