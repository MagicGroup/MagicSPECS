%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name Audio-WMA

Summary: Perl extension for reading WMA/ASF Metadata
Summary(zh_CN): 读取 WMA/ASF 元数据的 Perl 扩展模块
Name: perl-Audio-WMA
Version: 1.3
Release: 8%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/D/DA/DANIEL/%{pkg_name}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(ExtUtils::MakeMaker)

%description
This module implements access to metadata contained in WMA files.

%description -l zh_CN
本模块能实现对于包含在 WMA 文件中元数据的访问。

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

# check 过程需要额外依赖 perl(Test:Pod)
#%{!?_without_test:%{__make} test}

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
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.3-8
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.3-7
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.3-6
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.3-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.1-0.1mgc
- Initial package
