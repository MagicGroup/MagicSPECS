%{!?python:%define python python}

Name:           %{python}-twisted
Version:        12.2.0
Release:        2%{?dist}
Summary:        Event-based framework for internet applications
License:        MIT
URL:            http://twistedmatrix.com/
Source0:        README.fedora
#Obtained by running python setup.py egg_info in the unitary tarball
Source1:        PKG-INFO
BuildArch:      noarch
BuildRequires:  python
Requires:       python
Requires:       %{python}-twisted-core   >= %{version}
Requires:       %{python}-twisted-conch  >= %{version}
Requires:       %{python}-twisted-lore   >= %{version}
Requires:       %{python}-twisted-mail   >= %{version}
Requires:       %{python}-twisted-names  >= %{version}
Requires:       %{python}-twisted-news   >= %{version}
Requires:       %{python}-twisted-runner >= %{version}
Requires:       %{python}-twisted-web    >= %{version}
Requires:       %{python}-twisted-words  >= %{version}
Obsoletes:      Twisted < 2.4.0-1
Provides:       Twisted = %{version}-%{release}
Obsoletes:      twisted < 2.4.0-1
Provides:       twisted = %{version}-%{release}

%description
Twisted is an event-based framework for internet applications.  It includes a
web server, a telnet server, a chat server, a news server, a generic client
and server for remote object access, and APIs for creating new protocols and
services. Twisted supports integration of the Tk, GTK+, Qt or wxPython event
loop with its main event loop. The Win32 event loop is also supported, as is
basic support for running servers on top of Jython.

Installing this package brings all Twisted sub-packages into your system.

%prep
%setup -c -T
install -p -m 0644 %{SOURCE0} README


%install
install -d $RPM_BUILD_ROOT%{python_sitelib}
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{python_sitelib}/Twisted-%{version}-py2.7.egg-info
magic_rpm_clean.sh

%files
%doc README
%{python_sitelib}/Twisted-%{version}-py2.7.egg-info


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 12.2.0-2
- 为 Magic 3.0 重建

* Mon Sep 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.2.0-1
- Updated to 12.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.1.0-1
- Updated to 12.1.0

* Sun Feb 12 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.0.0-1
- Updated to 12.0.0

* Sat Jan 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-2
- Rebuilt for gcc-4.7

* Fri Nov 18 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-1
- Updated to 11.1.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sat Apr 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.0.0-1
- Updated to 11.0.0
- Added comment on how to obtain the PKG-INFO file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 10.2.0-1
- Updated to 10.2.0

* Mon Nov 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-3
- Use python_sitelib instead of python-sitearch
- The aforementioned macros are defined in Fedora 13 and above

* Sun Nov 07 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-2
- Added egg-info file

* Tue Sep 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-1
- Updated to 10.1.0
- Switched to macros for versioned dependencies

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Wed Jul 16 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Minor spec file cleanups.
- Merge back changes from Paul Howarth.

* Wed May 21 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.5.0-1
- update to 2.5.0 release (only the umbrella package was missing)

* Tue Jan 16 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-3
- list packages in README.fedora

* Wed Jan 03 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-2
- add a README.fedora
- made noarch, since it doesn't actually install any python twisted/ module
  code
- fixed provides/obsoletes

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.4.0-1
- this is now a pure umbrella package

* Mon Oct 10 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.1.0-1
- upstream release

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.1-1
- upstream release

* Mon Apr 04 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-2
- add zsh support

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-1
- final release

* Thu Mar 17 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.2.a3
- dropped web2

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0-0.1.a2
- new prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 2.0.0a1-1
- prep for split

* Fri Aug 20 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.3.0-1
- new version

* Mon Apr 19 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-3
- vaultize

* Mon Apr 12 2004 Jeff Pitman <symbiont+pyvault@berlios.de> 1.2.0-2
- require pyOpenSSL, SOAPpy, openssh-clients, crypto, dia so trial can run

