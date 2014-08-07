%global systemctl_bin /usr/bin/systemctl

Name: numad
Version: 0.5
Release: 18.20140620git%{?dist}
Summary: NUMA user daemon

License: LGPLv2
Group: System Environment/Daemons
URL: http://git.fedorahosted.org/git/?p=numad.git
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   git clone git://git.fedorahosted.org/numad.git numad-0.5git
#   tar --exclude-vcs -cJf numad-0.5git.tar.xz numad-0.5git/
Source0: %{name}-%{version}git.tar.xz
Patch1: 0001-Fix-build-with-Werror-format-security.patch

Requires: systemd-units, initscripts
Requires(post): systemd-units, initscripts
Requires(preun): systemd-units, initscripts
BuildRequires: systemd-units

ExcludeArch: s390 s390x %{arm}

%description
Numad, a daemon for NUMA (Non-Uniform Memory Architecture) systems,
that monitors NUMA characteristics and manages placement of processes
and memory to minimize memory latency and thus provide optimum performance.

%prep
%setup -q -n %{name}-%{version}git
%patch1 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -std=gnu99" LDFLAGS="$RPM_LD_FLAGS -lpthread -lrt -lm"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/man8/
install -p -m 644 numad.service %{buildroot}%{_unitdir}/
install -p -m 644 numad.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
make install prefix=%{buildroot}/usr

%files
%{_bindir}/numad
%{_unitdir}/numad.service
%config(noreplace) %{_sysconfdir}/logrotate.d/numad
%doc %{_mandir}/man8/numad.8.gz

%post
%systemd_post numad.service

%preun
%systemd_preun numad.service

%postun
%systemd_postun numad.service

%changelog
* Thu Aug 07 2014 Liu Di <liudidi@gmail.com> - 0.5-18.20140620git
- 为 Magic 3.0 重建

* Mon Jun 23 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-17.20140620git
- Update to 20140620

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-16.20140225git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-15.20140225git
- Update to the correct upstream version of 20140225

* Fri Feb 28 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-14.20140225git
- Update to 20140225
- Resolves: #1071221

* Mon Jan 20 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.5-13.20130814git
- Don't order service after syslog.target (#1055209).
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.
- Fix build with -Werror=format-security.

* Wed Aug 14 2013 Jan Synáček <jsynacek@redhat.com> - 0.5-12.20130814git
- Update to 20130814

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11.20121130git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-10.20121130git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-9.20121130git
- Update and comment the Makefile patch
- Related: #825153

* Mon Dec 03 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-8.20121130git
- Update to 20121130
- Update spec: fix command to generate tarball

* Tue Oct 16 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-7.20121015git
- Update to 20121015
- Add Makefile patch
- Update spec: update command to generate tarball

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-6.20120522git
- add systemd-rpm macros
- Resolves: #850236

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5.20120522git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-4.20120522git
- update source (20120522) and manpage

* Tue Mar 06 2012 Jan Synáček <jsynacek@redhat.com> 0.5-3.20120221git
- update source
- drop the patch

* Fri Feb 24 2012 Jan Synáček <jsynacek@redhat.com> 0.5-2.20120221git
- add BuildRequires: systemd-units

* Wed Feb 15 2012 Jan Synáček <jsynacek@redhat.com> 0.5-1.20120221git
- spec update

* Fri Feb 10 2012 Bill Burns <bburns@redhat.com> 0.5-1
- initial version
