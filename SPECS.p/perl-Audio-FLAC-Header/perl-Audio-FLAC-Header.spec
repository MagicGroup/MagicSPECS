%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define pkg_name Audio-FLAC-Header

Summary: Access to FLAC audio metadata
Summary(zh_CN): 对于 FLAC 音频元数据的访问
Name: perl-Audio-FLAC-Header
Version: 2.4
Release: 2%{?dist}
Group: Development/Libraries
Group(zh_CN): 开发/库
License: Artistic
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0: http://www.cpan.org/authors/id/D/DA/DANIEL/%{pkg_name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: flac-devel

%description
This module returns a hash containing basic information about a FLAC
file, a representation of the embedded cue sheet if one exists, as well
as tag information contained in the FLAC file's Vorbis tags.

%description -l zh_CN
本模块能返回关于 FLAC 文件的哈希基本信息，内嵌的 cue 表单，以及
包含在 FLAC 文件的 Vorbis 标记的标记信息。

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%{__perl} Makefile.PL PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

# check 过程需要额外依赖 perl(Test::Pod)
#%{!?_without_test:%{__make} test}

%install
%{__rm} -rf %{buildroot}

%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib}/perllocal.pod %{buildroot}%{perl_archlib}/auto

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc Changes README TODO
%doc %{_mandir}/man3/*.3pm*
%{perl_archlib}

%changelog
* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 2.4-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 1.8-0.1mgc
- Initial package
