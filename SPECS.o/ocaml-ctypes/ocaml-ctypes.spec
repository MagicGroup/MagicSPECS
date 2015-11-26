%define		module	ctypes
Summary:	Library for binding to C libraries using pure OCaml
Name:		ocaml-%{module}
Version:	0.4.1
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://github.com/ocamllabs/ocaml-ctypes/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	08a284c379e341d57b6918611b5bc56b
URL:		https://github.com/ocamllabs/ocaml-ctypes
BuildRequires:	libffi-devel
BuildRequires:	ocaml >= 3.04-7
# archs with ocaml_opt support (keep in sync with ocaml.spec)
ExclusiveArch:	%{ix86} x86_64 arm aarch64 ppc sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ctypes is a library for binding to C libraries using pure OCaml.
The primary aim is to make writing C extensions as straightforward
as possible.

The core of ctypes is a set of combinators for describing
the structure of C types -- numeric types, arrays, pointers, structs,
unions and functions. You can use these combinators to describe the
types of the functions that you want to call, then bind directly to
those functions -- all without writing or generating any C!

This package contains files needed to run bytecode executables using
this library.

%package devel
Summary:	Library for binding to C libraries using pure OCaml - development part
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains files needed to develop OCaml programs using
ctypes library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia programów w OCamlu
wykorzystujących bibliotekę ctypes.

%prep
%setup -q

%build
%{__make} -j1 all \
	CC="%{__cc} %{optflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ctypes/CHANGES.md
# findlib files, useless when packaging to rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes-foreign-base_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes_stubs.so
%dir %{_libdir}/ocaml/%{module}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%{_libdir}/ocaml/%{module}/*.cma

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/*.h
%{_libdir}/ocaml/%{module}/*.cm[ix]
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.[ao]
%{_libdir}/ocaml/%{module}/*.cmxa
%{_libdir}/ocaml/site-lib/%{module}
#{_examplesdir}/%{name}-%{version}

%changelog
* Sat Jul 25 2015 PLD Linux Team <feedback@pld-linux.org>
- For complete changelog see: http://git.pld-linux.org/?p=packages/ocaml-ctypes.git;a=log;h=master

* Sat Jul 25 2015 Jakub Bogusz <qboosh@pld-linux.org> dbd2b6b
- dynlinkable files (.cmxs, .cma) moved to base; release 2

* Sat Jul 18 2015 Jakub Bogusz <qboosh@pld-linux.org> cfd8525
- updated to 0.4.1

* Sun Mar 22 2015 Jan Rękorajski <baggins@pld-linux.org> 8f3cb7b
- rel 2

* Thu Mar 19 2015 Jakub Bogusz <qboosh@pld-linux.org> 4954302
- package module dir

* Fri Mar 13 2015 Jakub Bogusz <qboosh@pld-linux.org> 83a1bfa
- complete list of archs with opt support

* Fri Mar 13 2015 Jakub Bogusz <qboosh@pld-linux.org> adbf453
- pl, BR: libffi-devel

* Sun Mar 01 2015 Elan Ruusamäe <glen@delfi.ee> 4dafc5b
- cleanup

* Sun Mar 01 2015 Jan Rękorajski <baggins@pld-linux.org> 6e15805
- this is native only library, so can't disable opt
- updated files

* Sun Mar 01 2015 Jan Rękorajski <baggins@pld-linux.org> 32e46e2
- +10 to jbj for meaningfull error messages

* Sun Mar 01 2015 Jan Rękorajski <baggins@pld-linux.org> 7ab0e45
- work around rpmbuild parsing issues

* Sun Mar 01 2015 Jan Rękorajski <baggins@pld-linux.org> 0c952b3
- new

