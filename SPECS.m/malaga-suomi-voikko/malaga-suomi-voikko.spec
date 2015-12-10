Name:           malaga-suomi-voikko
Version: 1.19
Release: 3%{?dist}
Summary:        A description of Finnish morphology written in Malaga (Voikko edition)
Summary(zh_CN.UTF-8): 用 Malaga 编写的芬兰语形态描述

Group:          Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
License:        GPLv2+
URL:            http://voikko.sourceforge.net/
# The usual format of stable release source URLs
Source0:        http://www.puimula.org/voikko-sources/suomi-malaga/suomi-malaga-%{version}.tar.gz
# The usual format of testing release source URLs
#Source0:        http://www.puimula.org/htp/testing/suomi-malaga-%{version}rc3.tar.gz

BuildRequires:  malaga >= 7.8 python

# debuginfo would be empty
%define debug_package %{nil}

%description
A description of Finnish morphology written in Malaga. This package is built
to support the Voikko spellchecker/hyphenator, it doesn't support the Sukija
text indexer.

%description -l zh_CN.UTF-8
用 Malaga 编写的芬兰语形态描述。

%prep
%setup -q -n suomi-malaga-%{version}


%build
# configure removed, not needed in this package
make %{?_smp_mflags} voikko


%install
rm -rf $RPM_BUILD_ROOT
# Files differ on big-endian and small-endian archs, and they have different
# names (*_l vs *_b). This is the reason we use %%{_libdir} instead of
# %%{_datadir} and won't noarch the package.
make voikko-install DESTDIR=$RPM_BUILD_ROOT%{_libdir}/voikko
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc ChangeLog CONTRIBUTORS COPYING README README.fi
%{_libdir}/voikko


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.19-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.19-2
- 更新到 1.19

* Sat Aug 09 2014 Liu Di <liudidi@gmail.com> - 1.16-1
- 更新到 1.16

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.10-2
- 为 Magic 3.0 重建

* Fri Sep 16 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 1.10-1
- Suomi-malaga 1.10

* Sat Apr 23 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.9-1
- Suomi-malaga 1.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.8-1
- Suomi-malaga 1.8

* Thu Sep 16 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-1
- Suomi-malaga 1.7
- Remove the %%clean section of the spec file, not needed in Fedora >= 13

* Tue May 18 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.6-1
- RC3 released as stable, bump release to preserve upgrade path

* Thu May 13 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.6-0.1.rc3
- New upstream release candidate
- Remove unneeded BuildRoot tag

* Wed Jan 27 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.5-1
- Suomi-malaga 1.5

* Fri Oct 09 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.4-1
- RC3 released as stable.

* Mon Sep 28 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.4-0.3.rc3
- New release candidate.

* Fri Sep 18 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.4-0.2.rc2
- New release candidate.

* Tue Sep 15 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.4-0.1.rc1
- New release candidate.
- Don't require libmalaga anymore, libvoikko >= 2.2 uses its own malaga
  implementation for Finnish spell checking. Malaga is still required for
  building this package.
- Cleanup DESTDIR, Makefile now automatically adds the directory version
  and variant to it.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 06 2009 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.3-10
- Install data files into the new location expected by libvoikko 2.1
- Bump Release to 10 to differentiate this from earlier packages,
  this release or higher needs to be required by the libvoikko 2.1 package

* Thu Mar 05 2009 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.3-1
- Suomi-malaga 1.3

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 02 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.2-1
- Suomi-malaga 1.2
  - RC1 released as stable

* Wed Oct 01 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.2-0.1.rc1
- New release candidate

* Mon Apr 28 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.1-1
- Suomi-malaga 1.1

* Thu Jan 10 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.0-1
- Suomi-malaga 1.0
- Requires: libmalaga, not malaga. The malaga binaries are not needed for
  Finnish spellchecking, only the library is.
- Changed description a bit

* Thu Dec 4 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 0.7.7-1
- Suomi-malaga 0.7.7

* Mon Dec 03 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 0.7.7-0.1.rc1
- New release candidate

* Thu Nov 1 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 0.7.6-1
- Require malaga >= 7.8 as per the latest Voikko release notes
  (http://voikko.sourceforge.net/releases.html)
- Bump release for the initial Fedora build

* Tue Oct 23 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 0.7.6-0.2
- Remove duplicate files entries
- Remove (Build)Requires libmalaga

* Tue Oct 23 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 0.7.6-0.1
- Initial package
