# Supported build option:
#
# --with nls ... build this package with --enable-nls 

Name:           help2man
Summary:        Create simple man pages from --help output
Summary(zh_CN.UTF-8): 从 --help 的输出中生成简单的手册页 (man)
Version: 1.47.2
Release:        3%{?dist}
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv3+
URL:            http://www.gnu.org/software/help2man
Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz

%bcond_with nls

%{!?with_nls:BuildArch: noarch}
%{?with_nls:BuildRequires: perl(Locale::gettext)}
%{?with_nls:Requires: perl(Locale::gettext)}

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%description -l zh_CN.UTF-8
从 --help 的输出中生成简单的手册页 (man)。

%prep
%setup -q -n help2man-%{version}

%build
%configure --%{!?with_nls:disable}%{?with_nls:enable}-nls --libdir=%{_libdir}/help2man
make %{?_smp_mflags}

%install
make install_l10n DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %name --with-man || touch %name.lang

%post
/usr/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/help2man.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files -f %name.lang
%defattr(-, root, root,-)
%doc README NEWS THANKS COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%if %{with nls}
%{_libdir}/help2man
%endif

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.47.2-3
- 更新到 1.47.2

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.45.1-2
- 更新到 1.45.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.40.10-2
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.10-1
- Upstream update.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.8-1
- Upstream update.

* Sat Feb 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.6-1
- Upstream update.

* Thu Jan 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.5-1
- Upstream update.

* Thu Dec 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.4-1
- Upstream update.

* Wed Jun 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.2-1
- Upstream update.

* Fri Apr 22 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.39.2-1
- Upstream update.
- Spec modernization.
- Abandon patches (unnecessary).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 27 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.38.2-1
- Upstream update.
- Add *-locales.diff, *-mans.diff.
- Use %%find_lang --with-man.
- Use %%bcond_with nls.

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 1.36.4-6
- do ship COPYING file in %%doc

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.36.4-4
- Apply patch from http://bugs.gentoo.org/show_bug.cgi?id=237378#c6
  to address BZ #494089.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-2
- Update license tag.
- Convert THANKS to utf-8.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-1
- Upstream update.
- utf-8 encode l10n'd man pages.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.36.3-1
- Upstream update.
- Add build option --with nls.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.35.1-2
- Fix disttag (#176473).
- Cleanup spec.

* Fri Apr 29 2005 Ralf Corsepius <ralf[AT]links2linux.de> - 1.35.1-1
- Update to 1.35.1
- Minor spec fixes.
