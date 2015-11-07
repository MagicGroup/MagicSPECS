%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name Audio-Scan

Summary: Fast C metadata and tag reader for all common audio file formats  
Summary(zh_CN.UTF-8): 快速的 C 编写的所有通用音频文件格式的元数据和标记读取程序
Name: perl-Audio-Scan
Version: 0.93
Release: 11%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://search.cpan.org/CPAN/authors/id/A/AG/AGRUNDMA/%{pkg_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(MP3::Info) >= 1.20

%description
Fast C metadata and tag reader for all common audio file formats  

%description -l zh_CN.UTF-8
快速的 C 编写的所有通用音频文件格式的元数据和标记读取程序。

%prep
%setup -q -n %{pkg_name}-%{version}

%build
export PERL_MM_USE_DEFAULT=1 PERL5LIB=""                 \
  PERL_AUTOINSTALL=--skipdeps                            \
  MODULEBUILDRC=/dev/null
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

# check 过程需要额外依赖 perl(Test:Pod)
#%{__make} test

%install
%{__rm} -rf %{buildroot}

%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib}/perllocal.pod 
#%{buildroot}%{perl_vendorarch}/auto
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc Changes README
%doc %{_mandir}/man3/*.3pm*
%{perl_archlib}/*
%{perl_vendorarch}/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.93-11
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.93-10
- 为 Magic 3.0 重建

* Wed Apr 15 2015 Liu Di <liudidi@gmail.com> - 0.93-9
- 为 Magic 3.0 重建

* Wed Apr 15 2015 Liu Di <liudidi@gmail.com> - 0.93-8
- 为 Magic 3.0 重建

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 0.93-7
- 为 Magic 3.0 重建

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 0.93-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.93-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.93-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.93-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.93-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.7-0.1mgc
- Initial package
