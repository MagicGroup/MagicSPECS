%define language	japanese
%define basefontdir	%{_datadir}/fonts/%{language}
%define ttfontdir	%{basefontdir}/TrueType
%define bmpfontdir	%{basefontdir}/misc
%define cidmapdir	%{_sysconfdir}/ghostscript
%define chxlfd		/usr/bin/perl $RPM_BUILD_DIR/%{name}-%{version}/%{vft}/chbdfxlfd.pl
%define mkalias		/usr/bin/perl $RPM_BUILD_DIR/%{name}-%{version}/%{vft}/mkalias.pl
%define mkbold		$RPM_BUILD_DIR/%{name}-%{version}/%{shinonome}-src/tools/mkbold
%define mkitalic	$RPM_BUILD_DIR/%{name}-%{version}/%{vft}/mkitalic

%define sazanami	VLGothic-20090710
## FIXME: the below lines will be removed in the future.
#%%define substname	kochi-substitute
#%%define substver	20030809
#%%define kochisubst	%{substname}-%{substver}
#%%define ksnonaga10	%{substname}-nonaga10-%{substver}
#
%define kappa		Kappa20-0.396
%define shinonome	shinonome-0.9.11
%define	warabi12	warabi12-0.19a
%define	mplus		mplus_bitmap_fonts-2.2.2
%define	vft		vine-fonttools-0.1

Name:		fonts-japanese
Version:	0.20090710
Release: 	4%{?dist}
License:	Distributable
Group:		User Interface/X
Group(zh_CN):   用户界面/X
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	gzip xorg-x11-font-utils

## files in ttfonts-ja
Source0:	http://prdownloads.sourceforge.jp/efont/9934/%{sazanami}.tar.bz2
Source1:	fonts.alias.sz
Source2:	FAPIcidfmap.ja
Source3:	cidfmap.ja
## FIXME: the below lines will be removed in the future.
## Source0:     http://downloads.sourceforge.jp/efont/4767/%{kochisubst}.tar.bz2
#Source5:	%{ksnonaga10}.tar.bz2
#Source6:	fonts.alias.kk
## files in jisksp14
Source10:	jisksp14.bdf.gz
## files in jisksp16-1990
Source20:	jisksp16-1990.bdf.gz
## files in kappa20
## files in knm_new
Source40:	http://www.din.or.jp/~storm/fonts/knm_new.tar.gz
Source41:	ftp://ftp.freebsd.org/pub/FreeBSD/ports/distfiles/kaname_k12_bdf.tar.gz
## files in fonts-ja
Source50:	xfonts_jp.tgz
Source51:	http://kappa.allnet.ne.jp/20dot.fonts/%{kappa}.tar.bz2
Source52:	http://openlab.ring.gr.jp/efont/dist/shinonome/%{shinonome}-src.tar.bz2
## http://mlnews.com/marumoji/
Source53:	marumoji.tgz
# JIS X 0213-2000 fonts (14pxl, 16pxl)
# http://www.mars.sphere.ne.jp/imamura/jisx0213.html
# http://www.mars.sphere.ne.jp/imamura/K14-1.bdf.gz
# http://www.mars.sphere.ne.jp/imamura/K14-2.bdf.gz
# http://www.mars.sphere.ne.jp/imamura/jiskan16-2000-1.bdf.gz
# http://www.mars.sphere.ne.jp/imamura/jiskan16-2000-2.bdf.gz
Source54:	imamura-jisx0213.tgz
# jiskan16 JIS X 0208:1990 by Yasuoka
# http://kanji.zinbun.kyoto-u.ac.jp/~yasuoka/ftp/fonts/
Source55:	http://kanji.zinbun.kyoto-u.ac.jp/~yasuoka/ftp/fonts/jiskan16-1990.bdf.Z
# jiskan16 JIS X 0208:1997 Old Kanji
Source56:	http://kanji.zinbun.kyoto-u.ac.jp/~yasuoka/ftp/fonts/jiskano16-1997.bdf.Z
# k14 Old-Kanji
Source57:	http://www.hlla.is.tsukuba.ac.jp/~kourai/software/k14-oldkanji.tar.gz
## k14 invalid glyphs patch
## http://kappa.allnet.ne.jp/kanou/fonts/k14-patch.html
# Warabi12 (12pxl) jisx0213
# http://www.gelgoog.org/warabi12/
Source58:	http://www.gelgoog.org/warabi12/archives/%{warabi12}.tar.gz
# mplus fonts
# http://mplus-fonts.sourceforge.jp/
Source59:	http://prdownloads.sourceforge.jp/mplus-fonts/5030/%{mplus}.tar.gz
Source60:	%{vft}.tgz

Patch50:	http://kappa.allnet.ne.jp/kanou/fonts/k14.patch
# k14 to jisx0208.1990 patch
# http://www.brl.ntt.co.jp/people/takada/goodies/k14-1990/
# http://www.brl.ntt.co.jp/people/takada/goodies/k14-1990/patch.txt
Patch51:	k14-1990.patch
Patch52:	fonts-ja-8.0-gcc-warnings.patch
Patch53:	mplus_bitmap_fonts-install.patch
Patch54:	fonttools-replace.patch


Summary:	Free Japanese Bitmap/TrueType fonts
Summary(zh_CN):	免费的日文位图和 TrueType 字体

Requires(post): ttmkfdir >= 3.0.6, mkfontdir, fontconfig
Requires(postun): fontconfig
Obsoletes: ttfonts-ja jisksp14 jisksp16-1990 kappa20 knm_new fonts-ja

%description
This package provides the free Japanese Bitmap/TrueType fonts.

%description -l zh_CN
这个包提供了免费的日文位图和 TrueType 字体。

%prep
#%%setup -q -c -a 5 -a 40 -a 41 -a 50 -a 51 -a 52 -a 53 -a 54 -a 57 -a 58 -a 59 -a 60
%setup -q -c -a 40 -a 41 -a 50 -a 51 -a 52 -a 53 -a 54 -a 57 -a 58 -a 59 -a 60
## ttfonts-ja
## jisksp14
gunzip -c %{SOURCE10} > jisksp14.bdf
## jisksp16-1990
gunzip -c %{SOURCE20} > jisksp16-1990.bdf
## kappa20
## knm_new
## fonts-ja
gunzip -c %{SOURCE55} > jiskan16-1990.bdf
gunzip -c %{SOURCE56} > jiskano16-1997.bdf
%patch50 -p0
cp k14.bdf k14-1990.bdf
%patch51 -p0
%patch52 -p1
pushd %{mplus}
%patch53 -p1
popd
%patch54 -p1

%build
## jisksp14
bdftopcf jisksp14.bdf | gzip -9 > jisksp14.pcf.gz
## jisksp16-1990
bdftopcf jisksp16-1990.bdf | gzip -9 > jisksp16-1990.pcf.gz
## kappa20
## knm_new
## fonts-ja
pushd %{shinonome}-src
%configure --disable-bold --disable-italic --with-fontdir=$RPM_BUILD_ROOT%{bmpfontdir}
make bdf
popd
### rename Kappa and remove the bold fonts
pushd %{kappa}
  mv k20m.bdf k20.bdf
  mv 10x20rkm.bdf 10x20rk.bdf
  rm k20b.bdf 10x20rkb.bdf
popd
### rename in xfonts_jp
mv 7x14.bdf 7x14a.bdf
mv 8x16.bdf 8x16a.bdf
mv 12x24.bdf 12x24a.bdf
### marumoji
pushd marumoji
  for i in *.bdf; do
      %{chxlfd} $i '-Marumoji Club-Marumoji-.-.-.-.-.-.-.-.-.-.-.-.' $i.new && mv -f $i.new $i
  done
popd
### imamura jiskan16
pushd imamura-jisx0213
  for i in *.bdf; do
      %{chxlfd} $i '-Imamura-Fixed-.-.-.-.-.-.-.-.-.-.-.-.' $i.new && mv -f $i.new $i
  done
  mv K14-1.bdf k14-2000-1.bdf
  mv K14-2.bdf k14-2000-2.bdf
popd
### k14 and k14-1990 is used as Mincho
for i in k14.bdf k14-1990.bdf; do
    %{chxlfd} $i '-Misc-Mincho-.-.-.-.-.-.-.-.-.-.-.-.' $i.new && mv $i.new $i
done
### oldkanji
rm k14-oldkanji.pcf*
for i in k14-oldkanji.bdf jiskano16-1997.bdf; do
    %{chxlfd} $i '-Misc-.-.-.-.-Old Style-.-.-.-.-.-.-.-.' $i.new && mv $i.new $i
done
### warabi12
pushd %{warabi12}
  mv warabi12-1.bdf warabi12-2000-1.bdf
popd
### mplus
pushd %{mplus}
  DESTDIR=`pwd`/tmp/ ./install_mplus_fonts
popd

### move bdfs to topdir
mkdir fonts-ja
find -name "*.bdf" -path "./*/*" ! -path "./fonts-ja/*" ! -path "./fonts/*" -exec mv {} ./fonts-ja \;
mv k14-oldkanji.bdf jiskano16-1997.bdf k14-1990.bdf jiskan16-1990.bdf 7x14a.bdf 7x14rk.bdf 12x24a.bdf 12x24rk.bdf 8x16a.bdf 8x16rk.bdf k14.bdf jiskan16.bdf jiskan24.bdf ./fonts-ja/
### move the documents to topdir
for i in */README */COPYRIGHT */{LICENSE,README}_{E,J}; do
    mv $i fonts-ja/`basename $i`-`dirname $i`
done

ALL_MEDIUM_BDF_FONT="\
  shnmk12maru/     maru14/-L        maru16/                        \
  k14-oldkanji/    jiskano16-1997/                                 \
  k14-1990/-L      jiskan16-1990/                                  \
  warabi12-2000-1/                                                 \
  k14-2000-1/-L    k14-2000-2/-L                                   \
  jiskan16-2000-1/ jiskan16-2000-2/                                \
  shnm6x12a/-r     shnm6x12r/-r     shnmk12/ shnmk12p/ shnmk12min/ \
  shnm8x16a/-r     shnm8x16r/-r     shnmk16/           shnmk16min/ \
  7x14a/           7x14rk/          shnmk14/ k14/-L    shnmk14min/ \
  8x16a/           8x16rk/          jiskan16/                      \
  shnm9x18a/-r     shnm9x18r/-r                                    \
  10x20rk/         k20/                                            \
  12x24a/          12x24rk/         jiskan24/
"
ALL_BOLD_BDF_FONT="\
mplus_f10WEIGHT-euro/-r	mplus_f10WEIGHT/-r					\
mplus_f12WEIGHT-euro/-r	mplus_f12WEIGHT-jisx0201/-r	mplus_f12WEIGHT/-r	\
mplus_h10WEIGHT-euro/-r	mplus_h10WEIGHT-jisx0201/-r	mplus_h10WEIGHT/-r	\
mplus_h12WEIGHT-euro/-r	mplus_h12WEIGHT-jisx0201/-r	mplus_h12WEIGHT/-r	\
mplus_j10WEIGHT-iso/-r	mplus_j10WEIGHT-jisx0201/-r	mplus_j10WEIGHT/-r	\
mplus_j12WEIGHT/-r	\
mplus_s10WEIGHT-euro/-r	mplus_s10WEIGHT/-r
"
gcc $RPM_OPT_FLAGS %{vft}/mkitalic.c -o %{vft}/mkitalic

pushd fonts-ja
### delete 'r' from the filenames
for src in $ALL_BOLD_BDF_FONT; do
    mv `echo ${src%/*}.bdf | sed -e 's/WEIGHT/r/'` `echo ${src%/*}.bdf | sed -e 's/WEIGHT//'`
done

### making roman-bold fonts
for src in $ALL_MEDIUM_BDF_FONT; do
    %{mkbold} ${src#*/} -V ${src%/*}.bdf > ${src%/*}b.bdf
done
### making italic-medium fonts
for src in $ALL_MEDIUM_BDF_FONT; do
    %{mkitalic} -s 0.2 ${src%/*}.bdf > ${src%/*}i.bdf
done
for src in $ALL_BOLD_BDF_FONT; do
    %{mkitalic} -s 0.2 `echo ${src%/*}.bdf | sed -e 's/WEIGHT//'` > `echo ${src%/*}.bdf | sed -e 's/WEIGHT/i/'`
done
### making italic-bold fonts
for src in $ALL_MEDIUM_BDF_FONT; do
    %{mkbold} ${src#*/} -V ${src%/*}i.bdf > ${src%/*}bi.bdf
done
for src in $ALL_BOLD_BDF_FONT; do
    %{mkitalic} -s 0.2 `echo ${src%/*}.bdf | sed -e 's/WEIGHT/b/'` > `echo ${src%/*}.bdf | sed -e 's/WEIGHT/bi/'`
done

grep '^FONT ' *.bdf | sed -e 's/\.bdf:FONT//' > ALLFONTS.txt

### check the duplicated xlfds
DUP="`cut -d' ' -f2- ALLFONTS.txt | sort | uniq -d`"
if [ ! -z "$DUP" ]; then
    echo Duplicated XLFDs found. Please fix.
    echo -----------------------------------------
    echo "$DUP"
    exit 1
fi

cp ALLFONTS.txt mkalias.dat
# CHARSET PXL MISC FIXED MINCHO GOTHIC
# now, pixel 10 jisx0201 and pixel 20 gothic,
#      pixel 12 jisx0201 and pixel 24 gothic does not exist (fake)
%{mkalias} Misc-Fixed Alias-Fixed Alias-Gothic Alias-Mincho - \
ISO8859-1       10 mplus_f10WEIGHT mplus_f10WEIGHT mplus_j10WEIGHT - \
ISO8859-1       12 shnm6x12a shnm6x12a shnm6x12a shnm6x12a \
ISO8859-1       14 7x14a 7x14a 7x14a 7x14a \
ISO8859-1       16 shnm8x16a shnm8x16a shnm8x16a shnm8x16a \
ISO8859-1	18 shnm9x18a shnm9x18a shnm9x18a shnm9x18a \
ISO8859-1       20 10x20rk 10x20rk - 10x20rk \
ISO8859-1       24 12x24a 12x24a - 12x24a \
JISX0201.1976-0 10 mplus_j10WEIGHT-jisx0201 mplus_j10WEIGHT-jisx0201 mplus_j10WEIGHT-jisx0201 mplus_j10WEIGHT-jisx0201 \
JISX0201.1976-0 12 shnm6x12r shnm6x12r shnm6x12r shnm6x12r \
JISX0201.1976-0 14 7x14rk 7x14rk 7x14rk 7x14rk \
JISX0201.1976-0 16 shnm8x16r shnm8x16r shnm8x16r shnm8x16r \
JISX0201.1976-0	18 shnm9x18r shnm9x18r shnm9x18r shnm9x18r \
JISX0201.1976-0 20 10x20rk 10x20rk - 10x20rk \
JISX0201.1976-0 24 12x24rk 12x24rk - 12x24rk \
JISX0208.1983-0 10 mplus_j10WEIGHT mplus_j10WEIGHT mplus_j10WEIGHT - \
JISX0208.1983-0 12 shnmk12 shnmk12 shnmk12 shnmk12min \
JISX0208.1983-0 14 shnmk14 shnmk14 shnmk14 k14 \
JISX0208.1983-0 16 shnmk16 shnmk16 shnmk16 shnmk16min \
JISX0208.1983-0 20 - - - k20 \
JISX0208.1983-0 24 - - - jiskan24 \
JISX0208.1990-0 10 mplus_j10WEIGHT mplus_j10WEIGHT mplus_j10WEIGHT - \
JISX0213.2000-1 12 warabi12-2000-1 warabi12-2000-1 warabi12-2000-1 warabi12-2000-1 \
JISX0213.2000-1 14 k14-2000-1 k14-2000-1 k14-2000-1 k14-2000-1 \
JISX0213.2000-2 14 k14-2000-2 k14-2000-2 k14-2000-2 k14-2000-2 \
JISX0213.2000-1 16 jiskan16-2000-1 jiskan16-2000-1 jiskan16-2000-1 jiskan16-2000-1 \
JISX0213.2000-2 16 jiskan16-2000-2 jiskan16-2000-2 jiskan16-2000-2 jiskan16-2000-2 \
> fonts.alias
mkdir BDFS
for src in *.bdf; do
    bdftopcf $src | gzip -9 > ${src%.bdf}.pcf.gz && mv $src BDFS/
done
popd

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{ttfontdir}
install -d $RPM_BUILD_ROOT%{bmpfontdir}
install -d $RPM_BUILD_ROOT%{cidmapdir}

## ttfonts-ja
pushd VLGothic
install -m 0644 *.ttf $RPM_BUILD_ROOT%{ttfontdir}/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias
popd
#
#pushd %{kochisubst}
#install -m 0644 *.ttf $RPM_BUILD_ROOT%{ttfontdir}/
#if test -f $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias; then
#  cat $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias %{SOURCE6} > $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias.$$$ && mv $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias{.$$$,} || exit
#  chmod 0644 $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias
#else
#  install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{ttfontdir}/fonts.alias
#fi
#popd

## jisksp14
install -m 0644 jisksp14.pcf* $RPM_BUILD_ROOT%{bmpfontdir}/

## jisksp16-1990
install -m 0644 jisksp16-1990.pcf* $RPM_BUILD_ROOT%{bmpfontdir}/

## kappa20

## knm_new
for i in knmhn12x.bdf fonts/kaname-latin1.bdf fonts/knm12p.bdf fonts/knm12pb.bdf fonts/knmzn12x.bdf fonts/knmzn12xb.bdf; do
    bdftopcf $i | gzip -9 > $RPM_BUILD_ROOT%{bmpfontdir}/`basename $i | sed -e 's/.bdf/.pcf.gz/'`
done

## fonts-ja
### remove an unnecessary file
rm -f fonts-ja/mplus_cursors.pcf.gz
for i in fonts-ja/*.pcf.gz; do
    install -m 0644 $i $RPM_BUILD_ROOT%{bmpfontdir}/`basename $i`
done

# for ghostscript
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{cidmapdir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{cidmapdir}/

# for dummy
touch $RPM_BUILD_ROOT%{basefontdir}/fonts.cache-1
touch $RPM_BUILD_ROOT%{ttfontdir}/fonts.dir
touch $RPM_BUILD_ROOT%{ttfontdir}/fonts.scale
touch $RPM_BUILD_ROOT%{ttfontdir}/fonts.cache-1
touch $RPM_BUILD_ROOT%{bmpfontdir}/fonts.dir
touch $RPM_BUILD_ROOT%{bmpfontdir}/encodings.dir
touch $RPM_BUILD_ROOT%{bmpfontdir}/fonts.cache-1

install -m 0644 fonts-ja/fonts.alias $RPM_BUILD_ROOT%{bmpfontdir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
{
    umask 133
    touch %{ttfontdir} 2> /dev/null && {
	/usr/bin/ttmkfdir -d %{ttfontdir} -o %{ttfontdir}/fonts.scale
	mkfontdir %{ttfontdir}
    }
    fc-cache 2> /dev/null
}

%postun
{
    fc-cache 2> /dev/null
}

%files
%defattr(-, root, root)
#%doc %{sazanami}/doc
#%%doc %{kochisubst}/docs %{kochisubst}/{COPYING,README.ja,README.RedHat}
%doc doc.orig readme.kaname_bdf
%doc fonts-ja/COPYRIGHT* fonts-ja/README* fonts-ja/LICENSE* fonts-ja/ALLFONTS.txt
%dir %{basefontdir}
%dir %{ttfontdir}
%dir %{bmpfontdir}
%dir %{cidmapdir}
%config(noreplace) %verify(not md5 size mtime) %{ttfontdir}/fonts.alias
%config(noreplace) %verify(not md5 size mtime) %{bmpfontdir}/fonts.alias
%ghost %verify(not md5 size mtime) %{basefontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{ttfontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{ttfontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{ttfontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{bmpfontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{bmpfontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{bmpfontdir}/encodings.dir
%{ttfontdir}/*ttf
%{bmpfontdir}
%{cidmapdir}/FAPIcidfmap.ja
%{cidmapdir}/cidfmap.ja

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.20090710-4
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.20090710-3
- 为 Magic 3.0 重建

* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 0.20090710-2
- 为 Magic 3.0 重建

* Fri Feb 17 2007 Liu Di <liudidi@gmail.com> - 0.20061016-1mgc
- rebuild for Magic

* Wed Oct 18 2006 Akira TAGOH <tagoh@redhat.com> - 0.20061016-1
- correct U+7E6B. (#196433)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.20050222-11.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 17 2005 Warren Togami <wtogami@redhat.com> - 0.20050222-11
- split req(foo,bar) for erasure ordering

* Tue Nov 15 2005 Jeremy Katz <katzj@redhat.com> - 0.20050222-10
- better mkfontdir

* Mon Nov 14 2005 Warren Togami <wtogami@redhat.com> - 0.20050222-9
- rebuild against modular X

* Mon Nov  7 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-8
- rely on PATH to find mkfontdir instead of /usr/X11R6/bin hardcoded.
- replace Requires: mkfontdir instead of /usr/X11R6/bin/mkfontdir.

* Tue Aug 16 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-7
- Added cidfmap.ja for the latest ghostscript.
- Removed Kochi fonts.

* Tue Aug  2 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-6
- contain Sazanami fonts.

* Thu Jul 14 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-5
- use FAPIcidfmap instead of CIDFnmap for gs8.

* Thu Jun  9 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-4
- removed VFlib2 dependency.

* Wed Apr 20 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-3
- Updated the font path in CIDFnmap.ja (John Thacker, #155403)

* Thu Feb 24 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-2
- Use /usr/share/fonts/japanese instead of /usr/share/fonts/ja

* Tue Feb 22 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050222-1
- gets back Kochi font temporarily.

* Thu Feb 10 2005 Akira TAGOH <tagoh@redhat.com> - 0.20050210-1
- Initial release.
- integrated the below packages:
  - ttfonts-ja
  - jisksp14
  - jisksp16-1990
  - kappa20
  - knm_new
  - fonts-ja
- Update shinonome font to 0.9.11.
- Use Sazanami fonts instead of Kochi fonts.
