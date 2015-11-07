#%%global _internal_version  c147867

Name:           mate-icon-theme-faenza
Version:        1.8.0
Release:        4%{?dist}
#Release:        0.1.git%{_internal_version}%{?dist}
Summary:        Extra set of icon themes for MATE Desktop
Summary(zh_CN.UTF-8): MATE 桌面的额外图标集合
License:        GPLv2+
URL:            http://mate-desktop.org

# To generate tarball
# wget http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-{_internal_version}.tar.xz -O %%{name}-%%{version}.git%%{_internal_version}.tar.xz
#Source0: http://raveit65.fedorapeople.org/Mate/git-upstream/%{name}-%{version}.git%{_internal_version}.tar.xz

%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: hardlink
BuildRequires: mate-common

BuildArch: noarch

%description
Provides a complimentary set of icon themes for MATE Desktop

%description -l zh_CN.UTF-8
MATE 桌面的额外图标集合。

%prep
%setup -q
#%setup -q -n %{name}-%{_internal_version}

# nedded for git snapshots
#NOCONFIGURE=1 ./autogen.sh


%build
%configure
make %{?_smp_mflags} V=1

%install
%{make_install}

# save space by linking identical images
hardlink -c -v %{buildroot}%{_datadir}/icons
magic_rpm_clean.sh

%post
/bin/touch --no-create %{_datadir}/icons/matefaenza &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/matefaenzagray &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/matefaenzadark &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/matefaenza &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenza &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons//matefaenzadark &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenzadark &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons//matefaenzagray &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenzagray &> /dev/null || :


fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenza &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenzadark &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/matefaenzagray &> /dev/null || :




%files
%{_datadir}/icons/matefaenzagray
%{_datadir}/icons/matefaenzadark
%{_datadir}/icons/matefaenza
%doc AUTHORS COPYING README NEWS



%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.8.0-4
- 为 Magic 3.0 重建

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Mon Jan 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.0-1
- update to 1.7.0 release
- use modern 'make install' macro

* Thu Sep 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.1.gitc147867
- update latest git snapshot
- fix mate-icon-theme-faenza included Trademark and non-free logo, rhbz (#1005464)

* Wed Jul 31 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Initial build
