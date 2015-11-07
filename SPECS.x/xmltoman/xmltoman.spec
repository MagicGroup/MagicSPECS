Name:           xmltoman
Version:        0.4
Release:        6%{?dist}
Summary:        Scripts for converting XML to roff or HTML
Summary(zh_CN.UTF-8): 转换 XML 到 roff 或 HTML 的脚本

Group:          Applications/Publishing
Group(zh_CN.UTF-8):	应用程序/出版
License:        GPLv2+
URL:            http://sourceforge.net/projects/xmltoman/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         xmltoman-0.3-timestamps.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(XML::Parser)
BuildArch:      noarch

%description
This package provides xmltoman and xmlmantohtml scripts, to compile
the xml representation of manual page to either roff source, or HTML
(while providing the CSS stylesheet for eye-candy look). XSL stylesheet
for doing rougly the same job is provided.

%description -l zh_CN.UTF-8
转换 XML 到 roff 或 HTML 的脚本。

%prep
%setup -q
%patch0 -p1 -b .timestamps


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/xmltoman
%{_bindir}/xmlmantohtml
%{_datadir}/xmltoman
%doc COPYING README


%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.4-6
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 0.4-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.4-4
- 为 Magic 3.0 重建

* Sun Feb 26 2012 Liu Di <liudidi@gmail.com> - 0.4-3
- 为 Magic 3.0 重建

