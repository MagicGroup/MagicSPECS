%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name MP4-Info

Summary: Fetch info from MPEG-4 files
Summary(zh_CN): 从 MPEG-4 文件中获取信息
Name: perl-MP4-Info
Version: 1.13
Release: 5%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/J/JH/JHAR/%{pkg_name}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(ExtUtils::MakeMaker)
%{!?_without_test:BuildRequires: perl(Encode)}
%{!?_without_test:BuildRequires: perl(IO::String)}

%description
The MP4::Info module can be used to extract tag and meta information from
MPEG-4 audio (AAC) and video files. It is designed as a drop-in replacement
for MP3::Info. Note that this module does not allow you to update the
information in MPEG-4 files.

%description -l zh_CN
MP4::Info 模块可以用来从 MPEG-4 音频 (AAC) 和视频文件中解压缩标记和元数据信息。
它被设计为 MP3::Info 的一种替代物。
注意：本模块不允许您更新 MPEG-4 文件中的信息。

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
%doc README
%doc %{_mandir}/man3/*.3pm*
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

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.12-0.1mgc
- Initial package
