Name:           telepathy-rakia
Version:	0.8.0
Release:	1%{?dist}
Summary:        SIP connection manager for Telepathy
Summary(zh_CN.UTF-8): Telepathy 的 SIP 连接管理器

Group:          Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/Components
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  telepathy-glib-devel >= 0.17.7
BuildRequires:  sofia-sip-glib-devel >= 1.12.11
BuildRequires:  libxslt
BuildRequires:  python
BuildRequires:  gtk-doc
# Build Requires needed for tests.
BuildRequires:	python-twisted
BuildRequires:	dbus-python
BuildRequires:	pygobject2
# Drop the following once 0.7.5 is released.
BuildRequires:  autoconf

Requires:       telepathy-filesystem

Provides: 	telepathy-sofiasip = %{version}-%{release}
Obsoletes: 	telepathy-sofiasip < 0.7.2


%description
%{name} is a SIP connection manager for the Telepathy
framework based on the SofiaSIP-stack. 

%description -l zh_CN.UTF-8
Telepathy 的 SIP 连接管理器。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%check
#make check


%install
make install DESTDIR=$RPM_BUILD_ROOT
# Let's not install the headers
rm -rf $RPM_BUILD_ROOT%{_includedir}/%{name}-0.7

%files
%doc COPYING README NEWS TODO
%{_libexecdir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/managers/*.manager
%{_mandir}/man8/%{name}.8.gz


%changelog
* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 0.8.0-1
- 更新到 0.8.0

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.7.4-3
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4.
- Bump minimum version of tp-glib.
- Add patch to fix DSO linking bug.

* Mon Jan 09 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.7.3-2
- Rebuild for new gcc.

* Thu Oct 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.3-1
- Update to 0.7.3.

* Sat Oct 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.2-3
- Drop unnecessary removal in install section.
- Use Rex's obsolete suggestion.

* Mon Oct 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.2-2
- Bump obsolete version.

* Tue Sep 27 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2.
- Update min versions of tp-glib and sofia-sip-glib.
- Rename package.
- Don't install the header files.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.
- Add BR to run tests.
- Drop local user patch. Fixed upstream.
- Bump minimum ver of tp-glib.

* Mon Jan 31 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-2
- Add patch to prevent crash when receiving a call from user's own URI.
- Remove buildroot and clean section. No longer needed.
- Update url and source url.

* Tue Nov 23 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0.

* Mon Sep  6 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4.

* Thu Jul  1 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3.

* Wed Mar 17 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2.

* Fri Feb 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1.

* Tue Feb 16 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0.

* Tue Dec  1 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.19-1
- Update to 0.5.19.

* Tue Nov  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.18.1-0.9.20091102git
- Grab git snapshot that fixes sip support to the Fedora asterisk server.

* Tue Sep 15 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.18-1
- Update to 0.5.18.

* Sun Aug  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.17-1
- Update to 0.5.17.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.15-1
- Update to 0.5.15.

* Tue Jan 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.5.14-1
- Update to 0.5.14.

* Fri Nov  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.11-1
- Update to 0.5.11.

* Wed Jul 16 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.10-1
- Update to 0.5.10.
- Bump min version of telepathy-glib needed.

* Sun Jun  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.5.8-1
- Initial Fedora spec.

