Name:		mate-calc
Version:	1.8.0
Release:	4%{?dist}
Summary:	MATE Desktop calculator
Summary(zh_CN.UTF-8): MATE 桌面的计算器
License:	GPLv2+
URL:		http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:	gtk2-devel
BuildRequires:	libxml2-devel
BuildRequires:	mate-common
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	mate-desktop-devel
BuildRequires:	desktop-file-utils


%description
mate-calc is a powerful graphical calculator with financial, logical and scientific modes.
It uses a multiple precision package to do its arithmetic to give a high degree of accuracy.

%description -l zh_CN.UTF-8
MATE 桌面的计算器。

%prep
%setup -q -n %{name}-%{version}


%build
%configure --disable-schemas-compile \
           --with-gtk=2.0

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}


desktop-file-install									\
	--delete-original								\
	--dir=%{buildroot}%{_datadir}/applications					\
%{buildroot}%{_datadir}/applications/*.desktop
magic_rpm_clean.sh
%find_lang %{name} --all-name

%postun
if [ $1 -eq 0 ] ; then
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-calc
%{_bindir}/mate-calc-cmd
%{_bindir}/mate-calculator
%{_datadir}/applications/mate-calc.desktop
%{_datadir}/glib-2.0/schemas/org.mate.calc.gschema.xml
%{_datadir}/mate-calc
%{_datadir}/help/*/mate-calc


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.8.0-4
- 为 Magic 3.0 重建

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-2
- switch to proper upstream url
- fix setup line

* Sun Nov 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- specfile cleanup
- add more descriptive %%description section
- remove unused configure options
- remove unused build requires

* Mon Nov 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.0-1
- Initial build
