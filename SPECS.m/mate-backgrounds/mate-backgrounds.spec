Name:		mate-backgrounds
Version: 1.9.90
Release: 2%{?dist}
Summary:	MATE Desktop backgrounds
Summary(zh_CN.UTF-8): MATE 桌面背景
License:	GPLv2+
URL:		http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildArch:	noarch
BuildRequires:	mate-common

%description
Backgrounds for MATE Desktop

%description -l zh_CN.UTF-8
MATE 桌面背景。

%prep
%setup -q

%build
%configure

make %{?_smp_mflags} V=1


%install
%{make_install}
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/mate-background-properties
%{_datadir}/backgrounds/mate


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.9.90-2
- 更新到 1.9.90

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- use modern 'make install' macro
- use --with-gnome --all-name for find locale

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- remove unused configure option
- remove unused buildrequires

* Tue Nov 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Mon Aug 13 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
