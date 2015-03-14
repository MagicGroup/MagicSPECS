%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if !%{opt}
%global debug_package %{nil}
%endif

Name:           ocaml-biniou
Version:        1.0.9
Release:        5%{?dist}
Summary:        Safe and fast binary data format
Summary(zh_CN.UTF-8): 安全快速的二进制数据格式

License:        BSD
URL:            http://mjambon.com/biniou.html
Source0:        http://mjambon.com/releases/biniou/biniou-%{version}.tar.gz

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-easy-format-devel
BuildRequires:  ocaml-ocamldoc

%global libname %(sed -e 's/^ocaml-//' <<< %{name})

%description
Biniou (pronounced "be new") is a binary data format designed for
speed, safety, ease of use and backward compatibility as protocols
evolve. Biniou is vastly equivalent to JSON in terms of functionality
but allows implementations several times faster (4 times faster than
yojson), with 25-35%% space savings.

Biniou data can be decoded into human-readable form without knowledge
of type definitions except for field and variant names which are
represented by 31-bit hashes. A program named bdump is provided for
routine visualization of biniou data files.

%description -l zh_CN.UTF-8
安全快速的二进制数据格式。

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
sed -i.add-debuginfo \
    's/ocamlopt/ocamlopt -g/;s/ocamlc \(-[co]\)/ocamlc -g \1/' \
    Makefile


%build
# not thread safe - intermittent build failures as per 1.0.2
# see http://www.cmake.org/pipermail/cmake/2010-January/034746.html
# for similar problem
%global _smp_mflags %{nil}
make %{?_smp_mflags} all
%if %opt
make %{?_smp_mflags} opt
%endif
make %{?_smp_mflags} META


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export PREFIX=$RPM_BUILD_ROOT%{_prefix}
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $OCAMLFIND_DESTDIR
make install #DESTDIR=$RPM_BUILD_ROOT

%if %opt
# avoid potential future name conflict
mv $RPM_BUILD_ROOT%{_bindir}/{,ocaml-}bdump
%endif
magic_rpm_clean.sh

%check
make test


%files
%doc LICENSE
%{_libdir}/ocaml/%{libname}/
%if %opt
%exclude %{_libdir}/ocaml/*/*.a
%exclude %{_libdir}/ocaml/*/*.cmxa
%exclude %{_libdir}/ocaml/*/*.cmx
%exclude %{_libdir}/ocaml/*/*.o
%endif
%exclude %{_libdir}/ocaml/*/*.mli


%files devel
%doc LICENSE README.md Changes
%if %opt
%{_bindir}/ocaml-bdump
%{_libdir}/ocaml/*/*.a
%{_libdir}/ocaml/*/*.cmxa
%{_libdir}/ocaml/*/*.cmx
%{_libdir}/ocaml/*/*.o
%endif
%{_libdir}/ocaml/*/*.mli


%changelog
* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 1.0.9-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 1.0.9-3
- Removing ExclusiveArch

* Thu Jan 23 2014 Michel Salim <salimma@fedoraproject.org> - 1.0.9-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 1.0.9-1
- Initial package
