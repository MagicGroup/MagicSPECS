# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
BuildRequires: autoconf automake libtool m4
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%define tde_tdedocdir %{tde_docdir}/tde

# Builds all supported languages (not unsupported ones)
%if "%{?KDE_LANGS}" == ""
%define KDE_LANGS zh_CN zh_TW
%endif


Name:		trinity-i18n
Summary:	Internationalization support for Trinity
Version:	3.5.13.2
Release:	1%{?dist}%{?_variant}

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

Source0:	kde-i18n-trinity-%{version}.tar.xz

# TDE 3.5.12: Translate 'kdesu' message was modified in 'kdebase' package
Patch0:		kde-i18n-kdesu.patch

# TDE 3.5.12: Translate 'Open Terminal Here' desktop shortcut
Patch1:		trinity-kde-i18n-fr-openterminalhere.patch

# TDE 3.5.13: French translations for new features
Patch2:		kde-i18n-3.5.13-add_french_translations.patch

# TDE 3.5.13: Updated translations for zh_TW, thanks to Wei-Lun Chao !
Patch3:		kde-i18n-zh_TW-3.5.10.patch.gz

BuildRequires:	findutils
BuildRequires:	gettext
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1

%description
%{summary}.

%package Afrikaans
Summary: Afrikaans(af) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-af = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Afrikaans < %{version}-%{release}
Provides:	 trinity-kde-i18n-Afrikaans = %{version}-%{release}
%description Afrikaans
%{summary}.

%package Arabic 
Summary: Arabic(ar) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ar = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Arabic < %{version}-%{release}
Provides:	 trinity-kde-i18n-Arabic = %{version}-%{release}
%description Arabic
%{summary}.

%package Azerbaijani
Summary: Azerbaijani(az) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-az = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Arabic < %{version}-%{release}
Provides:	 trinity-kde-i18n-Arabic = %{version}-%{release}
%description Azerbaijani
%{summary}.

%package Belarusian
Summary: Belarusian(be) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-be = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Belarusian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Belarusian = %{version}-%{release}
%description Belarusian
%{summary}.

%package Bulgarian
Summary: Bulgarian(bg) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bg = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Bulgarian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Bulgarian = %{version}-%{release}
%description Bulgarian
%{summary}.

%package Bengali
Summary: Bengali(bn) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bn = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Bengali < %{version}-%{release}
Provides:	 trinity-kde-i18n-Bengali = %{version}-%{release}
%description Bengali
%{summary}.

%package Tibetan
Summary: Tibetan(bo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bo = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Tibetan < %{version}-%{release}
Provides:	 trinity-kde-i18n-Tibetan = %{version}-%{release}
%description Tibetan
%{summary}.

%package Breton
Summary: Breton(br) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-br = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Breton < %{version}-%{release}
Provides:	 trinity-kde-i18n-Breton = %{version}-%{release}
%description Breton
%{summary}.

%package Bosnian
Summary: Bosnian(bs) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-bs = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Bosnian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Bosnian = %{version}-%{release}
%description Bosnian
%{summary}.

%package Catalan
Summary: Catalan(ca) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ca = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Catalan < %{version}-%{release}
Provides:	 trinity-kde-i18n-Catalan = %{version}-%{release}
%description Catalan
%{summary}.

%package Czech
Summary: Czech(cs) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-cs = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Czech < %{version}-%{release}
Provides:	 trinity-kde-i18n-Czech = %{version}-%{release}
%description Czech
%{summary}.

%package Cymraeg
Summary: Cymraeg language support for TDE
Group: User Interface/Desktops
Obsoletes:	 trinity-kde-i18n-Cymraeg < %{version}-%{release}
Provides:	 trinity-kde-i18n-Cymraeg = %{version}-%{release}
%description Cymraeg
%{summary}.

%package Welsh
Summary: Welsh(cy) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-cy = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Welsh < %{version}-%{release}
Provides:	 trinity-kde-i18n-Welsh = %{version}-%{release}
%description Welsh
%{summary}.

%package Danish
Summary: Danish(da) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-da = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Danish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Danish = %{version}-%{release}
%description Danish
%{summary}.

%package German
Summary: German(de) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-de = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-German < %{version}-%{release}
Provides:	 trinity-kde-i18n-German = %{version}-%{release}
%description German
%{summary}.

%package Greek
Summary: Greek(el) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-el = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Greek < %{version}-%{release}
Provides:	 trinity-kde-i18n-Greek = %{version}-%{release}
%description Greek
%{summary}.

%package British
Summary: British(en_GB) English support for TDE
Group: User Interface/Desktops
Provides: %{name}-en_GB = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-British < %{version}-%{release}
Provides:	 trinity-kde-i18n-British = %{version}-%{release}
%description British
%{summary}.

%package Esperanto
Summary: Esperanto(eo) support for TDE
Group: User Interface/Desktops
Provides: %{name}-eo = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Esperanto < %{version}-%{release}
Provides:	 trinity-kde-i18n-Esperanto = %{version}-%{release}
%description Esperanto
%{summary}.

%package Spanish
Summary: Spanish(es) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-es = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Spanish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Spanish = %{version}-%{release}
%description Spanish
%{summary}.

%package Estonian
Summary: Estonian(et) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-et = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Estonian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Estonian = %{version}-%{release}
%description Estonian
%{summary}.

%package Basque
Summary: Basque(eu) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-eu = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Basque < %{version}-%{release}
Provides:	 trinity-kde-i18n-Basque = %{version}-%{release}
%description Basque
%{summary}.

%package Farsi
Summary: Farsi(fa) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fa = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Farsi < %{version}-%{release}
Provides:	 trinity-kde-i18n-Farsi = %{version}-%{release}
%description Farsi
%{summary}.

%package Finnish
Summary: Finnish(fi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fi = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Finnish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Finnish = %{version}-%{release}
%description Finnish
%{summary}.

%package Faroese
Summary: Faroese(fo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fo = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Faroese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Faroese = %{version}-%{release}
%description Faroese
%{summary}.

%package French
Summary: French(fr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fr = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-French < %{version}-%{release}
Provides:	 trinity-kde-i18n-French = %{version}-%{release}
%description French
%{summary}.

%package Frisian
Summary: Frisian(fy) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-fy = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Frisian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Frisian = %{version}-%{release}
%description Frisian
%{summary}.

%package Irish
Summary: Irish(ga) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ga = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Irish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Irish = %{version}-%{release}
%description Irish
%{summary}.

%package Galician
Summary: Galician(gl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-gl = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Galician < %{version}-%{release}
Provides:	 trinity-kde-i18n-Galician = %{version}-%{release}
%description Galician
%{summary}.

%package Hebrew
Summary: Hebrew(he) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-he = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Hebrew < %{version}-%{release}
Provides:	 trinity-kde-i18n-Hebrew = %{version}-%{release}
%description Hebrew
%{summary}.

%package Hindi
Summary: Hindi(hi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hi = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Hindi < %{version}-%{release}
Provides:	 trinity-kde-i18n-Hindi = %{version}-%{release}
%description Hindi
%{summary}.

%package Croatian
Summary: Croatian(hr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hr = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Croatian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Croatian = %{version}-%{release}
%description Croatian
%{summary}.

%package Hungarian
Summary: Hungarian(hu) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-hu = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Hungarian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Hungarian = %{version}-%{release}
%description Hungarian
%{summary}.

%package Indonesian
Summary: Indonesian(id) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-id = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Indonesian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Indonesian = %{version}-%{release}
%description Indonesian
%{summary}.

%package Icelandic
Summary: Icelandic(is) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-is = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Icelandic < %{version}-%{release}
Provides:	 trinity-kde-i18n-Icelandic = %{version}-%{release}
%description Icelandic
%{summary}.

%package Italian
Summary: Italian(it) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-it = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Italian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Italian = %{version}-%{release}
%description Italian
%{summary}.

%package Japanese
Summary: Japanese(ja) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ja = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Japanese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Japanese = %{version}-%{release}
%description Japanese
%{summary}.

%package Korean
Summary: Korean(ko) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ko = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Korean < %{version}-%{release}
Provides:	 trinity-kde-i18n-Korean = %{version}-%{release}
%description Korean
%{summary}.

%package Kurdish
Summary: Kurdish(ku) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ku = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Kurdish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Kurdish = %{version}-%{release}
%description Kurdish
%{summary}.

%package Lao
Summary: Lao(lo) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lo = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Lao < %{version}-%{release}
Provides:	 trinity-kde-i18n-Lao = %{version}-%{release}
%description Lao
%{summary}.

%package Lithuanian
Summary: Lithuanian(lt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lt = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Lithuanian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Lithuanian = %{version}-%{release}
%description Lithuanian
%{summary}.

%package Latvian
Summary: Latvian(lv) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-lv = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Latvian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Latvian = %{version}-%{release}
%description Latvian
%{summary}.

%package Maori
Summary: Maori(mi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mi = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Maori < %{version}-%{release}
Provides:	 trinity-kde-i18n-Maori = %{version}-%{release}
%description Maori
%{summary}.

%package Macedonian
Summary: Macedonian(mk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mk = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Macedonian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Macedonian = %{version}-%{release}
%description Macedonian
%{summary}.

%package Maltese
Summary: Maltese(mt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-mt = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Maltese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Maltese = %{version}-%{release}
%description Maltese
%{summary}.

%package Dutch
Summary: Dutch(nl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-nl = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Dutch < %{version}-%{release}
Provides:	 trinity-kde-i18n-Dutch = %{version}-%{release}
%description Dutch
%{summary}.

%package Norwegian
Summary: Norwegian(no) (Bokmaal) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-no = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Norwegian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Norwegian = %{version}-%{release}
%description Norwegian
%{summary}.

%package Norwegian-Nynorsk
Summary: Norwegian(nn) (Nynorsk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-nn = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Norwegian-Nynorsk < %{version}-%{release}
Provides:	 trinity-kde-i18n-Norwegian-Nynorsk = %{version}-%{release}
%description Norwegian-Nynorsk
%{summary}.

%package Occitan
Summary: Occitan(oc) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-oc = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Occitan < %{version}-%{release}
Provides:	 trinity-kde-i18n-Occitan = %{version}-%{release}
%description Occitan
%{summary}.

%package Polish
Summary: Polish(pl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pl = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Polish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Polish = %{version}-%{release}
%description Polish
%{summary}.

%package Portuguese
Summary: Portuguese(pt) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pt = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Portuguese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Portuguese = %{version}-%{release}
%description Portuguese
%{summary}.

%package Punjabi
Summary: Punjabi(pa) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pa = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Punjabi < %{version}-%{release}
Provides:	 trinity-kde-i18n-Punjabi = %{version}-%{release}
%description Punjabi
%{summary}.

%package Brazil
Summary: Brazil(pt_BR) Portuguese language support for TDE
Group: User Interface/Desktops
Provides: %{name}-pt_BR = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Brazil < %{version}-%{release}
Provides:	 trinity-kde-i18n-Brazil = %{version}-%{release}
%description Brazil
%{summary}.

%package Romanian
Summary: Romanian(ro) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ro = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Romanian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Romanian = %{version}-%{release}
%description Romanian
%{summary}.

%package Russian
Summary: Russian(ru) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ru = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Russian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Russian = %{version}-%{release}
%description Russian
%{summary}.

%package Slovak
Summary: Slovak(sk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sk = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Slovak < %{version}-%{release}
Provides:	 trinity-kde-i18n-Slovak = %{version}-%{release}
%description Slovak
%{summary}.

%package Slovenian
Summary: Slovenian(sl) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sl = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Slovenian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Slovenian = %{version}-%{release}
%description Slovenian
%{summary}.

%package Serbian
Summary: Serbian(sr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sr = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Serbian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Serbian = %{version}-%{release}
%description Serbian
%{summary}.

%package Swedish
Summary: Swedish(sv) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-sv = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Swedish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Swedish = %{version}-%{release}
%description Swedish
%{summary}.

%package Tamil
Summary: Tamil(ta) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ta = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Tamil < %{version}-%{release}
Provides:	 trinity-kde-i18n-Tamil = %{version}-%{release}
%description Tamil
%{summary}.

%package Tajik
Summary: Tajik(tg) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tg = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Tajik < %{version}-%{release}
Provides:	 trinity-kde-i18n-Tajik = %{version}-%{release}
%description Tajik
%{summary}.

%package Thai
Summary: Thai(th) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-th = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Thai < %{version}-%{release}
Provides:	 trinity-kde-i18n-Thai = %{version}-%{release}
%description Thai
%{summary}.

%package Turkish
Summary: Turkish(tr) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tr = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Turkish < %{version}-%{release}
Provides:	 trinity-kde-i18n-Turkish = %{version}-%{release}
%description Turkish
%{summary}.

%package Ukrainian
Summary: Ukrainian(uk) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-uk = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Ukrainian < %{version}-%{release}
Provides:	 trinity-kde-i18n-Ukrainian = %{version}-%{release}
%description Ukrainian
%{summary}.

%package Venda
Summary: Venda(ven) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-ven = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Venda < %{version}-%{release}
Provides:	 trinity-kde-i18n-Venda = %{version}-%{release}
%description Venda
%{summary}.

%package Vietnamese
Summary: Vietnamese(vi) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-vi = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Vietnamese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Vietnamese = %{version}-%{release}
%description Vietnamese
%{summary}.

%package Walloon
Summary: Walloon(wa) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-wa = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Walloon < %{version}-%{release}
Provides:	 trinity-kde-i18n-Walloon = %{version}-%{release}
%description Walloon
%{summary}.

%package Xhosa
Summary: Xhosa(xh) (a Bantu language) support for TDE
Group: User Interface/Desktops
Provides: %{name}-xh = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Xhosa < %{version}-%{release}
Provides:	 trinity-kde-i18n-Xhosa = %{version}-%{release}
%description Xhosa
%{summary}.

%package Chinese
Summary: Chinese(zh_CN) (Simplified Chinese) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-zh_CN = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Chinese < %{version}-%{release}
Provides:	 trinity-kde-i18n-Chinese = %{version}-%{release}
%description Chinese
%{summary}.

%package Chinese-Big5
Summary: Chinese(zh_TW) (Big5) language support for TDE
Group: User Interface/Desktops
Provides: %{name}-tz_TW = %{version}-%{release}
Obsoletes:	 trinity-kde-i18n-Chinese-Big5 < %{version}-%{release}
Provides:	 trinity-kde-i18n-Chinese-Big5 = %{version}-%{release}
%description Chinese-Big5
%{summary}.



%prep
%setup -q -n kde-i18n-trinity-%{version}

# Patches for Chinese (zh_TW) translations

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

export kde_htmldir="%{tde_tdedocdir}/HTML"

for l in %{KDE_LANGS}; do
  for f in tde-i18n-${l}/; do
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
  for f in tde-i18n-${l}/; do
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
find "%{buildroot}%{tde_tdedocdir}/HTML" -size 0 -exec rm -f {} \;

# See http://fedoraproject.org/wiki/Languages (???)
%__rm -f %{buildroot}%{tde_datadir}/locale/*/flag.png

# Removes conflict with KDE4
%if "%{?tde_prefix}" == "/usr"
%__rm -f %{buildroot}%{tde_datadir}/locale/*/entry.desktop
%endif

# remove obsolete KDE 3 application data translations
%__rm -rf "%{buildroot}%{tde_datadir}/apps"

%clean
%__rm -rf %{buildroot}

%if "%( grep -w af <<< '%{KDE_LANGS}' )" != ""
%files Afrikaans
%defattr(-,root,root,-)
%lang(af) %{tde_datadir}/locale/af/*
%lang(af) %{tde_tdedocdir}/HTML/af/
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
%endif

%if "%( grep -w cs <<< '%{KDE_LANGS}' )" != ""
%files Czech
%defattr(-,root,root,-)
%lang(cs) %{tde_datadir}/locale/cs/*
%lang(cs) %{tde_tdedocdir}/HTML/cs/
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
%lang(fi) %{tde_tdedocdir}/HTML/fi/
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
%lang(he) %{tde_tdedocdir}/HTML/he/
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
%lang(hr) %{tde_tdedocdir}/HTML/hr/
%endif

%if "%( grep -w hu <<< '%{KDE_LANGS}' )" != ""
%files Hungarian
%defattr(-,root,root,-)
%lang(hu) %{tde_datadir}/locale/hu/*
%lang(hu) %{tde_tdedocdir}/HTML/hu/
%endif

%if "%( grep -w id <<< '%{KDE_LANGS}' )" != ""
%files Indonesian
%defattr(-,root,root,-)
%lang(id) %{tde_datadir}/locale/id/*
%lang(id) %{tde_tdedocdir}/HTML/id/
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
%endif

%if "%( grep -w ja <<< '%{KDE_LANGS}' )" != ""
%files Japanese
%defattr(-,root,root,-)
%lang(ja) %{tde_datadir}/locale/ja/*
%lang(ja) %{tde_tdedocdir}/HTML/ja/
%endif

%if "%( grep -w ko <<< '%{KDE_LANGS}' )" != ""
%files Korean
%defattr(-,root,root,-)
%lang(ko) %{tde_datadir}/locale/ko/*
%lang(ko) %{tde_tdedocdir}/HTML/ko/
%endif

%if "%( grep -w ku <<< '%{KDE_LANGS}' )" != ""
%files Kurdish
%defattr(-,root,root,-)
%lang(ku) %{tde_datadir}/locale/ku/*
%lang(ku) %{tde_tdedocdir}/HTML/ku/
%endif

%if "%( grep -w lao <<< '%{KDE_LANGS}' )" != ""
%files Lao
%defattr(-,root,root,-)
%lang(lo) %{tde_datadir}/locale/lo/*
%lang(lo) %{tde_tdedocdir}/HTML/lo/
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

%if "%( grep -w mt <<< '%{KDE_LANGS}' )" != ""
%files Maltese
%defattr(-,root,root,-)
%lang(mt) %{tde_datadir}/locale/mt/*
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
#%lang(nb) %{tde_tdedocdir}/HTML/nb/
%endif

%if "%( grep -w nn <<< '%{KDE_LANGS}' )" != ""
%files Norwegian-Nynorsk
%defattr(-,root,root,-)
%lang(nn) %{tde_datadir}/locale/nn/*
#%lang(nn) %{tde_tdedocdir}/HTML/nn/
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
%lang(pl) %{tde_tdedocdir}/HTML/pl/
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
%lang(ro) %{tde_tdedocdir}/HTML/ro/
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
%lang(sr) %{tde_tdedocdir}/HTML/sr/
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
%lang(tr) %{tde_tdedocdir}/HTML/tr/
%endif

%if "%( grep -w uk <<< '%{KDE_LANGS}' )" != ""
%files Ukrainian
%defattr(-,root,root,-)
%lang(uk) %{tde_tdedocdir}/HTML/uk/
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
%lang(xh) %{tde_tdedocdir}/HTML/xh/
%endif

%if "%( grep -w zh_CN <<< '%{KDE_LANGS}' )" != ""
%files Chinese
%defattr(-,root,root,-)
%lang(zh_CN) %{tde_datadir}/locale/zh_CN/*
%lang(zh_CN) %{tde_tdedocdir}/HTML/zh_CN/
%endif

%if "%( grep -w zh_TW <<< '%{KDE_LANGS}' )" != ""
%files Chinese-Big5
%defattr(-,root,root,-)
%lang(zh_TW) %{tde_datadir}/locale/zh_TW/*
%lang(zh_TW) %{tde_tdedocdir}/HTML/zh_TW/
%endif

%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1

* Wed Aug 15 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-7
- Renames to 'trinity-i18n'
- Updates 'zh_TW' translations

* Sun Dec 18 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-6
- Updates French translations (mostly Kickoff Menu related)

* Sun Dec 04 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-5
- Removes 'kde-filesystem" dependancy

* Fri Nov 26 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-4
- Fix HTML directory location

* Fri Nov 11 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-3
- Re-adds missing files 'entry.desktop'
- Updates zh_TW translation, thanks to Wei-Lun Chao

* Tue Nov 01 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-2
- Add missing french translations for TDE 3.5.13

* Sun Oct 30 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-1
- Initial release for RHEL 6, RHEL 5 and Fedora 15

* Sun Dec 19 2010 Francois Andriot <francois.andriot@free.fr> - 3.5.13-0
- Initial version (French language only)
- Based on RHEL SPEC file 'kde-i18n'
- Add 'patch0' to reflect modifications in 'kdesu' from 'kdebase' package
- Import to GIT
