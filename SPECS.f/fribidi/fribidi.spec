Summary: Library implementing the Unicode Bidirectional Algorithm
Summary(zh_CN.UTF-8): Unicode 双向算法实现库
Name: fribidi
Version:	0.19.6
Release: 5%{?dist}
URL: http://fribidi.org
Source0: http://fribidi.org/download/%{name}-%{version}.tar.bz2
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake, autoconf, libtool, pkgconfig

%description
A library to handle bidirectional scripts (for example Hebrew, Arabic),
so that the display is done in the proper way; while the text data itself
is always written in logical order.

%description -l zh_CN.UTF-8
处理双向脚本的为（比如希伯来语、阿拉伯语等）。

%package devel
Summary: Libraries and include files for FriBidi
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %{version}-%{release}
Requires: pkgconfig

%description devel
Include files and libraries needed for developing applications which use
FriBidi.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%if 0%{?el5}
# FORTIFY_SOURCE=2 breaks EL-5 build
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's|FORTIFY_SOURCE=2|FORTIFY_SOURCE=1|'`
%ifarch ppc ppc64 x86_64
export CFLAGS="$CFLAGS -DPAGE_SIZE=4096"
%endif
%else
# outside of EL-5, only ppc* needs modification
%ifarch ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -DPAGE_SIZE=4096"
%endif
%endif
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README AUTHORS COPYING ChangeLog THANKS NEWS TODO
%{_bindir}/fribidi
%{_libdir}/libfribidi.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/fribidi
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/%{name}_*.gz

%changelog
* Fri Apr 04 2014 Liu Di <liudidi@gmail.com> - 0.19.6-5
- 更新到 0.19.6

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.19.2-5
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 0.19.2-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Behdad Esfahbod <besfahbo@redhat.com> 0.19.2-1
- Update to 0.19.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.19.1-3
- rebuild to get provides pkgconfig(fribidi)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.19.1-2
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Caolan McNamara <caolanm@redhat.com> 0.19.1-1
- next version
- workaround PAGE_SIZE requirement

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> 0.10.9-2
- rebuild

* Fri Aug 10 2007 Caolan McNamara <caolanm@redhat.com> 0.10.9-1
- next version

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> 0.10.8-2
- clarify license

* Thu May 31 2007 Caolan McNamara <caolanm@redhat.com> 0.10.8-1
- next version

* Mon Feb 05 2007 Caolan McNamara <caolanm@redhat.com> 0.10.7-6
- Resolves: rhbz#225771 spec cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.10.7-5.1
- rebuild

* Thu Jun 29 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-5
- rh#197223# devel Require pkg-config

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.10.7-4
- put devel .so symlink in the right subpackage

* Tue May 23 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-3
- rh#192669# clearly I didn't actually get around to basing fribidi-config 
  of pkg-config output

* Tue May 02 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-2
- base fribidi-config on pkg-config output
- allow fribidi_config.h to be the same on 32 and 64 bit

* Mon Mar 27 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-1
- latest version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.10.4-8.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.10.4-8.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 0.10.4-8
- rebuild with gcc4

* Wed Feb 09 2005 Caolan McNamara <caolanm@redhat.com> 0.10.4-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 24 2003 Jeremy Katz <katzj@redhat.com> 0.10.4-4
- update description
- include docs (#104964)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig to post/postun

* Fri May 16 2003 Jeremy Katz <katzj@redhat.com> 0.10.4-2
- Initial build in Red Hat Linux

