%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:       dblatex
Version:    0.3.4
Release:    8%{?dist}
Summary:    DocBook to LaTeX/ConTeXt Publishing
Summary(zh_CN.UTF-8): DocBook 转换到 LaTeX/ConTeXt
BuildArch:  noarch
# Most of package is GPLv2+, except:
# xsl/ directory is DMIT
# lib/dbtexmf/core/sgmlent.txt is Public Domain
# latex/misc/enumitem.sty, multirow2.sry and ragged2e.sty are LPPL
# latex/misc/lastpage.sty is GPLv2 (no +)
# latex/misc/passivetex is MIT (not included in binary RPM so not listed)
License:    GPLv2+ and GPLv2 and LPPL and DMIT and Public Domain
URL:        http://dblatex.sourceforge.net/
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source1 is from http://docbook.sourceforge.net/release/xsl/current/COPYING
Source1:    COPYING-docbook-xsl
Patch0:     dblatex-0.2.7-external-which.patch
Patch1:     dblatex-disable-debian.patch

BuildRequires:  python-devel
BuildRequires:  python-which
BuildRequires:  libxslt
BuildRequires:  ImageMagick
BuildRequires:  texlive-base
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-collection-xetex
BuildRequires:  texlive-collection-htmlxml
BuildRequires:  transfig
BuildRequires:  texlive-epstopdf-bin
BuildRequires:  texlive-xmltex-bin
BuildRequires:  texlive-anysize
BuildRequires:  texlive-appendix
BuildRequires:  texlive-changebar
BuildRequires:  texlive-jknapltx
BuildRequires:  texlive-multirow
BuildRequires:  texlive-overpic
BuildRequires:  texlive-pdfpages
BuildRequires:  texlive-subfigure
BuildRequires:  texlive-stmaryrd
Requires:       texlive-base
Requires:       texlive-collection-latex
Requires:       texlive-collection-xetex
Requires:       texlive-collection-htmlxml
Requires:       texlive-collection-fontsrecommended
Requires:       texlive-epstopdf-bin
Requires:       texlive-passivetex
Requires:       texlive-xmltex texlive-xmltex-bin
Requires:       texlive-anysize
Requires:       texlive-appendix
Requires:       texlive-bibtopic
Requires:       texlive-changebar
Requires:       texlive-ec
Requires:       texlive-jknapltx
Requires:       texlive-multirow
Requires:       texlive-overpic
Requires:       texlive-passivetex
Requires:       texlive-pdfpages
Requires:       texlive-subfigure
Requires:       texlive-stmaryrd
Requires:       texlive-xmltex-bin
Requires:       libxslt docbook-dtds
Requires:       transfig
Requires:       ImageMagick

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

Authors:
--------
   Benoît Guillon <marsgui at users dot sourceforge dot net>
   Andreas Hoenen <andreas dot hoenen at arcor dot de>

%description -l zh_CN.UTF-8
这是一个转换 SGML/XML DocBook 文档到纯 LaTex 的程序，以便于
制作 DVI, PS 或 PDF 文件。支持 MathML 2.0 标记。

%prep
%setup -q
%patch0 -p1 -b .external-which
%patch1 -p1 -b .disable-debian
rm -rf lib/contrib

%build
%{__python} setup.py build


%install
#%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/ xelatex/; do
  rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

## also move .xetex files
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.xetex' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

rmdir $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl


%files
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{python_sitelib}/dbtexmf/
%{python_sitelib}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex

%post -p /usr/bin/texhash

%postun -p /usr/bin/texhash

%changelog

