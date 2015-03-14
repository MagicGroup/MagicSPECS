%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%if %opt
%global target native
%else
%global target byte
%global debug_package %{nil}
%endif

Name:           ocaml-menhir
Version:	20141215
Release:	1%{?dist}
Summary:        LR(1) parser generator for OCaml
Summary(zh_CN.UTF-8): OCaml 的 LR(1) 解析器生成器

# The library is LGPLv2+ with a linking exception.
# The remaining code is QPL, with an exception granted to clause 6c.
License:        (QPL with exceptions) and (LGPLv2+ with exceptions)
URL:            http://gallium.inria.fr/~fpottier/menhir/
Source0:        http://gallium.inria.fr/~fpottier/menhir/menhir-%{version}.tar.gz

BuildRequires:  ocaml
BuildRequires:  ocaml-findlib

%description
Menhir is a LR(1) parser generator for the Objective Caml programming
language.  That is, Menhir compiles LR(1) grammar specifications down to
OCaml code.  Menhir was designed and implemented by François Pottier and
Yann Régis-Gianas.

%description -l zh_CN.UTF-8
OCaml 的 LR(1) 解析器生成器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
License:        LGPLv2+ with exceptions
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files
for developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n menhir-%{version}

# Fix encodings
for f in AUTHORS menhir.1 src/standard.mly; do
  iconv -f ISO8859-1 -t UTF-8 $f > $f.fixed
  touch -r $f $f.fixed
  mv -f $f.fixed $f
done

# Fix a dependency
sed "s|/usr/bin/env ocaml|/usr/bin/ocaml|" demos/ocamldep.wrapper > foo
touch -r demos/ocamldep.wrapper foo
mv -f foo demos/ocamldep.wrapper
chmod a+x demos/ocamldep.wrapper

# Prevent embedding buildroot paths into the executable
sed -i 's/install: all/install:/' Makefile

# Enable debuginfo
sed -i 's/-j 0/-cflag -g -lflag -g &/' src/Makefile

%build
make PREFIX=%{_prefix} TARGET=%{target}
make -C demos clean

%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
make install PREFIX=$RPM_BUILD_ROOT%{_prefix} TARGET=%{target}
rm -fr $RPM_BUILD_ROOT%{_docdir}/menhir

# Install the ocamldep wrapper
mv demos/ocamldep.wrapper $RPM_BUILD_ROOT%{_bindir}/menhir-ocamldep
magic_rpm_clean.sh

%files
%doc AUTHORS CHANGES LICENSE manual.pdf demos
%{_bindir}/menhir*
%{_mandir}/man1/menhir.1*
%{_datadir}/menhir/

%files devel
%{_libdir}/ocaml/menhirLib/

%changelog
* Mon Mar 09 2015 Liu Di <liudidi@gmail.com> - 20141215-1
- 更新到 20141215

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 20140422-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140422-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Jerry James <loganjerry@gmail.com> - 20140422-1
- New upstream version
- Fix standard.mly character encoding

* Fri Apr 18 2014 Jerry James <loganjerry@gmail.com> - 20130911-3
- Remove ocaml_arches macro (bz 1087794)

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 20130911-2
- Rebuild for OCaml 4.01.0

* Thu Sep 12 2013 Jerry James <loganjerry@gmail.com> - 20130911-1
- New upstream version
- Allow debuginfo generation since ocaml 4 supports it

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130116-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Jerry James <loganjerry@gmail.com> - 20130116-1
- New upstream version

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 20120123-5
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120123-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 20120123-3
- Rebuild for OCaml 4.00.0.

* Fri Jun  8 2012 Jerry James <loganjerry@gmail.com> - 20120123-2
- Rebuild for OCaml 4.00.0

* Mon Jan 23 2012 Jerry James <loganjerry@gmail.com> - 20120123-1
- New upstream version

* Fri Jan  6 2012 Jerry James <loganjerry@gmail.com> - 20111019-3
- Rebuild for ocaml 3.12.1

* Mon Dec 19 2011 Jerry James <loganjerry@gmail.com> - 20111019-2
- Change the subpackages to match Debian
- Add patch to allow building demos outside of the menhir source tree

* Wed Nov  9 2011 Jerry James <loganjerry@gmail.com> - 20111019-1
- Initial RPM
