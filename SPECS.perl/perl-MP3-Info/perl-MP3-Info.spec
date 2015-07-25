%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name MP3-Info

Summary: Manipulate / fetch info from MP3 audio files
Summary(zh_CN): 从 MP3 音频文件中控制/获取信息
Name: perl-MP3-Info
Version: 1.24
Release: 8%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/D/DA/DANIEL/%{pkg_name}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(ExtUtils::MakeMaker)
%{!?_without_test:BuildRequires: perl(Test::More)}


%description
Manipulate / fetch info from MP3 audio files.

%description -l zh_CN
从 MP3 音频文件中控制/获取信息。

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%{!?_without_test:%{__make} test}

%install
%{__rm} -rf %{buildroot}

%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc Changes README TODO
%doc %{_mandir}/man3/*.3pm*
%{perl_vendorlib}

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.24-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.24-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.24-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.24-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.24-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.24-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.24-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.23-0.1mgc
- Initial package
