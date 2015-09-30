Name:           splint
Version:        3.1.2
Release:        5%{?dist}
Summary:        An implementation of the lint program
Summary(zh_CN.UTF-8): lint 程序的实现

Group:          Development/Tools
Group(zh_CN.UTF-8):	开发/工具
License:        GPLv2+
URL:            http://www.splint.org/
Source0:        http://www.splint.org/downloads/%{name}-%{version}.src.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	flex 

Obsoletes:      lclint

%description
Splint is a tool for statically checking C programs for coding errors and
security vulnerabilities. With minimal effort, Splint can be used as a
better lint. If additional effort is invested adding annotations to programs,
Splint can perform even stronger checks than can be done by any standard lint.

%description -l zh_CN.UTF-8
Splint 扫描 C 编码以寻找错误和不对的样式。

%prep
%setup -q
chmod 644 doc/manual.pdf
cp -p src/.splintrc splintrc.demo

%build
%configure
# Parallel builds seem to fail
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README doc/manual.pdf splintrc.demo
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_datadir}/%{name}/


%changelog
* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 3.1.2-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.1.2-4
- 为 Magic 3.0 重建

* Thu Feb 09 2012 Liu Di <liudidi@gmail.com> - 3.1.2-3
- 为 Magic 3.0 重建


