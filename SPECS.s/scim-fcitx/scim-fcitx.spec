Name:           scim-fcitx
Version:        3.1.1
Release:        21%{?dist}
Summary:        FCITX Input Method Engine for SCIM

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.scim-im.org/projects/imengines/
Source0:        http://dl.sourceforge.net/scim/%{name}.%{version}.tar.bz2

BuildRequires:  scim-devel
Requires:	scim

Patch0:         scim-fcitx-3.1.1-gcc43.patch
Patch1:         scim-fcitx-3.1.1-gcc47.patch

%description
scim-fcitx is a port of the fcitx Chinese input method for the SCIM input
method platform.  It provides Wubi, Erbi, Cangjie, and Pinyin styles of input.


%package tools
Summary:    Fcitx tables tools
Group:      Development/Libraries

%description tools
This package contains input table tools from fcitx.


%prep
%setup -q -n fcitx
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .gcc47


%build
%configure --disable-static
# doesn't build with %{?_smp_mflags}
make


%install
make DESTDIR=${RPM_BUILD_ROOT} install

rm ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/IMEngine/fcitx.la

pushd ${RPM_BUILD_ROOT}/%{_bindir}/
  mv createPYMB createPYMB3
  mv mb2txt mb2txt3
  mv txt2mb txt2mb3
popd

%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/scim-1.0/*/IMEngine/fcitx.so
%{_datadir}/scim/fcitx
%{_datadir}/scim/icons/fcitx


%files tools
%defattr(-, root, root)
%{_bindir}/*


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.1.1-20
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012  Peng Wu <pwu@redhat.com> - 3.1.1-14
- Rename conflicted files with fcitx.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 29 2008 Huang Peng <phuang@redhat.com> - 3.1.1-9
- Fix build  error with GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.1-8
- Autorebuild for GCC 4.3

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 3.1.1-7
- update license field to GPLv2+
- remove with_libstdc_preview macro

* Wed Sep 27 2006 Jens Petersen <petersen@redhat.com> - 3.1.1-6
- rebuild for FE6

* Tue Apr  4 2006 Jens Petersen <petersen@redhat.com> - 3.1.1-5.fc6
- rebuild without libstdc++so7

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 3.1.1-4.fc5
- rebuild for FE5

* Mon Feb 13 2006 Jens Petersen <petersen@redhat.com> - 3.1.1-3
- build conditionally with libstdc++so7 preview library (#166041)
  - add with_libstdc_preview switch and tweak libtool to link against it
- update filelist since moduledir is now api-versioned

* Tue Dec 20 2005 Jens Petersen <petersen@redhat.com> - 3.1.1-2
- package cleanup (John Mahowald)

* Wed Oct  5 2005 Jens Petersen <petersen@redhat.com> - 3.1.1-1
- initial packaging for Fedora Extras.

* Mon Jun 20 2005 Jens Petersen <petersen@redhat.com>
- rebuild against scim-1.3.1

* Tue Jun 14 2005 Jens Petersen <petersen@redhat.com>
- initial build

* Thu May  5 2005 Haojun Bao <baohaojun@yahoo.com>
- first release of scim-fcitx.
