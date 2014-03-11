Name: jadetex
Version: 3.13
Release: 5%{?dist}
Group: Applications/Publishing
Group(zh_CN.GB18030): ”¶”√≥Ã–Ú/≥ˆ∞Ê

Summary: TeX macros used by Jade TeX output
Summary(zh_CN.GB18030): Jade TeX  ‰≥ˆ π”√µƒ Tex ∫Í

License: Freely redistributable without restriction
URL: http://sourceforge.net/projects/jadetex

Requires: sgml-common >= 0.5
Requires: tetex >= 3.0 tetex-latex >= 3.0
Requires: jade
Requires(post): tetex >= 3.0
BuildRequires: unzip tetex-latex tetex tetex-fonts

BuildRoot: %{_tmppath}/%{name}-%{version}

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: jadefmtutil.cnf
Patch0: jadetex-tetex3.patch
Patch1: jadetex-3.13-typoupstream.patch


%description
JadeTeX contains the additional LaTeX macros necessary for taking Jade
TeX output files and processing them as TeX files (to obtain DVI,
PostScript, or PDF files, for example).

%description -l zh_CN.GB18030
JadeTeX ∞¸∫¨¡À∂ÓÕ‚µƒ LaTeX ∫Í£¨Jade TeX “‘ TeX Œƒº˛ ‰≥ˆŒƒº˛≤¢¥¶¿ÌÀ¸√«
µƒ ±∫Ú–Ë“™°£

%prep
%setup -q
cp -p %{SOURCE1} .
%patch0 -p1 -b .tetex3
%patch1 -p1 -b .typoupstream

%build
make


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR
mkdir -p $DESTDIR
make install DESTDIR=$DESTDIR

mkdir -p ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.ini ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.sty ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.cnf ${DESTDIR}%{_datadir}/texmf/tex/jadetex

mkdir -p ${DESTDIR}%{_bindir}
ln -s etex ${DESTDIR}%{_bindir}/jadetex
ln -s pdfetex ${DESTDIR}%{_bindir}/pdfjadetex


%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR


%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :
%{_bindir}/env - PATH=$PATH:%{_bindir} fmtutil-sys --cnffile %{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf --all --fmtdir %{_datadir}/texmf/web2c > /dev/null 2>&1
exit 0

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :


%files
%defattr(-,root,root,-)
%doc index.html
%ghost %{_datadir}/texmf/web2c/jadetex.fmt
%ghost %{_datadir}/texmf/web2c/pdfjadetex.fmt
%dir %{_datadir}/texmf/tex/jadetex
%{_datadir}/texmf/tex/jadetex/dsssl.def
%{_datadir}/texmf/tex/jadetex/jadetex.ltx
%{_datadir}/texmf/tex/jadetex/jadetex.ini
%{_datadir}/texmf/tex/jadetex/pdfjadetex.ini
%{_datadir}/texmf/tex/jadetex/dummyels.sty
%{_datadir}/texmf/tex/jadetex/mlnames.sty
%{_datadir}/texmf/tex/jadetex/ucharacters.sty
%{_datadir}/texmf/tex/jadetex/uentities.sty
%{_datadir}/texmf/tex/jadetex/unicode.sty
%{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf
%{_bindir}/jadetex
%{_bindir}/pdfjadetex

%triggerin -- tetex-latex
/usr/bin/env - PATH=$PATH:%{_bindir} fmtutil-sys --cnffile %{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf --all > /dev/null 2>&1
exit 0

%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 3.13-5
- ‰∏∫ Magic 3.0 ÈáçÂª∫

* Fri Nov 20 2008 Liu Di <liudidi@gmail.com> - 3.13-2%{?dist}
- ÷ÿΩ®

