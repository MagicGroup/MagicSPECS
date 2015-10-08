#
# spec file for package tde-i18n (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.0
%endif
%define tde_pkg tde-i18n
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# Builds all supported languages (not unsupported ones)
%if "%{?TDE_LANGS}" == ""
%define TDE_LANGS af ar az be bg bn br bs ca cs csb cy da de el en_GB eo es et eu fa fi fr fy ga gl he hi hr hu is it ja kk km ko lt lv mk mn ms nb nds nl nn pa pl pt pt_BR ro ru rw se sk sl sr sr@Latn ss sv ta te tg th tr uk uz uz@cyrillic vi wa zh_CN zh_TW
%endif


Name:			trinity-%{tde_pkg}
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Internationalization support for Trinity
Group:			User Interface/Desktops
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch

# Speed build options
%define debug_package %{nil}
%define __spec_install_post %{nil}
AutoReq: no

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	findutils
BuildRequires:	gettext
BuildRequires:	cmake
BuildRequires:	gcc-c++

%description
This package contains %{summary}.

##########

%package Afrikaans
Summary:		Afrikaans(af) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-af = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Afrikaans < %{version}-%{release}
Provides:		trinity-kde-i18n-Afrikaans = %{version}-%{release}

%description Afrikaans
This package contains %{summary}.

%files Afrikaans
%defattr(-,root,root,-)
%{tde_datadir}/locale/af/

##########

%package Arabic 
Summary:		Arabic(ar) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ar = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Arabic < %{version}-%{release}
Provides:		trinity-kde-i18n-Arabic = %{version}-%{release}

%description Arabic
This package contains %{summary}.

%files Arabic 
%defattr(-,root,root,-)
%{tde_datadir}/locale/ar/

##########

%package Azerbaijani
Summary:		Azerbaijani(az) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-az = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Arabic < %{version}-%{release}
Provides:		trinity-kde-i18n-Arabic = %{version}-%{release}

%description Azerbaijani
This package contains %{summary}.

%files Azerbaijani
%defattr(-,root,root,-)
%{tde_datadir}/locale/az/

##########

%package Belarusian
Summary:		Belarusian(be) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-be = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Belarusian < %{version}-%{release}
Provides:		trinity-kde-i18n-Belarusian = %{version}-%{release}

%description Belarusian
This package contains %{summary}.

%files Belarusian
%defattr(-,root,root,-)
%{tde_datadir}/locale/be/

##########

%package Bulgarian
Summary:		Bulgarian(bg) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-bg = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Bulgarian < %{version}-%{release}
Provides:		trinity-kde-i18n-Bulgarian = %{version}-%{release}

%description Bulgarian
This package contains %{summary}.

%files Bulgarian
%defattr(-,root,root,-)
%{tde_datadir}/locale/bg/

##########

%package Bengali
Summary:		Bengali(bn) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-bn = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Bengali < %{version}-%{release}
Provides:		trinity-kde-i18n-Bengali = %{version}-%{release}

%description Bengali
This package contains %{summary}.

%files Bengali
%defattr(-,root,root,-)
%{tde_datadir}/locale/bn/

##########

%package Tibetan
Summary:		Tibetan(bo) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-bo = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Tibetan < %{version}-%{release}
Provides:		trinity-kde-i18n-Tibetan = %{version}-%{release}

%description Tibetan
This package contains %{summary}.

#%files Tibetan
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/bo/

##########

%package Breton
Summary:		Breton(br) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-br = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Breton < %{version}-%{release}
Provides:		trinity-kde-i18n-Breton = %{version}-%{release}

%description Breton
This package contains %{summary}.

%files Breton
%defattr(-,root,root,-)
%{tde_datadir}/locale/br/

##########

%package Bosnian
Summary:		Bosnian(bs) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-bs = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Bosnian < %{version}-%{release}
Provides:		trinity-kde-i18n-Bosnian = %{version}-%{release}

%description Bosnian
This package contains %{summary}.

%files Bosnian
%defattr(-,root,root,-)
%{tde_datadir}/locale/bs/

##########

%package Catalan
Summary:		Catalan(ca) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ca = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Catalan < %{version}-%{release}
Provides:		trinity-kde-i18n-Catalan = %{version}-%{release}

%description Catalan
This package contains %{summary}.

%files Catalan
%defattr(-,root,root,-)
%{tde_datadir}/locale/ca/
%{tde_tdedocdir}/HTML/ca/

##########

%package Czech
Summary:		Czech(cs) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-cs = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Czech < %{version}-%{release}
Provides:		trinity-kde-i18n-Czech = %{version}-%{release}

%description Czech
This package contains %{summary}.

%files Czech
%defattr(-,root,root,-)
%{tde_datadir}/locale/cs/
%{tde_tdedocdir}/HTML/cs/

##########

%package Kashubian
Summary:		Kashubian(csb) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-csb = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Kashubian < %{version}-%{release}
Provides:		trinity-kde-i18n-Kashubian = %{version}-%{release}

%description Kashubian
This package contains %{summary}.

%files Kashubian
%defattr(-,root,root,-)
%{tde_datadir}/locale/csb/

##########

%package Cymraeg
Summary:		Cymraeg language support for TDE
Group:			User Interface/Desktops
Obsoletes:		trinity-kde-i18n-Cymraeg < %{version}-%{release}
Provides:		trinity-kde-i18n-Cymraeg = %{version}-%{release}

%description Cymraeg
This package contains %{summary}.

##########

%package Welsh
Summary:		Welsh(cy) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-cy = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Welsh < %{version}-%{release}
Provides:		trinity-kde-i18n-Welsh = %{version}-%{release}

%description Welsh
This package contains %{summary}.

%files Welsh
%defattr(-,root,root,-)
%{tde_datadir}/locale/cy/

##########

%package Danish
Summary:		Danish(da) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-da = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Danish < %{version}-%{release}
Provides:		trinity-kde-i18n-Danish = %{version}-%{release}

%description Danish
This package contains %{summary}.

%files Danish
%defattr(-,root,root,-)
%{tde_datadir}/locale/da/
%{tde_tdedocdir}/HTML/da/

##########

%package German
Summary:		German(de) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-de = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-German < %{version}-%{release}
Provides:		trinity-kde-i18n-German = %{version}-%{release}

%description German
This package contains %{summary}.

%files German
%defattr(-,root,root,-)
%{tde_datadir}/locale/de/
%{tde_tdedocdir}/HTML/de/

##########

%package Greek
Summary:		Greek(el) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-el = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Greek < %{version}-%{release}
Provides:		trinity-kde-i18n-Greek = %{version}-%{release}

%description Greek
This package contains %{summary}.

%files Greek
%defattr(-,root,root,-)
%{tde_datadir}/locale/el/

##########

%package British
Summary:		British(en_GB) English support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-en_GB = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-British < %{version}-%{release}
Provides:		trinity-kde-i18n-British = %{version}-%{release}

%description British
This package contains %{summary}.

%files British
%defattr(-,root,root,-)
%{tde_datadir}/locale/en_GB/
%{tde_tdedocdir}/HTML/en_GB/

##########

%package Esperanto
Summary:		Esperanto(eo) support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-eo = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Esperanto < %{version}-%{release}
Provides:		trinity-kde-i18n-Esperanto = %{version}-%{release}

%description Esperanto
This package contains %{summary}.

%files Esperanto
%defattr(-,root,root,-)
%{tde_datadir}/locale/eo/

##########

%package Spanish
Summary:		Spanish(es) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-es = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Spanish < %{version}-%{release}
Provides:		trinity-kde-i18n-Spanish = %{version}-%{release}

%description Spanish
This package contains %{summary}.

%files Spanish
%defattr(-,root,root,-)
%{tde_datadir}/locale/es/
%{tde_tdedocdir}/HTML/es/

##########

%package Estonian
Summary:		Estonian(et) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-et = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Estonian < %{version}-%{release}
Provides:		trinity-kde-i18n-Estonian = %{version}-%{release}

%description Estonian
This package contains %{summary}.

%files Estonian
%defattr(-,root,root,-)
%{tde_datadir}/locale/et/
%{tde_tdedocdir}/HTML/et/

##########

%package Basque
Summary:		Basque(eu) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-eu = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Basque < %{version}-%{release}
Provides:		trinity-kde-i18n-Basque = %{version}-%{release}

%description Basque
This package contains %{summary}.

%files Basque
%defattr(-,root,root,-)
%{tde_datadir}/locale/eu/
%{tde_tdedocdir}/HTML/eu/

##########

%package Farsi
Summary:		Farsi(fa) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-fa = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Farsi < %{version}-%{release}
Provides:		trinity-kde-i18n-Farsi = %{version}-%{release}

%description Farsi
This package contains %{summary}.

%files Farsi
%defattr(-,root,root,-)
%{tde_datadir}/locale/fa/

##########

%package Finnish
Summary:		Finnish(fi) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-fi = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Finnish < %{version}-%{release}
Provides:		trinity-kde-i18n-Finnish = %{version}-%{release}

%description Finnish
This package contains %{summary}.

%files Finnish
%defattr(-,root,root,-)
%{tde_datadir}/locale/fi/
%{tde_tdedocdir}/HTML/fi/

##########

%package Faroese
Summary:		Faroese(fo) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-fo = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Faroese < %{version}-%{release}
Provides:		trinity-kde-i18n-Faroese = %{version}-%{release}

%description Faroese
This package contains %{summary}.

#%files Faroese
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/fo/

##########

%package French
Summary:		French(fr) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-fr = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-French < %{version}-%{release}
Provides:		trinity-kde-i18n-French = %{version}-%{release}

%description French
This package contains %{summary}.

%files French
%defattr(-,root,root,-)
%{tde_datadir}/locale/fr/
%{tde_tdedocdir}/HTML/fr/

##########

%package Frisian
Summary:		Frisian(fy) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-fy = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Frisian < %{version}-%{release}
Provides:		trinity-kde-i18n-Frisian = %{version}-%{release}

%description Frisian
This package contains %{summary}.

%files Frisian
%defattr(-,root,root,-)
%{tde_datadir}/locale/fy/

##########

%package Irish
Summary:		Irish(ga) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ga = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Irish < %{version}-%{release}
Provides:		trinity-kde-i18n-Irish = %{version}-%{release}

%description Irish
This package contains %{summary}.

%files Irish
%defattr(-,root,root,-)
%{tde_datadir}/locale/ga/

##########

%package Galician
Summary:		Galician(gl) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-gl = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Galician < %{version}-%{release}
Provides:		trinity-kde-i18n-Galician = %{version}-%{release}

%description Galician
This package contains %{summary}.

%files Galician
%defattr(-,root,root,-)
%{tde_datadir}/locale/gl/

##########

%package Hebrew
Summary:		Hebrew(he) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-he = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Hebrew < %{version}-%{release}
Provides:		trinity-kde-i18n-Hebrew = %{version}-%{release}

%description Hebrew
This package contains %{summary}.

%files Hebrew
%defattr(-,root,root,-)
%{tde_datadir}/locale/he/
%{tde_tdedocdir}/HTML/he/

##########

%package Hindi
Summary:		Hindi(hi) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-hi = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Hindi < %{version}-%{release}
Provides:		trinity-kde-i18n-Hindi = %{version}-%{release}

%description Hindi
This package contains %{summary}.

%files Hindi
%defattr(-,root,root,-)
%{tde_datadir}/locale/hi/

##########

%package Croatian
Summary:		Croatian(hr) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-hr = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Croatian < %{version}-%{release}
Provides:		trinity-kde-i18n-Croatian = %{version}-%{release}

%description Croatian
This package contains %{summary}.

%files Croatian
%defattr(-,root,root,-)
%{tde_datadir}/locale/hr/
%{tde_tdedocdir}/HTML/hr/

##########

%package Hungarian
Summary:		Hungarian(hu) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-hu = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Hungarian < %{version}-%{release}
Provides:		trinity-kde-i18n-Hungarian = %{version}-%{release}

%description Hungarian
This package contains %{summary}.

%files Hungarian
%defattr(-,root,root,-)
%{tde_datadir}/locale/hu/
%{tde_tdedocdir}/HTML/hu/

##########

%package Indonesian
Summary:		Indonesian(id) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-id = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Indonesian < %{version}-%{release}
Provides:		trinity-kde-i18n-Indonesian = %{version}-%{release}

%description Indonesian
This package contains %{summary}.

#%files Indonesian
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/id/

##########

%package Icelandic
Summary:		Icelandic(is) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-is = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Icelandic < %{version}-%{release}
Provides:		trinity-kde-i18n-Icelandic = %{version}-%{release}

%description Icelandic
This package contains %{summary}.

%files Icelandic
%defattr(-,root,root,-)
%{tde_datadir}/locale/is/

##########

%package Italian
Summary:		Italian(it) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-it = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Italian < %{version}-%{release}
Provides:		trinity-kde-i18n-Italian = %{version}-%{release}

%description Italian
This package contains %{summary}.

%files Italian
%defattr(-,root,root,-)
%{tde_datadir}/locale/it/
%{tde_tdedocdir}/HTML/it/

##########

%package Japanese
Summary:		Japanese(ja) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ja = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Japanese < %{version}-%{release}
Provides:		trinity-kde-i18n-Japanese = %{version}-%{release}

%description Japanese
This package contains %{summary}.

%files Japanese
%defattr(-,root,root,-)
%{tde_datadir}/locale/ja/
%{tde_tdedocdir}/HTML/ja/

##########

%package Kazakh
Summary:		Kazakh(kk) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-kk = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Kazakh < %{version}-%{release}
Provides:		trinity-kde-i18n-Kazakh = %{version}-%{release}

%description Kazakh
This package contains %{summary}.

%files Kazakh
%defattr(-,root,root,-)
%{tde_datadir}/locale/kk/

##########

%package Khmer
Summary:		Khmer(km) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ko = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Khmer < %{version}-%{release}
Provides:		trinity-kde-i18n-Khmer = %{version}-%{release}

%description Khmer
This package contains %{summary}.

%files Khmer
%defattr(-,root,root,-)
%{tde_datadir}/locale/km/

##########

%package Korean
Summary:		Korean(ko) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ko = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Korean < %{version}-%{release}
Provides:		trinity-kde-i18n-Korean = %{version}-%{release}

%description Korean
This package contains %{summary}.

%files Korean
%defattr(-,root,root,-)
%{tde_datadir}/locale/ko/
%{tde_tdedocdir}/HTML/ko/

##########

%package Kurdish
Summary:		Kurdish(ku) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ku = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Kurdish < %{version}-%{release}
Provides:		trinity-kde-i18n-Kurdish = %{version}-%{release}

%description Kurdish
This package contains %{summary}.

#%files Kurdish
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/ku/

##########

%package Lao
Summary:		Lao(lo) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-lo = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Lao < %{version}-%{release}
Provides:		trinity-kde-i18n-Lao = %{version}-%{release}

%description Lao
This package contains %{summary}.

#%files Lao
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/lo/

##########

%package Lithuanian
Summary:		Lithuanian(lt) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-lt = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Lithuanian < %{version}-%{release}
Provides:		trinity-kde-i18n-Lithuanian = %{version}-%{release}

%description Lithuanian
This package contains %{summary}.

%files Lithuanian
%defattr(-,root,root,-)
%{tde_datadir}/locale/lt/

##########

%package Latvian
Summary:		Latvian(lv) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-lv = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Latvian < %{version}-%{release}
Provides:		trinity-kde-i18n-Latvian = %{version}-%{release}

%description Latvian
This package contains %{summary}.

%files Latvian
%defattr(-,root,root,-)
%{tde_datadir}/locale/lv/

##########

%package Maori
Summary:		Maori(mi) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-mi = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Maori < %{version}-%{release}
Provides:		trinity-kde-i18n-Maori = %{version}-%{release}

%description Maori
This package contains %{summary}.

#%files Maori
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/mi/

##########

%package Macedonian
Summary:		Macedonian(mk) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-mk = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Macedonian < %{version}-%{release}
Provides:		trinity-kde-i18n-Macedonian = %{version}-%{release}

%description Macedonian
This package contains %{summary}.

%files Macedonian
%defattr(-,root,root,-)
%{tde_datadir}/locale/mk/

##########

%package Mongolian
Summary:		Mongolian(mn) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-mn = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Mongolian < %{version}-%{release}
Provides:		trinity-kde-i18n-Mongolian = %{version}-%{release}

%description Mongolian
This package contains %{summary}.

%files Mongolian
%defattr(-,root,root,-)
%{tde_datadir}/locale/mn/

##########

%package Malay
Summary:		Malay(ms) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ms = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Malay < %{version}-%{release}
Provides:		trinity-kde-i18n-Malay = %{version}-%{release}

%description Malay
This package contains %{summary}.

%files Malay
%defattr(-,root,root,-)
%{tde_datadir}/locale/ms/

##########

%package Maltese
Summary:		Maltese(mt) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-mt = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Maltese < %{version}-%{release}
Provides:		trinity-kde-i18n-Maltese = %{version}-%{release}

%description Maltese
This package contains %{summary}.

#%files Maltese
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/mt/

##########

%package Low-Saxon
Summary:		Low Saxon(nds) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-nds = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Low-Saxon < %{version}-%{release}
Provides:		trinity-kde-i18n-Low-Saxon = %{version}-%{release}

%description Low-Saxon
This package contains %{summary}.

%files Low-Saxon
%defattr(-,root,root,-)
%{tde_datadir}/locale/nds/

##########

%package Dutch
Summary:		Dutch(nl) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-nl = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Dutch < %{version}-%{release}
Provides:		trinity-kde-i18n-Dutch = %{version}-%{release}

%description Dutch
This package contains %{summary}.

%files Dutch
%defattr(-,root,root,-)
%{tde_datadir}/locale/nl/
%{tde_tdedocdir}/HTML/nl/

##########

%package Norwegian
Summary:		Norwegian(no) (Bokmaal) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-no = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Norwegian < %{version}-%{release}
Provides:		trinity-kde-i18n-Norwegian = %{version}-%{release}

%description Norwegian
This package contains %{summary}.

%files Norwegian
%defattr(-,root,root,-)
%{tde_datadir}/locale/nb/

##########

%package Norwegian-Nynorsk
Summary:		Norwegian(nn) (Nynorsk) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-nn = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Norwegian-Nynorsk < %{version}-%{release}
Provides:		trinity-kde-i18n-Norwegian-Nynorsk = %{version}-%{release}

%description Norwegian-Nynorsk
This package contains %{summary}.

%files Norwegian-Nynorsk
%defattr(-,root,root,-)
%{tde_datadir}/locale/nn/

##########

%package Occitan
Summary:		Occitan(oc) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-oc = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Occitan < %{version}-%{release}
Provides:		trinity-kde-i18n-Occitan = %{version}-%{release}

%description Occitan
This package contains %{summary}.

#%files Occitan
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/oc/

##########

%package Polish
Summary:		Polish(pl) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-pl = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Polish < %{version}-%{release}
Provides:		trinity-kde-i18n-Polish = %{version}-%{release}

%description Polish
This package contains %{summary}.

%files Polish
%defattr(-,root,root,-)
%{tde_datadir}/locale/pl/
%{tde_tdedocdir}/HTML/pl/

##########

%package Portuguese
Summary:		Portuguese(pt) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-pt = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Portuguese < %{version}-%{release}
Provides:		trinity-kde-i18n-Portuguese = %{version}-%{release}

%description Portuguese
This package contains %{summary}.

%files Portuguese
%defattr(-,root,root,-)
%{tde_datadir}/locale/pt/
%{tde_tdedocdir}/HTML/pt/

##########

%package Punjabi
Summary:		Punjabi(pa) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-pa = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Punjabi < %{version}-%{release}
Provides:		trinity-kde-i18n-Punjabi = %{version}-%{release}

%description Punjabi
This package contains %{summary}.

%files Punjabi
%defattr(-,root,root,-)
%{tde_datadir}/locale/pa/

##########

%package Brazil
Summary:		Brazil(pt_BR) Portuguese language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-pt_BR = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Brazil < %{version}-%{release}
Provides:		trinity-kde-i18n-Brazil = %{version}-%{release}

%description Brazil
This package contains %{summary}.

%files Brazil
%defattr(-,root,root,-)
%{tde_datadir}/locale/pt_BR/
%{tde_tdedocdir}/HTML/pt_BR/

##########

%package Romanian
Summary:		Romanian(ro) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ro = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Romanian < %{version}-%{release}
Provides:		trinity-kde-i18n-Romanian = %{version}-%{release}

%description Romanian
This package contains %{summary}.

%files Romanian
%defattr(-,root,root,-)
%{tde_datadir}/locale/ro/
%{tde_tdedocdir}/HTML/ro/

##########

%package Russian
Summary:		Russian(ru) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ru = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Russian < %{version}-%{release}
Provides:		trinity-kde-i18n-Russian = %{version}-%{release}

%description Russian
This package contains %{summary}.

%files Russian
%defattr(-,root,root,-)
%{tde_datadir}/locale/ru/
%{tde_tdedocdir}/HTML/ru/

##########

%package Kinyarwanda
Summary:		Kinyarwanda(rw) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-rw = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Kinyarwanda < %{version}-%{release}
Provides:		trinity-kde-i18n-Kinyarwanda = %{version}-%{release}

%description Kinyarwanda
This package contains %{summary}.

%files Kinyarwanda
%defattr(-,root,root,-)
%{tde_datadir}/locale/rw/

##########

%package Northern-Sami
Summary:		Northern-Sami(se) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-se = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Northern-Sami < %{version}-%{release}
Provides:		trinity-kde-i18n-Northern-Sami = %{version}-%{release}

%description Northern-Sami
This package contains %{summary}.

%files Northern-Sami
%defattr(-,root,root,-)
%{tde_datadir}/locale/se/

##########

%package Slovak
Summary:		Slovak(sk) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-sk = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Slovak < %{version}-%{release}
Provides:		trinity-kde-i18n-Slovak = %{version}-%{release}

%description Slovak
This package contains %{summary}.

%files Slovak
%defattr(-,root,root,-)
%{tde_datadir}/locale/sk/
%{tde_tdedocdir}/HTML/sk/

##########

%package Slovenian
Summary:		Slovenian(sl) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-sl = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Slovenian < %{version}-%{release}
Provides:		trinity-kde-i18n-Slovenian = %{version}-%{release}

%description Slovenian
This package contains %{summary}.

%files Slovenian
%defattr(-,root,root,-)
%{tde_datadir}/locale/sl/
%{tde_tdedocdir}/HTML/sl/

##########

%package Serbian
Summary:		Serbian(sr) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-sr = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Serbian < %{version}-%{release}
Provides:		trinity-kde-i18n-Serbian = %{version}-%{release}

%description Serbian
This package contains %{summary}.

%files Serbian
%defattr(-,root,root,-)
%{tde_datadir}/locale/sr/
%{tde_tdedocdir}/HTML/sr/

##########

%package Serbian-Latin
Summary:		Serbian-Latin(sr@Latn) language support for TDE
Group:			User Interface/Desktops
Obsoletes:		trinity-kde-i18n-Serbian-Latin < %{version}-%{release}
Provides:		trinity-kde-i18n-Serbian-Latin = %{version}-%{release}

%description Serbian-Latin
This package contains %{summary}.

%files Serbian-Latin
%defattr(-,root,root,-)
%{tde_datadir}/locale/sr@Latn/

##########

%package South-Sudan
Summary:		South-Sudan(ss) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ss = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-South-Sudan < %{version}-%{release}
Provides:		trinity-kde-i18n-South-Sudan = %{version}-%{release}

%description South-Sudan
This package contains %{summary}.

%files South-Sudan
%defattr(-,root,root,-)
%{tde_datadir}/locale/ss/

##########

%package Swedish
Summary:		Swedish(sv) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-sv = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Swedish < %{version}-%{release}
Provides:		trinity-kde-i18n-Swedish = %{version}-%{release}

%description Swedish
This package contains %{summary}.

%files Swedish
%defattr(-,root,root,-)
%{tde_datadir}/locale/sv/
%{tde_tdedocdir}/HTML/sv/

##########

%package Tamil
Summary:		Tamil(ta) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ta = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Tamil < %{version}-%{release}
Provides:		trinity-kde-i18n-Tamil = %{version}-%{release}

%description Tamil
This package contains %{summary}.

%files Tamil
%defattr(-,root,root,-)
%{tde_datadir}/locale/ta/

##########

%package Telugu
Summary:		Telugu(te) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-te = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Telugu < %{version}-%{release}
Provides:		trinity-kde-i18n-Telugu = %{version}-%{release}

%description Telugu
This package contains %{summary}.

%files Telugu
%defattr(-,root,root,-)
%{tde_datadir}/locale/te/

##########

%package Tajik
Summary:		Tajik(tg) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-tg = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Tajik < %{version}-%{release}
Provides:		trinity-kde-i18n-Tajik = %{version}-%{release}

%description Tajik
This package contains %{summary}.

%files Tajik
%defattr(-,root,root,-)
%{tde_datadir}/locale/tg/

##########

%package Thai
Summary:		Thai(th) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-th = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Thai < %{version}-%{release}
Provides:		trinity-kde-i18n-Thai = %{version}-%{release}

%description Thai
This package contains %{summary}.

%files Thai
%defattr(-,root,root,-)
%{tde_datadir}/locale/th/

##########

%package Turkish
Summary:		Turkish(tr) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-tr = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Turkish < %{version}-%{release}
Provides:		trinity-kde-i18n-Turkish = %{version}-%{release}

%description Turkish
This package contains %{summary}.

%files Turkish
%defattr(-,root,root,-)
%{tde_datadir}/locale/tr/
%{tde_tdedocdir}/HTML/tr/

##########

%package Ukrainian
Summary:		Ukrainian(uk) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-uk = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Ukrainian < %{version}-%{release}
Provides:		trinity-kde-i18n-Ukrainian = %{version}-%{release}

%description Ukrainian
This package contains %{summary}.

%files Ukrainian
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/uk/
%{tde_datadir}/locale/uk/

##########

%package Uzbek
Summary:		Uzbek(uz) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-uz = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Uzbek < %{version}-%{release}
Provides:		trinity-kde-i18n-Uzbek = %{version}-%{release}

%description Uzbek
This package contains %{summary}.

%files Uzbek
%defattr(-,root,root,-)
%{tde_datadir}/locale/uz/

##########

%package Uzbek-Cyrillic
Summary:		Uzbek(uz@cyrillic) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-uz@cyrillic = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Uzbek-Cyrillic < %{version}-%{release}
Provides:		trinity-kde-i18n-Uzbek-Cyrillic = %{version}-%{release}

%description Uzbek-Cyrillic
This package contains %{summary}.

%files Uzbek-Cyrillic
%defattr(-,root,root,-)
%{tde_datadir}/locale/uz@cyrillic/

##########

%package Venda
Summary:		Venda(ven) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-ven = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Venda < %{version}-%{release}
Provides:		trinity-kde-i18n-Venda = %{version}-%{release}

%description Venda
This package contains %{summary}.

#%files Venda
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/ven/

##########

%package Vietnamese
Summary:		Vietnamese(vi) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-vi = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Vietnamese < %{version}-%{release}
Provides:		trinity-kde-i18n-Vietnamese = %{version}-%{release}

%description Vietnamese
This package contains %{summary}.

%files Vietnamese
%defattr(-,root,root,-)
%{tde_datadir}/locale/vi/

##########

%package Walloon
Summary:		Walloon(wa) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-wa = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Walloon < %{version}-%{release}
Provides:		trinity-kde-i18n-Walloon = %{version}-%{release}

%description Walloon
This package contains %{summary}.

%files Walloon
%defattr(-,root,root,-)
%{tde_datadir}/locale/wa/

##########

%package Xhosa
Summary:		Xhosa(xh) (a Bantu language) support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-xh = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Xhosa < %{version}-%{release}
Provides:		trinity-kde-i18n-Xhosa = %{version}-%{release}

%description Xhosa
This package contains %{summary}.

#%files Xhosa
#%defattr(-,root,root,-)
#%{tde_datadir}/locale/xh/

##########

%package Chinese
Summary:		Chinese(zh_CN) (Simplified Chinese) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-zh_CN = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Chinese < %{version}-%{release}
Provides:		trinity-kde-i18n-Chinese = %{version}-%{release}

%description Chinese
This package contains %{summary}.

%files Chinese
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_CN/
%{tde_tdedocdir}/HTML/zh_CN/

##########

%package Chinese-Big5
Summary:		Chinese(zh_TW) (Big5) language support for TDE
Group:			User Interface/Desktops
Provides:		%{name}-tz_TW = %{version}-%{release}
Obsoletes:		trinity-kde-i18n-Chinese-Big5 < %{version}-%{release}
Provides:		trinity-kde-i18n-Chinese-Big5 = %{version}-%{release}

%description Chinese-Big5
This package contains %{summary}.

%files Chinese-Big5
%defattr(-,root,root,-)
%{tde_datadir}/locale/zh_TW/
%{tde_tdedocdir}/HTML/zh_TW/

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

(
for l in %{TDE_LANGS}; do
  for f in tde-i18n-${l}/; do
    if [ -d "${f}" ]; then 
      pushd ${f}
      if ! rpm -E %%cmake|grep -q "cd build"; then
        %__mkdir_p build
        cd build
      fi
      
      %cmake \
        -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        \
        -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
        -DBIN_INSTALL_DIR="%{tde_bindir}" \
        -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
        -DLIB_INSTALL_DIR="%{tde_libdir}" \
        -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig" \
        -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
        \
        -DBUILD_ALL=ON \
        -DBUILD_DOC=ON \
        -DBUILD_DATA=ON \
        -DBUILD_MESSAGES=ON \
      ..

      # Run the build process in background
      ( %__make -j4 || %__make || echo TDE_Error ) &
      
      # Do not build more than 4 languages at the same time
      while [ $(jobs | wc -l) -ge 4 ]; do sleep 3; done
      popd
    fi
  done
done
) 2>&1 | tee /tmp/rpmbuild.$$

if grep -qw TDE_Error /tmp/rpmbuild.$$; then
  echo "Error while building. See '/tmp/rpmbuild.$$'"
  exit 1
fi

wait
rm -f /tmp/rpmbuild.$$


%install
%__rm -rf %{?buildroot}
export PATH="%{tde_bindir}:${PATH}"

for l in %{TDE_LANGS}; do
  for f in tde-i18n-${l}/; do
    %__make install DESTDIR="%{?buildroot}" -C "${f}/build"
  done
done


# remove zero-length file
find "%{buildroot}%{tde_tdedocdir}/HTML" -size 0 -exec rm -f {} \;

# remove obsolete KDE 3 application data translations
%__rm -rf "%{buildroot}%{tde_datadir}/apps"


%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE 14.0.0
