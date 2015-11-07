Name:		polkit-pkla-compat
Version:	0.1
Release:	8%{?dist}
Summary:	Rules for polkit to add compatibility with pklocalauthority
Summary(zh_CN.UTF-8): 与 pk 本地认证兼容的 polkit 规则
# GPLv2-licensed ltmain.sh and Apache-licensed mocklibc are not shipped in
# the binary package.
License:	LGPLv2+
URL:		https://fedorahosted.org/polkit-pkla-compat/
Source0:	https://fedorahosted.org/releases/p/o/polkit-pkla-compat/polkit-pkla-compat-%{version}.tar.xz

BuildRequires:	docbook-style-xsl, libxslt, glib2-devel, polkit-devel
# To ensure the polkitd group already exists when this is installed
Requires(pre): polkit

%global _hardened_build 1

%description
A polkit JavaScript rule and associated helpers that mostly provide
compatibility with the .pkla file format supported in polkit <= 0.105 for users
of later polkit releases.

%description -l zh_CN.UTF-8
与 pk 本地认证兼容的 polkit 规则。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
%make_install INSTALL='install -p'
magic_rpm_clean.sh

%check
make check

%files
%doc AUTHORS COPYING NEWS README
%dir %attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/localauthority
%dir %{_sysconfdir}/polkit-1/localauthority/*.d
%dir %{_sysconfdir}/polkit-1/localauthority.conf.d
%config(noreplace) %{_sysconfdir}/polkit-1/rules.d/49-polkit-pkla-compat.rules
%{_bindir}/pkla-admin-identities
%{_bindir}/pkla-check-authorization
%{_mandir}/man8/pkla-admin-identities.8*
%{_mandir}/man8/pkla-check-authorization.8*
%{_mandir}/man8/pklocalauthority.8*
%dir %attr(0750,root,polkitd) %{_localstatedir}/lib/polkit-1
%dir %{_localstatedir}/lib/polkit-1/localauthority
%dir %{_localstatedir}/lib/polkit-1/localauthority/*.d

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.1-8
- 为 Magic 3.0 重建

* Sat Jul 25 2015 Liu Di <liudidi@gmail.com> - 0.1-7
- 为 Magic 3.0 重建

* Tue Dec 23 2014 Liu Di <liudidi@gmail.com> - 0.1-6
- 为 Magic 3.0 重建

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Miloslav Trmač <mitr@redhat.com> - 0.1-2
- Add a comment above License about SRPM-only licenses
- Reword Summary: to avoid a rpmlint warning
- Move INSTALL= to the %%install section

* Tue May  7 2013 Miloslav Trmač <mitr@redhat.com> - 0.1-1
- Initial package

