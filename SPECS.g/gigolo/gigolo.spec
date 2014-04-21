Name:           gigolo
Version:        0.4.1
Release:        4%{?dist}
Summary:        GIO/GVFS management application

Group:          User Interface/Desktops
License:        GPLv2
URL:            http://goodies.xfce.org/projects/applications/gigolo/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/apps/%{name}/%{majorver}/%{name}-%{version}.tar.bz2
# http://git.xfce.org/apps/gigolo/commit/?id=95a37d4c
Patch0:         gigolo-0.4.1-update-de.po.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=748228
# patch from http://git.xfce.org/apps/gigolo/commit/?id=0e53ec5c
Patch1:         gigolo-0.4.1-fix-crash-748228.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils

Requires: %{_bindir}/gvfs-open
Requires: %{_bindir}/fusermount

Obsoletes: sion < 0.1.0-3

%description
A frontend to easily manage connections to remote filesystems using GIO/GVFS. 
It allows you to quickly connect/mount a remote filesystem and manage
bookmarks of such. 

%prep
%setup -q
#%patch0 -p1 -b .updat
#%patch1 -p1 -b .fix

%build
export CFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
              --exec-prefix=%{_exec_prefix} \
              --bindir=%{_bindir} \
              --sbindir=%{_sbindir} \
              --sysconfdir=%{_sysconfdir} \
              --datadir=%{_datadir} \
              --includedir=%{_includedir} \
              --libdir=%{_libdir} \
              --libexecdir=%{_libexecdir} \
              --localstatedir=%{_localstatedir} \
              --sharedstatedir=%{_sharedstatedir} \
              --mandir=%{_mandir} --infodir=%{_infodir} --enable-debug

./waf build -v

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT ./waf install 

# remove docs that waf installs in the wrong place
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/gigolo

desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.I18N TODO THANKS
%{_bindir}/gigolo
%{_datadir}/applications/gigolo.desktop
%{_mandir}/man1/gigolo.1.gz

%changelog
* Sun Apr 06 2014 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 更新到

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.4.1-4
- 为 Magic 3.0 重建

* Sun Oct 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-3
- Fix crash when closing gigolo from the toolbar (#748228)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 01 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.1
- Patch to fix German translation
 
* Thu Dec 31 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 18 2009 Kevin Fenzi <kevin@tummy.com> - 0.3.2-1
- Update to 0.3.2

* Sat Apr 04 2009 Kevin Fenzi <kevin@tummy.com> - 0.3.1-1
- Update to 0.3.1

* Tue Mar 31 2009 Kevin Fenzi <kevin@tummy.com> - 0.3.0-1
- Update to 0.3.0 

* Sun Feb 22 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.1-1
- Update to 0.2.1
- Add THANKS
- Fix waf configure line and use local waf.

* Sun Feb 15 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.0-2
- Fix CFLAGS
- Fix build to be verbose
- Use Fedora waf
- Remove vendor

* Sun Feb 15 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.0-1
- Change name to gigolo
- Update to 0.2.0

* Sun Jan 04 2009 Kevin Fenzi <kevin@tummy.com> - 0.1.0-2
- Fix License tag
- Add Requires for needed binaries

* Fri Jan 02 2009 Kevin Fenzi <kevin@tummy.com> - 0.1.0-1
- Initial version for Fedora
