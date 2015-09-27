Name:           shntool
Version:        3.0.10
Release:        6%{?dist}
Summary:        A multi-purpose WAVE data processing and reporting utility
Summary(zh_CN.UTF-8): 多用途音频数据处理和报告工具

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPLv2+
URL:            http://etree.org/shnutils/shntool
Source0:        http://etree.org/shnutils/shntool/dist/src/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A multi-purpose WAVE data processing and reporting utility. File
formats are abstracted from its core, so it can process any file that contains
WAVE data, compressed or not - provided there exists a format module to handle
that particular file type. 

%description -l zh_CN.UTF-8
多用途音频数据处理和报告工具。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%doc doc/*
%{_bindir}/shn*
%{_mandir}/man1/%{name}.1.gz


%changelog
* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 3.0.10-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.0.10-5
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 3.0.10-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Felix Kaechele <felix at fetzig dot org> - 3.0.10-1
- 3.0.10

* Sun Mar 29 2009 Felix Kaechele <felix at fetzig dot org> - 3.0.9-1
- 3.0.9

* Tue Mar 03 2009 Felix Kaechele <felix at fetzig dot org> - 3.0.8-1
- initial build
