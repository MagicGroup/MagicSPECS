
%define fontdir       %{_datadir}/fonts/mathml

Summary: Mathematical symbol fonts
Summary(zh_CN.UTF-8): 数学符号字体
Name:    mathml-fonts
Version: 1.0 
Release: 25%{?dist}

URL:     http://www.mozilla.org/projects/mathml/fonts/
# The actual license says "The author of these fonts, Basil K. Malyshev, has 
# kindly granted permission to use and modify these fonts."
# One of the font files is separately licensed GPL+.
License: Copyright only and GPL+
Group:   User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## Sources
Source1: find_symbol_font.sh
# Install as:
%define find_symbol_dir  %{_libexecdir}/%{name}
%define find_symbol_font %{find_symbol_dir}/find_symbol_font.sh

## Mathematica fonts
#  License: http://support.wolfram.com/mathematica/systems/windows/general/latestfonts.html (non-distributable)
%{?_with_mathematica:Source10: http://support.wolfram.com/mathematica/systems/windows/general/MathFonts_TrueType.exe}
## TeX fonts
# Bakoma TeX fonts, http://wiki.lyx.org/FAQ/Qt
Source20: ftp://ftp.lyx.org/pub/lyx/contrib/BaKoMa4LyX-1.1.zip
# extras (cmbx10)
Source21: ftp://tug.ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/ttf/cmbx10.ttf
#Now included in BaKoMa4LyX-1.1
#Source22: ftp://tug.ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/ttf/eufm10.ttf

## Design Science fonts, URL: http://www.dessci.com/en/dl/fonts/
Source30: http://www.dessci.com/en/dl/MathTypeTrueTypeFonts.asp
Source31: http://www.dessci.com/en/support/eula/fonts/mtextralic.htm

BuildRequires: cabextract
BuildRequires: unzip

# we're pretty much useless without it, and use fc-cache in scriptlets 
# but, fontconfig will run fc-cache on install, so what's the big deal?
#Prereq: fontconfig

# Provide lyx upstream contrib rpms
Provides: latex-xft-fonts = 0.1
Provides: latex-bakoma4lyx-fonts = 1

%description
This package contains fonts required to display mathematical
symbols.  Applications supported include:
* mozilla-based browsers (including firefox, seamonkey) to display MathML
* lyx
* kformula (koffice)

%description -l zh_CN.UTF-8
数学符号字体

%prep
%setup -T -c -n %{name}

## Math'ca
%{?_with_mathematica:unzip %{SOURCE10}}

## TeX fonts
# BaKoMa4Lyx
%setup -T -D -n %{name} -a 20
# cmbx
install -p -m644 %{SOURCE21} .

## MathType fonts (mtextra)
cabextract %{SOURCE30}
install -p -m644 %{SOURCE31} .


%build
# blank


%install
rm -rf "$RPM_BUILD_ROOT"

install -d $RPM_BUILD_ROOT%{fontdir}

install -p -m644 \
  %{?_with_mathematica:math{1,2,4}___.ttf} \
  *10.ttf mtextra.ttf \
  $RPM_BUILD_ROOT%{fontdir}/

# find_symbol_font
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{find_symbol_font}

# "touch" all fonts.dir, fonts.scale, etc files we've got flagged as %ghost
touch $RPM_BUILD_ROOT%{fontdir}/{fonts.cache-1,Symbol.pfa,SY______.PFB}


%triggerin -- acroread,AdobeReader_enu
%{find_symbol_font} ||:

%triggerun -- acroread,AdobeReader_enu
if [ $2 -eq 0 ]; then
  fc-cache -f %{fontdir} 2> /dev/null ||: 
fi

%post
%{find_symbol_font} ||:
fc-cache -f %{fontdir} 2> /dev/null ||: 

%postun
if [ $1 -eq 0 ]; then
  fc-cache 2> /dev/null ||: 
fi


%files
%defattr(-,root,root)
%doc Licence.txt mtextralic.htm Readme.txt
%dir %{find_symbol_dir}
%{find_symbol_font}
%dir %{fontdir}
%{fontdir}/*.[ot]tf
%ghost %{fontdir}/Symbol.pfa
%ghost %{fontdir}/SY______.PFB
%ghost %{fontdir}/fonts.cache-*


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 1.0-25
- 为 Magic 3.0 重建

* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 1.0-24
- 为 Magic 3.0 重建


