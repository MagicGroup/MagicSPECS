Name:		SDL_net
Version:	1.2.8
Release:	3%{?dist}
Summary:	SDL portable network library
Summary(zh_CN.UTF-8): SDL 可移植网络库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL_net/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	SDL-devel >= 1.2.4-1


%description
This is a portable network library for use with SDL.
%description -l zh_CN.UTF-8
SDL 可移植网络库。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4-1
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/SDL/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 1.2.8-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.8-2
- 为 Magic 3.0 重建

* Tue Jan 31 2012 Jon Ciesla <limburgher@gmail.com> - 1.2.8-1
- New upstream.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 07 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.2.7-7
- rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-4
- Rebuild for gcc-4.3.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-3
- Rebuild.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-2
- Update license tag.

* Mon Jul 30 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7.
- Drop requires on SDL. devel soname will pull it in.

* Thu Aug 31 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.2.6-2
- Rebuild for FC6.

* Fri Aug 25 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6.
- Simplify description & summary for devel package.
- Use disable-static configure flag.
- Drop ppc64 patch.
- Drop 137525 patch, fixed upstream.

* Mon Feb 13 2006 Brian Pepple <bdpepple@ameritech.net> - 1.2.5-8
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Sep 27 2005 Brian Pepple <bdpepple@ameritech.net> - 1.2.5-7
- General spec formatting cleanup.
- Add dist tag.

* Thu Jun  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.5-6
- Add SDL-devel dependency to -devel, remove duplicate docs.
- Remove trailing semicolon from "extern C" block in SDL_net.h (#137525, Kees).

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 1.2.5-4
- rebuild

* Wed Feb  9 2005 Thomas Woerner <twoerner@redhat.com> 1.2.5-3
- rebuild

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar  9 2004 Thomas Woerner <twoerner@redhat.com> 1.2.5-1
- new version 1.2.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 1.2.4-6
- ppc64 fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 01 2002 Elliot Lee <sopwith@redhat.com>
- Remove unpackaged files

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.4-1
- 1.2.4

* Fri Feb 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-2
- Rebuild in new environment

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.3-1
- 1.2.3
- remove obsolete dependencies
- Clean up spec file

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.2-1
- Add build dependencies (#49829)
- Update to 1.2.2 (bugfix release) while at it
- s/Copyright/License/

* Tue Jul 10 2001 Elliot Lee <sopwith@redhat.com>
- Rebuild

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Initial Red Hat build
