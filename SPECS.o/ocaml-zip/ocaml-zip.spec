%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-zip
Version:        1.05
Release:        7%{?dist}
Summary:        OCaml library for reading and writing zip, jar and gzip files
Summary(zh_CN.UTF-8): 读写 zip, jar 和 gzip 文件的 OCaml 库
License:        LGPLv2 with exceptions

URL:            http://forge.ocamlcore.org/projects/camlzip/
Source0:        https://forge.ocamlcore.org/frs/download.php/1037/camlzip-%{version}.tar.gz
Patch1:		ocaml-zip-1.05-fix-ints.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  zlib-devel >= 1.1.3
BuildRequires:  chrpath


%description
This Objective Caml library provides easy access to compressed files
in ZIP and GZIP format, as well as to Java JAR files. It provides
functions for reading from and writing to compressed files in these
formats.

%description -l zh_CN.UTF-8
读写 zip, jar 和 gzip 文件的 OCaml 库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n camlzip-%{version}
%patch1 -p0

%build
make all
%if %opt
make allopt
%endif
chrpath --delete dll*.so

cat > META <<EOF
name = "%{name}"
version = "%{version}"
description = "%{description}"
requires = "unix"
archive(byte) = "zip.cma"
archive(native) = "zip.cmxa"
EOF


%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml/zip
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml/stublibs

export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

ocamlfind install zip *.cma *.cmxa *.a *.cmx *.cmi *.mli dll*.so META
magic_rpm_clean.sh

%files
%doc LICENSE
%{_libdir}/ocaml/zip
%if %opt
%exclude %{_libdir}/ocaml/zip/*.a
%exclude %{_libdir}/ocaml/zip/*.cmxa
%exclude %{_libdir}/ocaml/zip/*.cmx
%endif
%exclude %{_libdir}/ocaml/zip/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc LICENSE Changes README
%if %opt
%{_libdir}/ocaml/zip/*.a
%{_libdir}/ocaml/zip/*.cmxa
%{_libdir}/ocaml/zip/*.cmx
%endif
%{_libdir}/ocaml/zip/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 1.05-7
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1.05-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.05-5
- 为 Magic 3.0 重建

* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 1.05-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.05-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.05-1
- New upstream version 1.05.
- OCaml 4.01.0 rebuild.
- Modernize spec file.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.04-10
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.04-8
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.04-7
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Richard W.M. Jones <rjones@redhat.com> - 1.04-5
- Project has moved, new source URLs.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.04-4
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.04-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Mon Mar 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.04-1
- New upstream release (resolves rhbz#490407).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-6
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-5
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-4
- Rebuild for OCaml 3.10.2

* Mon Mar 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-3
- Add unix as a dependency to the META-file (rhbz #439652).

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-2
- Rebuild for ppc64.

* Fri Feb 22 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-1
- Initial RPM release.
