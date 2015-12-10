%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-SDL
Version:        0.9.1
Release:        7%{?dist}
Summary:        OCaml bindings for SDL
Summary(zh_CN.UTF-8): SDL 的 OCaml 绑定
License:        LGPLv2+

URL:            http://ocamlsdl.sourceforge.net
Source0:        http://downloads.sourceforge.net/ocamlsdl/ocamlsdl-%{version}.tar.gz
Source1:        ocamlsdl-0.7.2-htmlref.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml-lablgl-devel
BuildRequires:  SDL_ttf-devel, SDL_mixer-devel, SDL_image-devel 
BuildRequires:  ocaml
Requires:       ocaml


%description
Runtime libraries to allow programs written in OCaml to write to SDL 
(Simple DirectMedia Layer) interfaces.

%description -l zh_CN.UTF-8
SDL 的 OCaml 绑定。

%package        devel
Summary:        Development files for ocamlSDL
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release} 


%description    devel
The ocamlSDL-devel package provides libraries and headers for developing 
applications using ocamlSDL

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n ocamlsdl-%{version} -a 1


%build
%configure
make %{?_smp_mflags}



%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%files
%doc README COPYING AUTHORS NEWS
%{_libdir}/ocaml/sdl
%{_libdir}/ocaml/stublibs/*.so*
%if %opt
%exclude %{_libdir}/ocaml/sdl/*.a
%exclude %{_libdir}/ocaml/sdl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/sdl/*.mli


%files devel
%doc htmlref/
%if %opt
%{_libdir}/ocaml/sdl/*.a
%{_libdir}/ocaml/sdl/*.cmxa
%endif
%{_libdir}/ocaml/sdl/*.mli


%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 0.9.1-7
- 为 Magic 3.0 重建

* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.9.1-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.9.1-5
- 为 Magic 3.0 重建

* Sat Mar 14 2015 Liu Di <liudidi@gmail.com> - 0.9.1-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.1-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-1
- New upstream version 0.9.1.
- OCaml 4.01.0 rebuild.
- Modernize the spec file.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Bruno Wolff III <bruno@wolff.to> - 0.8.0-7
- Rebuild for OCaml 4.0.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.0-5
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.0-4
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Richard W.M. Jones <rjones@redhat.com> - 0.8.0-2
- New upstream version 0.8.0.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-21
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-19
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-17
- Force rebuild.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-16
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-15
- Rebuild for OCaml 3.11.0

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7.2-14
- fix license tag

* Mon Jun  2 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-13
- labgl -> ocaml-lablgl-devel

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-12
- Rebuild for OCaml 3.10.2.

* Sat Apr 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-11
- Add commas in dependencies & rebuild.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> 0.7.2-10
- Rebuild for ppc64.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> 0.7.2-9
- *.so.owner files aren't being generated by this ocamlfind.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> 0.7.2-8
- Rebuild for OCaml 3.10.1.
- Generate correct provides and requires.
- Fix 'make install' rule for new ocamlfind.
- Fix paths to conform with OCaml packaging guidelines.

* Wed May 09 2007 Nigel Jones <dev@nigelj.com> 0.7.2-7
- ExcludeArch ppc64 until ocaml builds

* Fri May 04 2007 Nigel Jones <dev@nigelj.com> 0.7.2-6
- Fix download URL and remove ldconfig

* Fri May 04 2007 Nigel Jones <dev@nigelj.com> 0.7.2-5
- Minor fixups per review

* Thu May 03 2007 Nigel Jones <dev@nigelj.com> 0.7.2-4
- Rename per policy
- Revert -3 changes
- Add htmlref

* Thu Apr 26 2007 Nigel Jones <dev@nigelj.com> 0.7.2-3
- Provide ocamlSDL-static, add COPYING to -devel as docs.

* Wed Apr 11 2007 Nigel Jones <dev@nigelj.com> 0.7.2-2
- Fix missing dependencies

* Tue Apr 10 2007 Nigel Jones <dev@nigelj.com> 0.7.2-1
- Initial spec file

