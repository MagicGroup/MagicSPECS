Name: texi2html
Version: 1.82
Release: 3%{?dist}
# GPLv2+ is for the code
# OFSFDL (Old FSF Documentation License) for the documentation
# CC-BY-SA or GPLv2 for the images
License: GPLv2+ and OFSFDL and (CC-BY-SA or GPLv2)
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Summary: A highly customizable texinfo to HTML and other formats translator
Summary(zh_CN.UTF-8): 高度可定制的texinfo到HTML和其它格式的转换器
Source0: http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.bz2
URL: http://www.nongnu.org/texi2html/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: perl >= 5.004
Requires: latex2html
BuildRequires: perl(Text::Unidecode) 
# not detected automatically because it is required at runtime based on
# user configuration
Requires: perl(Text::Unidecode)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
The basic purpose of texi2html is to convert Texinfo documents into HTML, 
and other formats.  Configuration files written in perl provide fine degree 
of control over the final output, allowing most every aspect of the final 
output not specified in the Texinfo input file to be specified.  

%description -l zh_CN.UTF-8
texi2html的基本目标是转换Texinfo文档到HTML和其它格式。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# directories shared by all the texinfo implementations for common
# config files, like htmlxref.cnf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texinfo $RPM_BUILD_ROOT%{_sysconfdir}/texinfo


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO %{name}.init
%{_bindir}/%{name}
%{_datadir}/texinfo/html/%{name}.html
%{_mandir}/man*/%{name}*
%{_infodir}/%{name}.info*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.init
%{_datadir}/%{name}/*.texi
%dir %{_datadir}/%{name}/i18n/
%{_datadir}/%{name}/i18n/*
%dir %{_datadir}/%{name}/images/
%{_datadir}/%{name}/images/*
%dir %{_datadir}/texinfo
%dir %{_sysconfdir}/texinfo

%changelog
* Wed Jan 09 2013 Liu Di <liudidi@gmail.com> - 1.82-3
- 为 Magic 3.0 重建

