# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           fedpkg
Version:        1.15
Release:        2%{?dist}
Summary:        Fedora utility for working with dist-git
Summary(zh_CN.UTF-8): Fedora 的发行版 git 工具

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        GPLv2+
URL:            http://fedorahosted.org/fedpkg
Source0:        http://fedorahosted.org/releases/f/e/fedpkg/fedpkg-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       pyrpkg >= 1.13, magic-rpm-config
Requires:       python-pycurl, koji, python-fedora
Requires:       fedora-cert, python-offtrac, bodhi-client
%if 0%{?rhel} == 5 || 0%{?rhel} == 4
Requires:       python-kitchen
%endif

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools, python-offtrac
# We br these things for man page generation due to imports
BuildRequires:  pyrpkg, fedora-cert
# This until fedora-cert gets fixed
BuildRequires:  python-fedora


%description
Provides the fedpkg command for working with dist-git


%prep
%setup -q

%build
%{__python} setup.py build
%{__python} src/fedpkg_man_page.py > fedpkg.1


%install
#rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__install} -p -m 0644 fedpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1
rename es.py es $RPM_BUILD_ROOT%{_libexecdir}/fedpkg-fixbranches.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%config(noreplace) %{_sysconfdir}/rpkg
%{_sysconfdir}/bash_completion.d
%{_bindir}/%{name}
%{_mandir}/*/*
%{_libexecdir}/fedpkg-fixbranches
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 <dennis@ausil.us> - 1.15-1
- remove tag-request we no longer use that work flow, the process is managed
  via blocker bugs now (dennis)
- use the rpm changelog as default update template patch from
  https://bugzilla.redhat.com/show_bug.cgi?id=1023915 (dennis)
- allow epel branches to be epel<release> clean up overrides (dennis)
- Fix log message (bochecha)

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> - 1.14-1
- clean up arches in fedpkg bash completeion - drop sparc - add i686 - add arm
  variants - add ppc64p7 (dennis)
- Add arm7hl to bash completion arches (opensource)
- Add more ppc64-only packages (opensource)
- remove --push from retire command in bash completion (opensource)
- undefine macros rather than define as nil (dennis)

* Sat Aug 24 2013 Dennis Gilmore <dennis@ausil.us> - 1.13-1
- Rework --retire (opensource)

* Sat Aug 24 2013 Dennis Gilmore <dennis@ausil.us> - 1.12-1
- update ppc secondary arch packages, remove sparc, point to new seconary arch
  config location (dennis)
- retire packages in packagedb as well (opensource)
- Move fedpkg to own module (opensource)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  6 2013 Tom Callaway <spot@fedoraproject.org> - 1.11-2
- use --eval '%%undefine to unset dist values instead of nil (bz876308)

* Tue Nov 06 2012 Jesse Keating <jkeating@redhat.com> - 1.11-1
- Unset runtime disttag (spot)
- use nil to unset dist values. (spot)

* Tue Oct 09 2012 Jesse Keating <jkeating@redhat.com> - 1.10-1
- Force invalid dist values to 0 (spot) (jkeating)
- Fix a traceback in fixbranches (#817478) (jkeating)

* Mon Mar 12 2012 Jesse Keating <jkeating@redhat.com> - 1.9-1
- Wrap the prune command in a try (rhbz#785820) (jkeating)
- Use koji if we have it to get master details (rhbz#785234) (jkeating)
- Always send builds from master to 'rawhide' (rhbz#785234) (jkeating)
- Handle fedpkg calls not from a git repo (rhbz#785776) (jkeating)

* Thu Mar 01 2012 Jesse Keating <jkeating@redhat.com> - 1.8-1
- More completion fixes (jkeating)
- Add mock-config and mockbuild completion (jkeating)
- Simplify test for fedpkg availability. (ville.skytta)
- Fix ~/... path completion. (ville.skytta)
- Add --raw to bash completion (jkeating)
- Make things quiet when possible (jkeating)
- Fix property variables (jkeating)

* Sat Jan 14 2012 Jesse Keating <jkeating@redhat.com> - 1.7-1
- Adapt property overloading to new-style class. (bochecha)
- Use super(), now that rpkg uses new-style classes everywhere (bochecha)
- Add gitbuildurl to the bash completion. (jkeating)
- Handle koji config with unknown module name (jkeating)

* Mon Nov 21 2011 Jesse Keating <jkeating@redhat.com> - 1.6-1
- Replace -c with -C for the --config option (jkeating)
- Package up fedpkg-fixbranches (#751507) (jkeating)
- Use old style of super class calls (jkeating)

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 1.5-1
- Pass along the return value from import_srpm (jkeating)
- Whitespace cleanup (jkeating)

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 1.4-1
- Use the GPLv2 content for COPYING to match intent. (jkeating)

* Thu Nov 03 2011 Jesse Keating <jkeating@redhat.com> - 1.3-1
- Fix buildrequires (jkeating)
- Don't register a nonexestant target (jkeating)
- Drop koji-rhel.conf file (jkeating)
- Fix up the setup.py (jkeating)

* Thu Nov 03 2011 Jesse Keating <jkeating@redhat.com> - 1.2-1
- Catch raises in the libraries (jkeating)
- Fix the fixbranches script for new module name (jkeating)
- srpm takes arguments, pass them along (jkeating)
- Get error output from user detection failures (jkeating)
- Get the user name from the Fedora SSL certificate. (bochecha)
- Fix crash when detecting Rawhide. (bochecha)

* Fri Oct 28 2011 Jesse Keating <jkeating@redhat.com> - 1.1-1
- Overload curl stuff (jkeating)
- Hardcode fedpkg version requires (jkeating)
- Fix up changelog date (jkeating)
