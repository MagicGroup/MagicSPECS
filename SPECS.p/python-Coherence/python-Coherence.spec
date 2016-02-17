%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: Python framework to participate in digital living networks
Name: python-Coherence
Version: 0.6.6.2
Release: 7%{?dist}
License: MIT
Group: Development/Languages
URL: http://coherence.beebits.net/
Source: http://coherence.beebits.net/download/Coherence-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python-setuptools
# As of 0.5.8, only "ConfigObj >= 4.3" in the requires.txt egg file
# As of 0.6.2, "Twisted >= 2.5.0" is there too, and "web" is req for sure
# As of 0.6.6, now required at build time too
Requires: python-twisted-core >= 2.5
Requires: python-twisted-web >= 2.5
Requires: python-louie
Requires: python-configobj
# Needed for the parent directory
Requires: dbus
BuildRequires: python-devel
BuildRequires: python-twisted-core >= 2.5
BuildRequires: python-twisted-web >= 2.5
# Must have setuptools to build the package
BuildRequires: python-setuptools
Buildarch: noarch
# Fist test packages had different names
Obsoletes: coherence < 0.2.1-2
Obsoletes: Coherence < 0.2.1-3

%description
Coherence is a framework written in Python enabling applications to participate
in digital living networks, such as the UPnP universe.


%prep
%setup -q -n Coherence-%{version}
# As of 0.5.8, louie is bundled but we prefer the external package since we
# have it easily available
find coherence -type f -exec \
    sed -i 's/coherence.extern.louie as louie/louie/' {} \;
%{__rm} -rf coherence/extern/louie/


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install \
    --single-version-externally-managed \
    -O1 --skip-build --root %{buildroot}
# Install the D-Bus service file
%{__install} -D -m 0644 -p misc/org.Coherence.service \
    %{buildroot}/%{_datadir}/dbus-1/services/org.Coherence.service
# Install the man page
%{__install} -D -m 0644 -p docs/man/coherence.1 \
    %{buildroot}/%{_mandir}/man1/coherence.1


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENCE README docs/*.*
%exclude %{_bindir}/applet-coherence
%{_bindir}/coherence
%{_datadir}/dbus-1/services/org.Coherence.service
%{python_sitelib}/Coherence-*.egg-info/
%{python_sitelib}/coherence/
# We don't want this in the package
%exclude %{python_sitelib}/misc/
%{_mandir}/man1/coherence.1*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.6.6.2-7
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.6.6.2-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.6.6.2-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 28 2010 Matthias Saou <http://freshrpms.net/> 0.6.6.2-1
- Update to 0.6.6.2.
- The website no longer forces https, change spec URLs back to plain http.
- Install the man page instead of having it in %%doc (#546827).

* Tue Sep 08 2009 Bastien Nocera <bnocera@redhat.com> 0.6.4-1
- Update to 0.6.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr  5 2009 Matthias Saou <http://freshrpms.net/> 0.6.2-2
- Re-add re-needed re-python-twisted re-quirements (#485093).
- Require dbus for proper parent directory ownership.

* Tue Feb 24 2009 - Bastien Nocera <bnocera@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Jan 20 2009 - Bastien Nocera <bnocera@redhat.com> 0.6.0-2
- Install the D-Bus service file so that the Totem plugin can work

* Fri Jan  2 2009 Matthias Saou <http://freshrpms.net/> 0.6.0-1
- Update to 0.6.0.
- Remove bundled internal louie and require external + trivial sed to use it.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.8-2
- Rebuild for Python 2.6

* Tue Jul 15 2008 Matthias Saou <http://freshrpms.net/> 0.5.8-1
- Update to 0.5.8.
- Don't include new "misc" directory, as its location is ugly!
- Don't include applet-coherence as it probably requires the "misc" directory.
- Remove all reqs but python-configobj, as it seems to be the only one left.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 0.5.0-1
- Update to 0.5.0.

* Wed Aug 29 2007 Matthias Saou <http://freshrpms.net/> 0.4.0-2
- Update python-setuptools build requirement to new python-setuptools-devel.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 0.4.0-1
- Update to 0.4.0.
- No need to update License field, MIT is already correct.

* Tue Jul 24 2007 Matthias Saou <http://freshrpms.net/> 0.3.0-1
- Update to 0.3.0.

* Tue May  8 2007 Matthias Saou <http://freshrpms.net/> 0.2.1-3
- Rename Coherence -> python-Coherence to match our python naming guidelines.

* Mon May  7 2007 Matthias Saou <http://freshrpms.net/> 0.2.1-2
- Rename coherence -> Coherence to match upstream and our naming guidelines.
- Obsolete coherence < 0.2.1-2 but don't provide it since elisa's requirement
  has been updated to match the name change and nothing else requires it.

* Fri Apr 20 2007 Matthias Saou <http://freshrpms.net/> 0.2.1-1
- Update to 0.2.1.

* Fri Mar 23 2007 Matthias Saou <http://freshrpms.net/> 0.1.0-1
- Update to 0.1.0 release.

* Wed Feb 14 2007 Matthias Saou <http://freshrpms.net/> 0.0-1.r303
- Switch to using the go-4-python-2.5 svn branch.

* Fri Feb  9 2007 Matthias Saou <http://freshrpms.net/> 0-0.1.r294
- Initial RPM release.

