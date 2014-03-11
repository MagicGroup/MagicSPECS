%global xfceversion 4.10

Name:           xfce4-dev-tools
Version:        4.10.0
Release:        2%{?dist}
Summary:        Xfce developer tools

Group:          Development/Tools
License:        GPLv2+
URL:            http://xfce.org/~benny/projects/xfce4-dev-tools/
#VCS git:git://git.xfce.org/xfce/xfce4-dev-tools
Source0:        http://archive.xfce.org/src/xfce/xfce4-dev-tools/%{xfceversion}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext-devel
BuildRequires:  gtk-doc
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  make
BuildRequires:  glib2-devel
Requires:       glib2-devel

%description
This package contains common tools required by Xfce developers and people
that want to build Xfce from SVN.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} INSTALL='install -p'

mkdir $RPM_BUILD_ROOT%{_datadir}/aclocal/
install -p -m 644 m4macros/xdt*.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal/ 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog HACKING NEWS README
%{_bindir}/xdt-autogen
%{_bindir}/xdt-commit
%{_bindir}/xdt-csource
%dir %{_datadir}/xfce4/
%{_datadir}/xfce4/dev-tools/
%{_datadir}/aclocal/*

%changelog
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.2-1
- Update to 4.9.2 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1
- Packge is no longer noarch.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final. 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Oct 31 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Mon Sep 21 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Sun Sep 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1

* Wed Aug 19 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sun Dec 28 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Sep 08 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.0.1-1
- Update to 4.4.0.1

* Tue Aug 12 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.4.0-2
- Fix license tag.

* Mon Jan 22 2007 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0.

* Sat Nov 11 2006 Christoph Wickert <cwickert@fedoraproject.org> - 4.3.99.2-1
- Update to 4.3.99.2.

* Tue Oct 03 2006 Christoph Wickert <cwickert@fedoraproject.org> - 4.3.99.1-3
- Require gettext-devel.
- Install m4 macros also to /usr/share/aclocal.

* Tue Oct 03 2006 Christoph Wickert <cwickert@fedoraproject.org> - 4.3.99.1-2
- Some more requires: glib2-devel, make and gtk-doc.
- Own %%{_datadir}/xfce4

* Sat Sep 23 2006 Christoph Wickert <cwickert@fedoraproject.org> - 4.3.99.1-1
- Initial Fedora Extras release.
