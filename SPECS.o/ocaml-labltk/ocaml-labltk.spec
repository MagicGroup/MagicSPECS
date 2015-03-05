%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

Name:          ocaml-labltk
Version:       8.06.0
Release:       1%{?dist}

Summary:       Tcl/Tk interface for OCaml

License:       LGPLv2+ with exceptions

URL:           https://forge.ocamlcore.org/projects/labltk/
Source0:       https://forge.ocamlcore.org/frs/download.php/1455/labltk-8.06.0.tar.gz

# This adds debugging (-g) everywhere.
Patch1:        labltk-8.06.0-enable-debugging.patch

BuildRequires: ocaml
BuildRequires: tcl-devel, tk-devel


%description
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).


%package devel
Summary:       Tcl/Tk interface for OCaml

Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).

This package contains the development files.


%prep
%setup -q -n labltk-%{version}

%patch1 -p1

# Remove version control files which might get copied into documentation.
find -name .gitignore -delete


%build
./configure
%if !%{native_compiler}
make %{?_smp_mflags} byte
%else
make %{?_smp_mflags} all
make %{?_smp_mflags} opt
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/labltk \
    STUBLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
# The *.o files are not installed by the Makefile.  AIUI
# that prevents linking with native code programs.
install -m 0644 camltk/*.o $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk


%files
%doc Changes README.mlTk
%dir %{_libdir}/ocaml/labltk
%{_libdir}/ocaml/labltk/*.cmi
%{_libdir}/ocaml/labltk/*.cma
%{_libdir}/ocaml/labltk/*.cmo
%{_libdir}/ocaml/stublibs/dlllabltk.so


%files devel
%doc README.mlTk
%doc examples_camltk
%doc examples_labltk
%{_bindir}/labltk
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/labltk/labltktop
%{_libdir}/ocaml/labltk/pp
%{_libdir}/ocaml/labltk/tkcompiler
%{_libdir}/ocaml/labltk/*.a
%if %{native_compiler}
%{_libdir}/ocaml/labltk/*.cmxa
%{_libdir}/ocaml/labltk/*.cmx
%{_libdir}/ocaml/labltk/*.o
%endif
%{_libdir}/ocaml/labltk/*.mli


%changelog
* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-1
- New upstream version 8.06.0.
- Big jump in upstream version numbers to match Tk versions.
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.7.beta1
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.6.beta1
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-0.5.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.4.beta1
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.3.beta1
- OCaml 4.02.0 beta rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.2.beta1
- Enable debugging.
- Move labltk to -devel package.
- Enable _smp_flags.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.1.beta1
- Initial packaging of new out-of-tree ocaml-labltk.
