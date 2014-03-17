Name:           cups-pk-helper
Version:        0.2.5
Release:        2%{?dist}
Summary:        A helper that makes system-config-printer use PolicyKit

Group:          System Environment/Base
License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/cups-pk-helper/
Source0:        http://www.freedesktop.org/software/cups-pk-helper/releases/cups-pk-helper-%{version}.tar.xz

Patch0:         polkit_result.patch

BuildRequires:  libtool >= 1.4.3
BuildRequires:  cups-devel >= 1.2
BuildRequires:  python-devel >= 2.4
BuildRequires:  glib2-devel >= 2.29.8
BuildRequires:  gtk2-devel >= 2.12.0
BuildRequires:  dbus-glib-devel >= 0.74
BuildRequires:  polkit-devel >= 0.97
BuildRequires:  polkit-gnome >= 0.97
BuildRequires:  intltool >= 0.40.6
BuildRequires:  gettext-devel >= 0.17
BuildRequires:  gnome-common >= 2.26
BuildRequires:  autoconf automake libtool

Requires:       python >= 2.4
Requires:       cups-libs >= 1.2
Requires:       dbus >= 1.2
Requires:       dbus-glib >= 0.74
Requires:       glib2 >= 2.29.8


%description
cups-pk-helper is an application which makes cups configuration
interfaces available under control of PolicyKit.

%prep
%setup -q
%patch0 -p1 -b .polkit-result


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_libexecdir}/cups-pk-helper-mechanism
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.opensuse.CupsPkHelper.Mechanism.conf
%{_datadir}/dbus-1/system-services/org.opensuse.CupsPkHelper.Mechanism.service
%{_datadir}/polkit-1/actions/org.opensuse.cupspkhelper.mechanism.policy
%doc AUTHORS COPYING NEWS



%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Marek Kasik <mkasik@redhat.com> - 0.2.5-1
- Update to 0.2.5
- Change URL of cups-pk-helper project
- Use tarballs with configure
- Fix changelog's dates

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Marek Kasik <mkasik@redhat.com> - 0.2.4-1
- Update to 0.2.4
- Resolves CVE-2012-4510
- Revert stricter validation of printer names

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Marek Kasik <mkasik@redhat.com> - 0.2.2-1
- Update to 0.2.2
- Remove upstreamed patches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Marek Kasik <mkasik@redhat.com> - 0.2.1-2
- Fix configure.ac

* Tue Nov 22 2011 Marek Kasik <mkasik@redhat.com> - 0.2.1-1
- Update to 0.2.1
- Remove upstreamed patches
- Actualize Requires

* Thu Oct 27 2011 Marek Kasik <mkasik@redhat.com> - 0.1.3-3
- Set requesting-user-name for IPP_GET_JOB_ATTRIBUTES
- Resolves: #743886

* Fri Sep  2 2011 Marek Kasik <mkasik@redhat.com> - 0.1.3-2
- Make ppd-name parameter optional
- Readd patch for allowing authentication for any and inactive users
- Readd patch for check of result of polkit authorization check
- Resolves: #724959

* Fri Aug  5 2011 Marek Kasik <mkasik@redhat.com> - 0.1.3-1
- Update to 0.1.3
- Fix #724959

* Wed Mar 23 2011 Marek Kasik <mkasik@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Thu Mar 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.1.1-1
- Update to 0.1.1
- Drop accumulated upstreamed patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 22 2010 Marek Kasik <mkasik@redhat.com> - 0.0.4-13
- Add JobCancelPurge method
- Related: #548756

* Tue Feb 23 2010 Marek Kasik <mkasik@redhat.com> - 0.0.4-12
- Avoid timeout on job-related methods for invalid jobs
- Make sure to return an error via dbus in case of failure
- Remove a small leak
- Resolves: #548790

* Tue Feb 23 2010 Marek Kasik <mkasik@redhat.com> - 0.0.4-11
- Make cph_cups_job_get_status() efficient
- Resolves: #548771

* Tue Feb 23 2010 Marek Kasik <mkasik@redhat.com> - 0.0.4-10
- Fix adding of printers without specification of ppd-name.
- Patch by Tim Waugh.
- Resolves: #545452

* Tue Feb 23 2010 Marek Kasik <mkasik@redhat.com> - 0.0.4-9
- Allow inactive users and any user to authenticate
- Resolves: #543085

* Wed Sep 30 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-8
- Fix adding of printers without specification of device-uri.
- Patch by Tim Waugh.
- Resolves: #526442

* Tue Aug 18 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-7
- Fix policies to check when editing a job.

* Tue Aug 18 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-6
- Check result of polkit_authority_check_authorization_sync() for NULL.

* Thu Aug 13 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-5
- Add parameters to DevicesGet method.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-3
- Add devices_get() function.

* Thu Jun 18 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-2
- Update to polkit-1

* Tue Mar 31 2009 Marek Kasik <mkasik@redhat.com> - 0.0.4-1
- Update to 0.0.4

* Fri Feb 27 2009 Marek Kasik <mkasik@redhat.com> - 0.0.3-6
- Replace job-cancel, job-restart and job-set-hold-until with job-edit
- Replace job-cancel-another-owner, job-restart-another-owner
  and job-set-hold-until-another-owner with job-not-owned-edit
- Add cph_cups_job_get_status() function + some minor changes

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Marek Kasik <mkasik@redhat.com> 0.0.3-4
- Add ability to reconnect to CUPS server after its reload
  (caused by cupsAdminSetServerSettings() or cupsPutFile())

* Wed Jan 28 2009 Marek Kasik <mkasik@redhat.com> 0.0.3-3
- Add functions for handling jobs (JobRestart, JobCancel, JobSetHoldUntil)

* Mon Jan 26 2009 Marek Kasik <mkasik@redhat.com> 0.0.3-2
- Add handling of file:/ protocol
- Change order of checked policies so the PolicyKit asks only for
  "printer-enable" policy when enabling/disabling a printer
- Change order of checked policies so the PolicyKit asks only for
  "printer-set-default" policy when setting default printer

* Tue Jan 13 2009 Marek Kasik <mkasik@redhat.com> 0.0.3-1
- Initial spec file.
