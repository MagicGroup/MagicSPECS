Name:      hyphen
Summary:   A text hyphenation library
Summary(zh_CN.UTF-8): 文本断字库
Version:   2.8.8
Release:   4%{?dist}
Source:    http://downloads.sourceforge.net/hunspell/hyphen-%{version}.tar.gz
Group:     System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:       http://hunspell.sf.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:   GPLv2 or LGPLv2+ or MPLv1.1
BuildRequires: perl, patch, autoconf, automake, libtool
%ifarch %{ix86} x86_64
BuildRequires: valgrind
%endif

%description
Hyphen is a library for high quality hyphenation and justification.

%description -l zh_CN.UTF-8
文本断字库。

%package devel
Requires: hyphen = %{version}-%{release}
Summary: Files for developing with hyphen
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
Includes and definitions for developing with hyphen

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package en
Requires: hyphen
Summary: English hyphenation rules
Summary(zh_CN.UTF-8): 英语的断字规则
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
BuildArch: noarch

%description en
English hyphenation rules.

%description en -l zh_CN.UTF-8
英语的断字规则。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%check
#%ifarch %{ix86} x86_64, see rhbz#813780
%ifarch %{ix86}
VALGRIND=memcheck make check
%else
make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
en_US_aliases="en_AG en_AU en_BS en_BW en_BZ en_CA en_DK en_GB en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NZ en_PH en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_US_aliases; do
        ln -s hyph_en_US.dic hyph_$lang.dic
done
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README README.hyphen README.nonstandard TODO
%{_libdir}/*.so.*
%dir %{_datadir}/hyphen

%files en
%defattr(-,root,root,-)
%{_datadir}/hyphen/hyph_en*.dic

%files devel
%defattr(-,root,root,-)
%{_includedir}/hyphen.h
%{_libdir}/*.so
%{_bindir}/substrings.pl

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.8.8-4
- 为 Magic 3.0 重建

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 2.8.8-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 18 2014 Caolán McNamara <caolanm@redhat.com> - 2.8.8-1
- latest version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 David Tardon <dtardon@redhat.com> - 2.8.7-2
- fix hyphen.h

* Fri Jun 27 2014 Caolán McNamara <caolanm@redhat.com> - 2.8.7-1
- latest version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> - 2.8.6-3
- Resolves: rhbz#925563 support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.6-1
- latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.5-1
- latest version

* Fri Jun 29 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.4-1
- latest version

* Wed Apr 18 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.3-4
- Resolves: rhbz#813481 x86_64 valgrind spews, see rhbz#813780
- Related: rhbz#813481 dump valgrind failure log

* Thu Apr 12 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.3-3
- add Malawian alias
- add Zambian alias

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Caolán McNamara <caolanm@redhat.com> - 2.8.3-1
- latest version

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 2.8-1
- latest version

* Fri Jun 24 2011 Caolán McNamara <caolanm@redhat.com> - 2.7-3
- Resolves: rhbz#715995 FTBFS

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Caolán McNamara <caolanm@redhat.com> - 2.7-1
- latest version

* Mon Jul 19 2010 Caolán McNamara <caolanm@redhat.com> - 2.6-1
- latest version
- run make check

* Thu Feb 25 2010 Caolán McNamara <caolanm@redhat.com> - 2.5-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Caolán McNamara <caolanm@redhat.com> - 2.4-4
- make hyphen-en a noarch subpackage

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 2.4-3
- extend coverage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 02 2008 Caolán McNamara <caolanm@redhat.com> - 2.4-1
- latest version

* Tue Feb 19 2008 Caolán McNamara <caolanm@redhat.com> - 2.3.1-1
- latest version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3-2
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Caolán McNamara <caolanm@redhat.com> - 2.3-1
- initial version
