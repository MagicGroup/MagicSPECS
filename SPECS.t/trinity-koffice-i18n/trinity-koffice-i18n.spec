# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

%define tdeversion 3.5.13.2

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

# Builds all supported languages (not unsupported ones)
%if "%{?KDE_LANGS}" == ""
%define KDE_LANGS zh_CN zh_TW
%endif


Name:		trinity-koffice-i18n
Summary:	Internationalization support for Trinity
Version:	1.6.3
Release:	3%{?dist}%{?_variant}

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# GFDL, with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
License:	GFDL
Group:		User Interface/Desktops
BuildArch:	noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Source0:	koffice-i18n-trinity-%{tdeversion}.tar.xz

BuildRequires:	findutils
BuildRequires:	gettext
BuildRequires:	autoconf automake libtool m4
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1

%description
%{summary}.

%package Bulgarian
Summary: Bulgarian(bg) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bg = %{version}-%{release}
%description Bulgarian
%{summary}.

%package Bengali
Summary: Bengali(bn) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bn = %{version}-%{release}
%description Bengali
%{summary}.

%package Tibetan
Summary: Tibetan(bo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bo = %{version}-%{release}
%description Tibetan
%{summary}.

%package Breton
Summary: Breton(br) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-br = %{version}-%{release}
%description Breton
%{summary}.

%package Bosnian
Summary: Bosnian(bs) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bs = %{version}-%{release}
%description Bosnian
%{summary}.

%package Catalan
Summary: Catalan(ca) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ca = %{version}-%{release}
%description Catalan
%{summary}.

%package Czech
Summary: Czech(cs) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-cs = %{version}-%{release}
%description Czech
%{summary}.

%package Cymraeg
Summary: Cymraeg language support for TDE
Group: User Interface/Desktops
%description Cymraeg
%{summary}.

%package Welsh
Summary: Welsh(cy) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-cy = %{version}-%{release}
%description Welsh
%{summary}.

%package Danish
Summary: Danish(da) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-da = %{version}-%{release}
%description Danish
%{summary}.

%package German
Summary: German(de) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-de = %{version}-%{release}
%description German
%{summary}.

%package Greek
Summary: Greek(el) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-el = %{version}-%{release}
%description Greek
%{summary}.

%package British
Summary: British(en_GB) English support for TDE
Group: User Interface/Desktops
Provides: %{name}-en_GB = %{version}-%{release}
%description British
%{summary}.

%package Esperanto
Summary: Esperanto(eo) support for TDE
Group: User Interface/Desktops
Provides: %{name}-eo = %{version}-%{release}
%description Esperanto
%{summary}.

%package Spanish
Summary: Spanish(es) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-es = %{version}-%{release}
%description Spanish
%{summary}.

%package Estonian
Summary: Estonian(et) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-et = %{version}-%{release}
%description Estonian
%{summary}.

%package Basque
Summary: Basque(eu) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-eu = %{version}-%{release}
%description Basque
%{summary}.

%package Finnish
Summary: Finnish(fi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fi = %{version}-%{release}
%description Finnish
%{summary}.

%package Faroese
Summary: Faroese(fo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fo = %{version}-%{release}
%description Faroese
%{summary}.

%package French
Summary: French(fr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fr = %{version}-%{release}
%description French
%{summary}.

%package Frisian
Summary: Frisian(fy) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fy = %{version}-%{release}
%description Frisian
%{summary}.

%package Irish
Summary: Irish(ga) language support for TDE
Group: User Interface/Desktops
Obsoletes: kde-i18n-Gaeilge < %{version}
Provides: %{name}-ga = %{version}-%{release}
%description Irish
%{summary}.

%package Galician
Summary: Galician(gl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-gl = %{version}-%{release}
%description Galician
%{summary}.

%package Hebrew
Summary: Hebrew(he) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-he = %{version}-%{release}
%description Hebrew
%{summary}.

%package Hindi
Summary: Hindi(hi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hi = %{version}-%{release}
%description Hindi
%{summary}.

%package Croatian
Summary: Croatian(hr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hr = %{version}-%{release}
%description Croatian
%{summary}.

%package Hungarian
Summary: Hungarian(hu) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hu = %{version}-%{release}
%description Hungarian
%{summary}.

%package Indonesian
Summary: Indonesian(id) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-id = %{version}-%{release}
%description Indonesian
%{summary}.

%package Icelandic
Summary: Icelandic(is) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-is = %{version}-%{release}
%description Icelandic
%{summary}.

%package Italian
Summary: Italian(it) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-it = %{version}-%{release}
%description Italian
%{summary}.

%package Japanese
Summary: Japanese(ja) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ja = %{version}-%{release}
%description Japanese
%{summary}.

%package Khmer
Summary: Khmer(km) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-km = %{version}-%{release}
%description Khmer
%{summary}.

%package Korean
Summary: Korean(ko) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ko = %{version}-%{release}
%description Korean
%{summary}.

%package Kurdish
Summary: Kurdish(ku) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ku = %{version}-%{release}
%description Kurdish
%{summary}.

%package Lao
Summary: Lao(lo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lo = %{version}-%{release}
%description Lao
%{summary}.

%package Lithuanian
Summary: Lithuanian(lt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lt = %{version}-%{release}
%description Lithuanian
%{summary}.

%package Latvian
Summary: Latvian(lv) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lv = %{version}-%{release}
%description Latvian
%{summary}.

%package Maori
Summary: Maori(mi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mi = %{version}-%{release}
%description Maori
%{summary}.

%package Macedonian
Summary: Macedonian(mk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mk = %{version}-%{release}
%description Macedonian
%{summary}.

%package Malay
Summary: Malay(ms) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ms = %{version}-%{release}
%description Malay
%{summary}.

%package Maltese
Summary: Maltese(mt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mt = %{version}-%{release}
%description Maltese
%{summary}.

%package LowSaxon
Summary: Low Saxon (nds) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-nds = %{version}-%{release}
%description LowSaxon
%{summary}.

%package Nepali
Summary: Nepali(ne) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ne = %{version}-%{release}
%description Nepali
%{summary}.

%package Dutch
Summary: Dutch(nl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-nl = %{version}-%{release}
%description Dutch
%{summary}.

%package Norwegian
Summary: Norwegian(no) (Bokmaal) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-no = %{version}-%{release}
%description Norwegian
%{summary}.

%package Norwegian-Nynorsk
Summary: Norwegian(nn) (Nynorsk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-nn = %{version}-%{release}
%description Norwegian-Nynorsk
%{summary}.

%package Occitan
Summary: Occitan(oc) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-oc = %{version}-%{release}
%description Occitan
%{summary}.

%package Polish
Summary: Polish(pl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pl = %{version}-%{release}
%description Polish
%{summary}.

%package Portuguese
Summary: Portuguese(pt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pt = %{version}-%{release}
%description Portuguese
%{summary}.

%package Punjabi
Summary: Punjabi(pa) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pa = %{version}-%{release}
%description Punjabi
%{summary}.

%package Brazil
Summary: Brazil(pt_BR) Portuguese language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pt_BR = %{version}-%{release}
%description Brazil
%{summary}.

%package Romanian
Summary: Romanian(ro) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ro = %{version}-%{release}
%description Romanian
%{summary}.

%package Russian
Summary: Russian(ru) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ru = %{version}-%{release}
%description Russian
%{summary}.

%package Slovak
Summary: Slovak(sk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sk = %{version}-%{release}
%description Slovak
%{summary}.

%package Slovenian
Summary: Slovenian(sl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sl = %{version}-%{release}
%description Slovenian
%{summary}.

%package Serbian
Summary: Serbian(sr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sr = %{version}-%{release}
%description Serbian
%{summary}.

%package Swedish
Summary: Swedish(sv) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sv = %{version}-%{release}
%description Swedish
%{summary}.

%package Tamil
Summary: Tamil(ta) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ta = %{version}-%{release}
%description Tamil
%{summary}.

%package Tajik
Summary: Tajik(tg) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tg = %{version}-%{release}
%description Tajik
%{summary}.

%package Thai
Summary: Thai(th) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-th = %{version}-%{release}
%description Thai
%{summary}.

%package Turkish
Summary: Turkish(tr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tr = %{version}-%{release}
%description Turkish
%{summary}.

%package Ukrainian
Summary: Ukrainian(uk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-uk = %{version}-%{release}
%description Ukrainian
%{summary}.

%package Venda
Summary: Venda(ven) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ven = %{version}-%{release}
%description Venda
%{summary}.

%package Vietnamese
Summary: Vietnamese(vi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-vi = %{version}-%{release}
%description Vietnamese
%{summary}.

%package Walloon
Summary: Walloon(wa) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-wa = %{version}-%{release}
%description Walloon
%{summary}.

%package Xhosa
Summary: Xhosa(xh) (a Bantu language) support for TDE
Group: User Interface/Desktops
Provides: %{name}-xh = %{version}-%{release}
%description Xhosa
%{summary}.

%package Chinese
Summary: Chinese(zh_CN) (Simplified Chinese) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-zh_CN = %{version}-%{release}
%description Chinese
%{summary}.

%package Chinese-Big5
Summary: Chinese(zh_TW) (Big5) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tz_TW = %{version}-%{release}
%description Chinese-Big5
%{summary}.



%prep
%setup -q -n koffice-i18n-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"


%build
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

export kde_htmldir="%{tde_tdedocdir}/HTML"

for l in %{KDE_LANGS}; do
  for f in koffice-i18n-${l}/; do
    if [ -d "${f}" ]; then 
      pushd ${f}
      autoreconf -fiv
      %__make -f ../admin/Makefile.common
      %configure \
        --prefix=%{tde_prefix} \
        --datadir=%{tde_datadir} \
        --docdir=%{tde_tdedocdir}
      %__make %{?_smp_mflags}
      popd
    fi
  done
done

%install
%__rm -rf %{?buildroot}
export PATH="%{tde_bindir}:${PATH}"

for l in %{KDE_LANGS}; do
  for f in koffice-i18n-${l}/; do
    if [ -d "${f}" ] && [ -r "${f}/Makefile" ] ; then 
      %__make install DESTDIR="%{?buildroot}" -C "${f}"
    fi
  done
done

# make symlinks relative
%if "%{tde_prefix}" == "/usr"
pushd "%{buildroot}%{tde_tdedocdir}/HTML"
for lang in *; do
  if [ -d "$lang" ]; then
    pushd "$lang"
    for i in */*/*; do
      if [ -d $i -a -L $i/common ]; then
        rm -f $i/common
        ln -sf ../../../docs/common $i
      fi
    done

    for i in */*; do
      if [ -d $i -a -L $i/common ]; then
        rm -f $i/common
        ln -sf ../../docs/common $i
      fi
    done

    for i in *; do
      if [ -d $i -a -L $i/common ]; then
        rm -f $i/common
        ln -sf ../docs/common $i
      fi
    done

    popd
  fi
done
popd   
%endif

# remove zero-length file
# find "%{buildroot}%{tde_tdedocdir}/HTML" -size 0 -exec rm -f {} \;

%clean
%__rm -rf %{buildroot}

%if "%( grep -w af <<< '%{KDE_LANGS}' )" != ""
%files Afrikaans
%defattr(-,root,root,-)
%lang(af) %{tde_datadir}/locale/af/*
%endif

%if "%( grep -w ar <<< '%{KDE_LANGS}' )" != ""
%files Arabic 
%defattr(-,root,root,-)
%lang(ar) %{tde_datadir}/locale/ar/*
%endif

%if "%( grep -w az <<< '%{KDE_LANGS}' )" != ""
%files Azerbaijani
%defattr(-,root,root,-)
%lang(az) %{tde_datadir}/locale/az/*
%endif

%if "%( grep -w be <<< '%{KDE_LANGS}' )" != ""
%files Belarusian
%defattr(-,root,root,-)
%lang(be) %{tde_datadir}/locale/be/*
%endif

%if "%( grep -w bg <<< '%{KDE_LANGS}' )" != ""
%files Bulgarian
%defattr(-,root,root,-)
%lang(bg) %{tde_datadir}/locale/bg/*
%endif

%if "%( grep -w bn <<< '%{KDE_LANGS}' )" != ""
%files Bengali
%defattr(-,root,root,-)
%lang(bn) %{tde_datadir}/locale/bn/*
%endif

%if "%( grep -w bo <<< '%{KDE_LANGS}' )" != ""
%files Tibetan
%defattr(-,root,root,-)
%lang(bo) %{tde_datadir}/locale/bo/*
%endif

%if "%( grep -w br <<< '%{KDE_LANGS}' )" != ""
%files Breton
%defattr(-,root,root,-)
%lang(br) %{tde_datadir}/locale/br/*
%endif

%if "%( grep -w bs <<< '%{KDE_LANGS}' )" != ""
%files Bosnian
%defattr(-,root,root,-)
%lang(bs) %{tde_datadir}/locale/bs/*
%endif

%if "%( grep -w ca <<< '%{KDE_LANGS}' )" != ""
%files Catalan
%defattr(-,root,root,-)
%lang(ca) %{tde_datadir}/locale/ca/*
%lang(ca) %{tde_tdedocdir}/HTML/ca/
%lang(ca) %{tde_datadir}/apps/koffice/autocorrect/ca.xml
%endif

%if "%( grep -w cs <<< '%{KDE_LANGS}' )" != ""
%files Czech
%defattr(-,root,root,-)
%lang(cs) %{tde_datadir}/locale/cs/*
%lang(cs) %{tde_datadir}/apps/koffice/autocorrect/cs.xml
%endif

%if "%( grep -w cy <<< '%{KDE_LANGS}' )" != ""
%files Welsh
%defattr(-,root,root,-)
%lang(cy) %{tde_datadir}/locale/cy/*
%endif

%if "%( grep -w da <<< '%{KDE_LANGS}' )" != ""
%files Danish
%defattr(-,root,root,-)
%lang(da) %{tde_datadir}/locale/da/*
%lang(da) %{tde_tdedocdir}/HTML/da/
%endif

%if "%( grep -w de <<< '%{KDE_LANGS}' )" != ""
%files German
%defattr(-,root,root,-)
%lang(de) %{tde_datadir}/locale/de/*
%lang(de) %{tde_tdedocdir}/HTML/de/
%lang(de) %{tde_datadir}/apps/koffice/autocorrect/de.xml
%endif

%if "%( grep -w el <<< '%{KDE_LANGS}' )" != ""
%files Greek
%defattr(-,root,root,-)
%lang(el) %{tde_datadir}/locale/el/*
%endif

%if "%( grep -w en_GB <<< '%{KDE_LANGS}' )" != ""
%files British
%defattr(-,root,root,-)
%lang(en_GB) %{tde_datadir}/locale/en_GB/*
%lang(en_GB) %{tde_tdedocdir}/HTML/en_GB/
%endif

%if "%( grep -w eo <<< '%{KDE_LANGS}' )" != ""
%files Esperanto
%defattr(-,root,root,-)
%lang(eo) %{tde_datadir}/locale/eo/*
%endif

%if "%( grep -w es <<< '%{KDE_LANGS}' )" != ""
%files Spanish
%defattr(-,root,root,-)
%lang(es) %{tde_datadir}/locale/es/*
%lang(es) %{tde_tdedocdir}/HTML/es/
%lang(es) %{tde_datadir}/apps/koffice/autocorrect/es.xml
%endif

%if "%( grep -w et <<< '%{KDE_LANGS}' )" != ""
%files Estonian
%defattr(-,root,root,-)
%lang(et) %{tde_datadir}/locale/et/*
%lang(et) %{tde_tdedocdir}/HTML/et/
%endif

%if "%( grep -w eu <<< '%{KDE_LANGS}' )" != ""
%files Basque
%defattr(-,root,root,-)
%lang(eu) %{tde_datadir}/locale/eu/*
%endif

%if "%( grep -w fa <<< '%{KDE_LANGS}' )" != ""
%files Farsi
%defattr(-,root,root,-)
%lang(fa) %{tde_datadir}/locale/fa/*
%endif

%if "%( grep -w fi <<< '%{KDE_LANGS}' )" != ""
%files Finnish
%defattr(-,root,root,-)
%lang(fi) %{tde_datadir}/locale/fi/*
%endif

%if "%( grep -w fo <<< '%{KDE_LANGS}' )" != ""
%files Faroese
%defattr(-,root,root,-)
%lang(fo) %{tde_datadir}/locale/fo/*
%endif

%if "%( grep -w fr <<< '%{KDE_LANGS}' )" != ""
%files French
%defattr(-,root,root,-)
%lang(fr) %{tde_datadir}/locale/fr/*
%lang(fr) %{tde_tdedocdir}/HTML/fr/
%lang(fr) %{tde_datadir}/apps/koffice/autocorrect/fr.xml
%endif

%if "%( grep -w fy <<< '%{KDE_LANGS}' )" != ""
%files Frisian
%defattr(-,root,root,-)
%lang(fy) %{tde_datadir}/locale/fy/*
%endif

%if "%( grep -w ga <<< '%{KDE_LANGS}' )" != ""
%files Irish
%defattr(-,root,root,-)
%lang(ga) %{tde_datadir}/locale/ga/*
%endif

%if "%( grep -w gl <<< '%{KDE_LANGS}' )" != ""
%files Galician
%defattr(-,root,root,-)
%lang(gl) %{tde_datadir}/locale/gl/*
%endif

%if "%( grep -w he <<< '%{KDE_LANGS}' )" != ""
%files Hebrew
%defattr(-,root,root,-)
%lang(he) %{tde_datadir}/locale/he/*
%endif

%if "%( grep -w hi <<< '%{KDE_LANGS}' )" != ""
%files Hindi
%defattr(-,root,root,-)
%lang(hi) %{tde_datadir}/locale/hi/*
%endif

%if "%( grep -w hr <<< '%{KDE_LANGS}' )" != ""
%files Croatian
%defattr(-,root,root,-)
%lang(hr) %{tde_datadir}/locale/hr/*
%endif

%if "%( grep -w hu <<< '%{KDE_LANGS}' )" != ""
%files Hungarian
%defattr(-,root,root,-)
%lang(hu) %{tde_datadir}/locale/hu/*
%lang(hu) %{tde_datadir}/apps/koffice/autocorrect/hu.xml
%endif

%if "%( grep -w id <<< '%{KDE_LANGS}' )" != ""
%files Indonesian
%defattr(-,root,root,-)
%lang(id) %{tde_datadir}/locale/id/*
%endif

%if "%( grep -w is <<< '%{KDE_LANGS}' )" != ""
%files Icelandic
%defattr(-,root,root,-)
%lang(is) %{tde_datadir}/locale/is/*
%endif

%if "%( grep -w it <<< '%{KDE_LANGS}' )" != ""
%files Italian
%defattr(-,root,root,-)
%lang(it) %{tde_datadir}/locale/it/*
%lang(it) %{tde_tdedocdir}/HTML/it/
%lang(it) %{tde_datadir}/apps/koffice/autocorrect/it.xml
%endif

%if "%( grep -w ja <<< '%{KDE_LANGS}' )" != ""
%files Japanese
%defattr(-,root,root,-)
%lang(ja) %{tde_datadir}/locale/ja/*
%endif

%if "%( grep -w km <<< '%{KDE_LANGS}' )" != ""
%files Khmer
%defattr(-,root,root,-)
%lang(km) %{tde_datadir}/locale/km/*
%endif

%if "%( grep -w ko <<< '%{KDE_LANGS}' )" != ""
%files Korean
%defattr(-,root,root,-)
%lang(ko) %{tde_datadir}/locale/ko/*
%endif

%if "%( grep -w ku <<< '%{KDE_LANGS}' )" != ""
%files Kurdish
%defattr(-,root,root,-)
%lang(ku) %{tde_datadir}/locale/ku/*
%endif

%if "%( grep -w lao <<< '%{KDE_LANGS}' )" != ""
%files Lao
%defattr(-,root,root,-)
%lang(lo) %{tde_datadir}/locale/lo/*
%endif

%if "%( grep -w lt <<< '%{KDE_LANGS}' )" != ""
%files Lithuanian
%defattr(-,root,root,-)
%lang(lt) %{tde_datadir}/locale/lt/*
%endif

%if "%( grep -w lv <<< '%{KDE_LANGS}' )" != ""
%files Latvian
%defattr(-,root,root,-)
%lang(lv) %{tde_datadir}/locale/lv/*
%endif

%if "%( grep -w mi <<< '%{KDE_LANGS}' )" != ""
%files Maori
%defattr(-,root,root,-)
%lang(mi) %{tde_datadir}/locale/mi/*
%endif

%if "%( grep -w mk <<< '%{KDE_LANGS}' )" != ""
%files Macedonian
%defattr(-,root,root,-)
%lang(mk) %{tde_datadir}/locale/mk/*
%endif

%if "%( grep -w ms <<< '%{KDE_LANGS}' )" != ""
%files Malay
%defattr(-,root,root,-)
%lang(ms) %{tde_datadir}/locale/ms/*
%endif

%if "%( grep -w mt <<< '%{KDE_LANGS}' )" != ""
%files Maltese
%defattr(-,root,root,-)
%lang(mt) %{tde_datadir}/locale/mt/*
%endif

%if "%( grep -w nds <<< '%{KDE_LANGS}' )" != ""
%files LowSaxon
%defattr(-,root,root,-)
%lang(nds) %{tde_datadir}/locale/nds/*
%endif

%if "%( grep -w ne <<< '%{KDE_LANGS}' )" != ""
%files Nepali
%defattr(-,root,root,-)
%lang(ne) %{tde_datadir}/locale/ne/*
%endif

%if "%( grep -w nl <<< '%{KDE_LANGS}' )" != ""
%files Dutch
%defattr(-,root,root,-)
%lang(nl) %{tde_datadir}/locale/nl/*
%lang(nl) %{tde_tdedocdir}/HTML/nl/
%endif

%if "%( grep -w nb <<< '%{KDE_LANGS}' )" != ""
%files Norwegian
%defattr(-,root,root,-)
%lang(nb) %{tde_datadir}/locale/nb/*
%endif

%if "%( grep -w nn <<< '%{KDE_LANGS}' )" != ""
%files Norwegian-Nynorsk
%defattr(-,root,root,-)
%lang(nn) %{tde_datadir}/locale/nn/*
%endif

%if "%( grep -w oc <<< '%{KDE_LANGS}' )" != ""
%files Occitan
%defattr(-,root,root,-)
%lang(oc) %{tde_datadir}/locale/oc/*
%endif

%if "%( grep -w pa <<< '%{KDE_LANGS}' )" != ""
%files Punjabi
%defattr(-,root,root,-)
%lang(pa) %{tde_datadir}/locale/pa/*
%endif

%if "%( grep -w pl <<< '%{KDE_LANGS}' )" != ""
%files Polish
%defattr(-,root,root,-)
%lang(pl) %{tde_datadir}/locale/pl/*
%endif

%if "%( grep -w pt <<< '%{KDE_LANGS}' )" != ""
%files Portuguese
%defattr(-,root,root,-)
%lang(pt) %{tde_datadir}/locale/pt/*
%lang(pt) %{tde_tdedocdir}/HTML/pt/
%endif

%if "%( grep -w pt_BR <<< '%{KDE_LANGS}' )" != ""
%files Brazil
%defattr(-,root,root,-)
%lang(pt_BR) %{tde_datadir}/locale/pt_BR/*
%lang(pt_BR) %{tde_tdedocdir}/HTML/pt_BR/
%endif

%if "%( grep -w ro <<< '%{KDE_LANGS}' )" != ""
%files Romanian
%defattr(-,root,root,-)
%lang(ro) %{tde_datadir}/locale/ro/*
%endif

%if "%( grep -w ru <<< '%{KDE_LANGS}' )" != ""
%files Russian
%defattr(-,root,root,-)
%lang(ru) %{tde_datadir}/locale/ru/*
%lang(ru) %{tde_tdedocdir}/HTML/ru/
%endif

%if "%( grep -w sk <<< '%{KDE_LANGS}' )" != ""
%files Slovak
%defattr(-,root,root,-)
%lang(sk) %{tde_datadir}/locale/sk/*
%lang(sk) %{tde_tdedocdir}/HTML/sk/
%lang(sk) %{tde_datadir}/apps/koffice/autocorrect/sk.xml
%endif

%if "%( grep -w sl <<< '%{KDE_LANGS}' )" != ""
%files Slovenian
%defattr(-,root,root,-)
%lang(sl) %{tde_datadir}/locale/sl/*
%lang(sl) %{tde_tdedocdir}/HTML/sl/
%endif

%if "%( grep -w sr <<< '%{KDE_LANGS}' )" != ""
%files Serbian
%defattr(-,root,root,-)
%lang(sr) %{tde_datadir}/locale/sr/*
%endif

%if "%( grep -w sv <<< '%{KDE_LANGS}' )" != ""
%files Swedish
%defattr(-,root,root,-)
%lang(sv) %{tde_datadir}/locale/sv/*
%lang(sv) %{tde_tdedocdir}/HTML/sv/
%endif

%if "%( grep -w ta <<< '%{KDE_LANGS}' )" != ""
%files Tamil
%defattr(-,root,root,-)
%lang(ta) %{tde_datadir}/locale/ta/*
%endif

%if "%( grep -w tg <<< '%{KDE_LANGS}' )" != ""
%files Tajik
%defattr(-,root,root,-)
%lang(tg) %{tde_datadir}/locale/tg/*
%endif

%if "%( grep -w th <<< '%{KDE_LANGS}' )" != ""
%files Thai
%defattr(-,root,root,-)
%lang(th) %{tde_datadir}/locale/th/*
%endif

%if "%( grep -w tr <<< '%{KDE_LANGS}' )" != ""
%files Turkish
%defattr(-,root,root,-)
%lang(tr) %{tde_datadir}/locale/tr/*
%endif

%if "%( grep -w uk <<< '%{KDE_LANGS}' )" != ""
%files Ukrainian
%defattr(-,root,root,-)
%lang(uk) %{tde_datadir}/locale/uk/*
%endif

%if "%( grep -w ven <<< '%{KDE_LANGS}' )" != ""
%files Venda
%defattr(-,root,root,-)
%lang(ven) %{tde_datadir}/locale/ven/*
%endif

%if "%( grep -w vi <<< '%{KDE_LANGS}' )" != ""
%files Vietnamese
%defattr(-,root,root,-)
%lang(vi) %{tde_datadir}/locale/vi/*
%endif

%if "%( grep -w wa <<< '%{KDE_LANGS}' )" != ""
%files Walloon
%defattr(-,root,root,-)
%lang(wa) %{tde_datadir}/locale/wa/*
%endif

%if "%( grep -w xh <<< '%{KDE_LANGS}' )" != ""
%files Xhosa
%defattr(-,root,root,-)
%lang(xh) %{tde_datadir}/locale/xh/*
%endif

%if "%( grep -w zh_CN <<< '%{KDE_LANGS}' )" != ""
%files Chinese
%defattr(-,root,root,-)
%lang(zh_CN) %{tde_datadir}/locale/zh_CN/*
%endif

%if "%( grep -w zh_TW <<< '%{KDE_LANGS}' )" != ""
%files Chinese-Big5
%defattr(-,root,root,-)
%lang(zh_TW) %{tde_datadir}/locale/zh_TW/*
%endif

%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 1.6.3-3.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.6.3-2
- Initial build for TDE 3.5.13.1

* Sun Jul 01 2012 Francois Andriot <francois.andriot@free.fr> - 1.6.3-1
- Initial build for TDE 3.5.13

