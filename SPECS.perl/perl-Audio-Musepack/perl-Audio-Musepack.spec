%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name Audio-Musepack

Summary: An OOP interface to Musepack file information and APE tag fields
Summary(zh_CN.UTF-8): Musepack 文件信息和 APE 标记的面向对象的接口
Name: perl-Audio-Musepack
Version:	1.0.1
Release:	9%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/D/DA/DANIEL/%{pkg_name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(MP3::Info) >= 1.20

%description
This module returns a hash containing basic information about a Musepack
file, as well as tag information contained in the Musepack file's APE tags.
See Audio::APETags for more information about the tags.

%description -l zh_CN.UTF-8
Musepack 文件信息和 APE 标记的面向对象的接口。

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

# check 过程需要额外依赖 perl(Test:Pod)
#%{__make} test

%install
%{__rm} -rf %{buildroot}

%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc Changes README
%doc %{_mandir}/man3/*.3pm*
%{perl_vendorlib}

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.0.1-9
- 为 Magic 3.0 重建

* Wed Apr 15 2015 Liu Di <liudidi@gmail.com> - 1.0.1-8
- 为 Magic 3.0 重建

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 1.0.1-7
- 为 Magic 3.0 重建

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.0.1-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.0.1-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.7-0.1mgc
- Initial package
