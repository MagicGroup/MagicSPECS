Name:           dash
Version:        0.5.7
Release:        3%{?dist}
Summary:        Small and fast POSIX-compliant shell
Group:          System Environment/Shells
License:        BSD
URL:            http://gondor.apana.org.au/~herbert/dash/
Source0:        http://gondor.apana.org.au/~herbert/dash/files/dash-%{version}.tar.gz

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible. It does this without sacrificing speed where possible. In fact, it is
significantly faster than bash (the GNU Bourne-Again SHell) for most tasks.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%post
grep -qF '^/bin/dash$' /etc/shells || echo '/bin/dash' >> /etc/shells

%postun
if [ $1 -eq 0 ]; then
    sed -i '/^\/bin\/dash$/d' /etc/shells
fi

%files
%doc INSTALL COPYING ChangeLog
%{_bindir}/dash
%{_datadir}/man/man1/dash.1.gz

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.7-3
- 为 Magic 3.0 重建

* Fri Jul 27 2012 Liu Di <liudidi@gmail.com> - 0.5.7-2
- 为 Magic 3.0 重建

* Wed Aug 17 2011 Petr Sabata <contyk@redhat.com> - 0.5.7-1
- 0.5.7 bump

* Mon May 23 2011 Petr Sabata <psabata@redhat.com> - 0.5.6-5
- Try to add dash to /etc/shells every time, not just on new installs (#706138)
- Also, make the grep regexps a bit more strict, just to be sure

* Thu May 19 2011 Petr Sabata <psabata@redhat.com> - 0.5.6-4
- Install/remove dash from /etc/shells (#706138)
- Buildroot and defattr cleanup
- Add INSTALL, COPYING, ChangeLog to doc

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 21 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.5.6-2
- New upstream realease
- Version bump

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Andreas Thienemann <andreas@bawue.net> - 0.5.5.1-2
- Added patch from upstream git to not close stdout on err. This improves
  initramfs use of dash.

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 0.5.5.1-1
- 0.5.5.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Warren Togami <wtogami@redhat.com> 0.5.4-3
- rebuild for gcc-4.3

* Wed Nov 07 2007 Warren Togami <wtogami@redhat.com> 0.5.4-2
- move to /bin/dash
- BSD license tag

* Fri Nov 02 2007 Warren Togami <wtogami@redhat.com> 0.5.4-1
- initial package


