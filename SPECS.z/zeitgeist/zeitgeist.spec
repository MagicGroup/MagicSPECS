Summary:	Framework providing Desktop activity awareness
Name:		zeitgeist
Version:	0.9.14
Release:	4%{?dist}

# most of the source code is LGPLv2+, except:
# datahub/ is LGPLv3+
# examples/c/ is GPLv3
# extensions/fts++/ is GPLv2+
# src/notify.vala: GPLv2+
# test/c/ is GPLv3
# tools/zeitgeist-explorer/ is GPLv2+
License:	LGPLv2+ and LGPLv3+ and GPLv2+
URL:		https://launchpad.net/zeitgeist
Source0:	http://launchpad.net/%{name}/0.9/%{version}/+download/%{name}-%{version}.tar.xz
Patch0:		zeitgeist-fix-giodeps.patch

BuildRequires:	dbus-devel
BuildRequires:	gettext
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk3-devel
BuildRequires:	intltool
BuildRequires:	json-glib-devel
BuildRequires:	python-devel
BuildRequires:	python-rdflib
BuildRequires:	raptor2
BuildRequires:	sqlite-devel
BuildRequires:	telepathy-glib-devel
BuildRequires:	vala
BuildRequires:	xapian-core-devel
Requires:	dbus
Requires:	dbus-python

Obsoletes:	zeitgeist-datahub < 0.9.10

%description
Zeitgeist is a service which logs the users's activities and events (files
opened, websites visites, conversations hold with other people, etc.) and makes
relevant information available to other applications. 

Note that this package only contains the daemon, which you can use
together with several different user interfaces.


%package	libs
Summary:	Client library for interacting with the Zeitgeist daemon
License:	LGPLv2+

%description	libs
Libzeitgeist is a client library for interacting with the Zeitgeist
daemon.


%package	devel
Summary:	Development files for %{name}
License:	LGPLv2+
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

## nuke unwanted rpaths, see also
## https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
%configure --enable-fts --enable-datahub     
make %{?_smp_mflags} 

%install
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.la

# We install AUTHORS and NEWS with %%doc instead
rm -rf %{buildroot}%{_datadir}/zeitgeist/doc

#%find_lang %{name}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS COPYING COPYING.GPL NEWS
%{_bindir}/zeitgeist-daemon
%{_bindir}/zeitgeist-datahub
%{_libexecdir}/zeitgeist-fts
%{_datadir}/%{name}/
%{python_sitelib}/zeitgeist/
%{_datadir}/dbus-1/services/org.gnome.zeitgeist*.service
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/zeitgeist-daemon
%{_mandir}/man1/zeitgeist-*.*
%{_sysconfdir}/xdg/autostart/zeitgeist-datahub.desktop

%files libs
%doc COPYING
%{_libdir}/girepository-1.0/Zeitgeist-2.0.typelib
%{_libdir}/libzeitgeist-2.0.so.*

%files devel
%{_includedir}/zeitgeist-2.0/
%{_libdir}/libzeitgeist-2.0.so
%{_libdir}/pkgconfig/zeitgeist-2.0.pc
%{_datadir}/gir-1.0/Zeitgeist-2.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/zeitgeist-2.0.deps
%{_datadir}/vala/vapi/zeitgeist-2.0.vapi
%{_datadir}/vala/vapi/zeitgeist-datamodel-2.0.vapi

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.9.14-4
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.9.14-3
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  9 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14.

* Sun Jun 16 2013 Kalev Lember <kalevlember@gmail.com> - 0.9.13-2
- Fix postun script syntax error

* Fri Jun 14 2013 Deji Akingunola <dakingun@gmail.com> - 0.9.13-1
- Update to 0.9.13

* Sun Apr 14 2013 Kalev Lember <kalevlember@gmail.com> - 0.9.12-1
- Update to 0.9.12 (#949286)
- Obsolete zeitgeist-datahub
- Package up the libzeitgeist-2.0 library
- Update the license tag and add a spec file comment with longer explanations

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 23 2012 Deji Akingunola <dakingun@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Deji Akingunola <dakingun@gmail.com> - 0.9.0-1
- Update to 0.9.0
- Apply upstream patch to fix a crasher bug.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.2-2
- Revert post-install script to restart zeitgeist daemon on update

* Tue Oct 18 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.2-1
- Update to 0.8.2
- Restart the zeitgeist daemon on update (BZ #627982)

* Wed Jul 20 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Fri May 13 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.0-1
- Update to 0.8.0
- Add a hard requires on zeitgeist-datahub

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Deji Akingunola <dakingun@gmail.com> - 0.7-1
- Update to 0.7

* Fri Aug 06 2010 Deji Akingunola <dakingun@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Deji Akingunola <dakingun@gmail.com> - 0.4.0-1
- Update to 0.4.0

* Wed Apr 21 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.3.1-1
- Update to 0.3.3.1 to fix datasource_registry bug (BZ #586238)

* Wed Apr 21 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.3-1
- Update to 0.3.3

* Wed Jan 20 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.2-1
- Update to 0.3.2

* Thu Jan 14 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.1-1
- Add missing requires (Package reviews)
- Update license tag (Package reviews)
- Update to latest release

* Tue Dec 01 2009 Deji Akingunola <dakingun@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Wed Nov 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.2.1-1
- Initial Fedora packaging
