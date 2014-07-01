# we don't want to either provide or require anything from _docdir, per policy
# https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
%{?filter_setup:
%filter_provides_in %{_docdir}
%filter_requires_in %{_docdir}
%filter_setup
}

Name:           debhelper
Version:	9.20140613
Release:        1%{?dist}
Summary:        Helper programs for Debian rules
Summary(zh_CN.UTF-8): Debian 打包用的辅助程序

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv2+
URL:            http://kitenet.net/~joey/code/debhelper/
Source0:        http://ftp.de.debian.org/debian/pool/main/d/%{name}/%{name}_%{version}.tar.gz
Patch0:         debhelper-7.4.20-no-utf8-to-pod2man.patch
BuildArch:      noarch

BuildRequires:  po4a
BuildRequires:  man-db
BuildRequires:  dpkg-dev
# For 'make test'
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)

Requires:       binutils
Requires:       dpkg-perl
Requires:       html2text
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       po-debconf

%description
A collection of programs that can be used in a Debian rules file
to automate common tasks related to building Debian packages.
Programs are included to install various files into your package,
compress files, fix file permissions, integrate your package with
the Debian menu system, debconf, doc-base, etc. Most Debian
packages use debhelper as part of their build process.

%description -l zh_CN.UTF-8
Debian 自动打包用的 rule 文件相关的一些程序集合。

%prep
%setup -q -n %{name}
%patch0 -p1 -b .no-utf8-to-pod2man

%build
make %{?_smp_mflags} build

%install
%make_install

# Use debhelper to install (man-pages of) debhelper...

./run dh_installman -P %{buildroot}

# Add man-pages to a .lang file:
# We cannot use "find_lang --with-man" because it only handle
# single man-page -- we have many
magic_rpm_clean.sh
rm -f debhelper-mans.lang
for lang in de es fr; do
    for level in 1 7; do
        # Append to .lang file
        # Replace buildroot with the lang prefix, append '*' (for gzip, etc.)
        find %{buildroot}%{_mandir}/$lang/man$level -type f -o -type l | sed "
                s:^%{buildroot}:%%lang($lang) :
                s:\$:*:
                " >> debhelper-mans.lang
    done
done


%check
make test


%files -f debhelper-mans.lang
%doc examples/ doc/
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_bindir}/dh*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/autoscripts
%dir %{perl_vendorlib}/Debian
%{perl_vendorlib}/Debian/Debhelper

%changelog
* Thu Jun 26 2014 Liu Di <liudidi@gmail.com> - 9.20140613-1
- 更新到 9.20140613

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 9.20140228-1
- 更新到 9.20140228

* Mon Feb 10 2014 Sérgio Basto <sergio@serjux.com> - 9.20131227-1
- Update to 9.20131227, most of the work by Sandro Mani <manisandro@gmail.com>
- Drop debhelper-find-perm.patch, fixed upstream.
- Drop debhelper-fr.po.patch, fixed upstream.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20120909-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 9.20120909-2
- Perl 5.18 rebuild

* Fri May 10 2013 Oron Peled <oron@actcom.co.il> - 9.20120909-1
- Update to latest Debian/wheezy version
- Fix find_lang for man-pages
- Added 'de' to language list

* Thu Mar 29 2012 Oron Peled <oron@actcom.co.il> - 9.20120322-3
- Fix testing BR -- perl(Test::...)
- Now make test works as intended

* Wed Mar 28 2012 Oron Peled <oron@actcom.co.il> - 9.20120322-2
- Avoid auto-requires under _docdir
- Prepare for make test (but don't fail yet, as we miss perl-Test-More)

* Mon Mar 26 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 9.20120322
- New version

* Wed Sep 29 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 7.4.20-4
- Fix locale

* Fri Aug 13 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 7.4.20-3
- Fix description

* Thu May 13 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 7.4.20-2
- Include es/fr man pages
- Update to newer version from Debian Sid
- Fix package requirements

* Tue May 11 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 7.0.15-1
- First package
