%define lang en
%define langrelease 0
%define aspellversion 6
Summary: English dictionaries for Aspell
Summary(zh_CN.UTF-8): Aspell 的英语字典
Name: aspell-%{lang}
Epoch: 50
Version: 7.1
Release: 5%{?dist}
License: MIT and BSD
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Buildrequires: aspell >= 12:0.60
Requires: aspell >= 12:0.60
Obsoletes: aspell-en-gb <= 0.33.7.1
Obsoletes: aspell-en-ca <= 0.33.7.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: English, Canadian
English, British English

%description -l zh_CN.UTF-8
Aspell 的英语字典。

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 50:7.1-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 50:7.1-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 50:7.1-3
- 为 Magic 3.0 重建


