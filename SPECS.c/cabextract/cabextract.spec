Name:           cabextract
Version:        1.4
Release:        6%{?dist}
Summary:        Utility for extracting cabinet (.cab) archives
Summary(zh_CN.UTF-8): 解压缩 (.cab) 格式归档的工具

Group:          Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
License:        GPLv2+
URL:            http://www.cabextract.org.uk/
Source:         http://www.cabextract.org.uk/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libmspack-devel


%description
cabextract is a program which can extract files from cabinet (.cab)
archives.

%description -l zh_CN.UTF-8
解压缩 (.cab) 格式归档的工具。

%prep
%setup -q


%build
%configure --with-external-libmspack

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/cabextract
%{_mandir}/man1/cabextract.1*


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.4-6
- 为 Magic 3.0 重建

* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 1.4-5
- 为 Magic 3.0 重建

* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 1.4-4
- 为 Magic 3.0 重建


