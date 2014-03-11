Summary:	Namespace-aware XML parser written in TeX
Summary(zh_CN.UTF-8): 以 TeX 写的命名空间 XML 解析器
Name:		xmltex
Version:	20020625
Release:	14%{?dist}
License:	LPPL
Group:		Applications/Publishing
Group(zh_CN.UTF-8):	应用程序/出版
URL:			http://www.dcarlisle.demon.co.uk/xmltex/manual.html
Source0:	ftp://ftp.tex.ac.uk/tex-archive/macros/xmltex-1.9.tar.gz
Requires:	tex(latex)
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

BuildRequires: tex(latex)

%description
Namespace-aware XML parser written in TeX.

%description -l zh_CN.UTF-8
以 TeX 写的命名空间 XML 解析器。

%prep
%setup -q -c %{name}-%{version}
mv -f xmltex/base/* .


%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/texmf/tex/xmltex
install -d $RPM_BUILD_ROOT%{_bindir}

install -p *.xmt %{name}.cfg *.ini *.tex $RPM_BUILD_ROOT%{_datadir}/texmf/tex/xmltex
ln -s pdftex ${RPM_BUILD_ROOT}%{_bindir}/pdf%{name}
ln -s latex ${RPM_BUILD_ROOT}%{_bindir}/%{name}

gzip -9nf readme.txt
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :
for f in xmltex pdfxmltex; do
/usr/bin/env - PATH=$PATH:%{_bindir} fmtutil-sys --byfmt $f > /dev/null 2>&1
done
exit 0

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :

%triggerin -- tetex-latex
for f in xmltex pdfxmltex; do
/usr/bin/env - PATH=$PATH:%{_bindir} fmtutil-sys --byfmt $f > /dev/null 2>&1
done
exit 0

%files
%defattr(644,root,root,755)
%doc *.gz *.html
%attr(755,root,root) %{_bindir}/*
%{_datadir}/texmf/tex/xmltex

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 20020625-14
- 为 Magic 3.0 重建

* Sun Feb 26 2012 Liu Di <liudidi@gmail.com> - 20020625-13
- 为 Magic 3.0 重建


