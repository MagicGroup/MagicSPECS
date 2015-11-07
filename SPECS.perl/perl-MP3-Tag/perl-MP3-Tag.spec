%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name MP3-Tag

Summary: Module for reading tags of mp3 files
Summary(zh_CN): 读取 mp3 文件标记的模块
Name: perl-MP3-Tag
Version: 1.13
Release: 5%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/I/IL/ILYAZ/modules/%{pkg_name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(ExtUtils::MakeMaker)


%description
Tag is a wrapper module to read different tags of mp3 files. It provides an
easy way to access the functions of separate modules which do the handling of
reading/writing the tags itself.

%description -l zh_CN
Tag 是一个用于读取 mp3 文件的不同标记的包装化模块。
它提供了一种简单的途径来访问分离的自身处理读取/写入标记的模块功能。

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
%doc Changes README* TODO
%doc %{_mandir}/man3/*.3pm*
%{_bindir}/audio_rename
%{_bindir}/mp3info2
%{_bindir}/typeset_audio_dir
%{_mandir}/man1/*.1.gz
%{perl_vendorlib}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.13-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.13-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.13-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.13-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.9709-0.1mgc
- Initial package
