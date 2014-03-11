%define pkgname Ogg-Vorbis-Header

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

Name: perl-Ogg-Vorbis-Header
Summary: Ogg-Vorbis-Header - An object-oriented interface to Ogg Vorbis
Summary(zh_CN): Ogg Vorbis 面向对象的接口
Version: 0.03
Release: 2%{?dist}
License: Artistic
Group: Applications/CPAN
Group(zh_CN): 应用程序/CPAN
Url: http://search.cpan.org/dist/Ogg-Vorbis-Header/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Prefix: %{_prefix}
Source: http://search.cpan.org/CPAN/authors/id/A/AM/AMOLLOY/Ogg-Vorbis-Header-0.03.tar.gz

BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: perl(Inline) >= 0.44
Requires: perl(Inline) >= 0.44

%description
This module presents an object-oriented interface to Ogg Vorbis files
which allows user to view Vorbis info and comments and to modify or
add comments.

%description -l zh_CN
本模块提供了对 Ogg Vorbis 文件的面向对象的接口。
它能让用户查看 Vorbis 信息和评论并修改或添加评论。

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"

%{__make}

%install
%{__rm} -rf %{buildroot}

%makeinstall

### Clean up buildroot
%{__rm} -rf %{buildroot}%{perl_archlib}/perllocal.pod %{buildroot}%{perl_vendorarch}/auto/Ogg/Vorbis/Header/.packlist

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,0755)
%doc Changes README LICENSE.GPL
%doc %{_mandir}/man3/Ogg::Vorbis::Header.3pm.gz
%dir %{perl_vendorarch}/Ogg
%dir %{perl_vendorarch}/Ogg/Vorbis
%{perl_vendorarch}/Ogg/Vorbis/Header.pm
%{perl_vendorarch}/auto/Ogg/Vorbis/Header/*.bs
%{perl_vendorarch}/auto/Ogg/Vorbis/Header/*.so

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.03-0.1mgc
- Initial build
