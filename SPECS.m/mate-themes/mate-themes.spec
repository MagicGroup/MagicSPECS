Name:           mate-themes
Version:        1.4.0
Release:        8%{?dist}
Summary:        MATE Desktop themes
License:        GPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:  icon-naming-utils mate-common mate-doc-utils mate-icon-theme-devel
BuildRequires:  pkgconfig(gtk-engines-2)
Requires:       mate-icon-theme
Requires:       gtk2-engines
Requires:       gtk-murrine-engine
BuildARch:      noarch

%description
MATE Desktop themes


%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --enable-all-themes   \
           --enable-test-themes  \
           --enable-icon-mapping \
           --enable-test-themes
make %{?_smp_mflags} V=1


%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'
magic_rpm_clean.sh
%find_lang %{name}


%post
for icon_theme in \
  Fog PrintLarge Quid Reverse Shiny Simply TraditionalOk \
  ContrastHighLargePrint ContrastHighLargePrintInverse \
  ContrastLow ContrastHigh ContrastHighInverse Aldabra ;
do
  /bin/touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
done

%postun
if [ $1 -eq 0 ]; then
for icon_theme in \
  Fog PrintLarge Quid Reverse Shiny Simply TraditionalOk \
  ContrastHighLargePrint ContrastHighLargePrintInverse \
  ContrastLow ContrastHigh ContrastHighInverse Aldabra ;
do
  /bin/touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done
fi

%posttrans
for icon_theme in \
  Fog PrintLarge Quid Reverse Shiny Simply TraditionalOk \
  ContrastHighLargePrint ContrastHighLargePrintInverse \
  ContrastLow ContrastHigh ContrastHighInverse Aldabra ;
do
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/icons/ContrastHigh-SVG
%{_datadir}/themes/TraditionalOkClassic
%{_datadir}/themes/ContrastLowLargePrint
%{_datadir}/themes/Fog
%{_datadir}/themes/PrintLarge
%{_datadir}/themes/Quid
%{_datadir}/themes/Reverse
%{_datadir}/themes/Shiny
%{_datadir}/themes/Simply
%{_datadir}/themes/TraditionalOk
%{_datadir}/themes/ContrastHighLargePrint
%{_datadir}/themes/ContrastHighLargePrintInverse
%{_datadir}/themes/ContrastLow
%{_datadir}/themes/ContrastHigh
%{_datadir}/themes/ContrastHighInverse
%{_datadir}/themes/Aldabra
%{_datadir}/icons/ContrastHigh
%{_datadir}/icons/ContrastHighInverse
%{_datadir}/icons/ContrastHighLargePrint
%{_datadir}/icons/Fog
%{_datadir}/icons/MateLargePrint
%{_datadir}/icons/Quid
%{_datadir}/themes/AlaDelta
%{_datadir}/themes/Atantla
%{_datadir}/icons/mate/cursors
%{_datadir}/icons/ContrastHighLargePrintInverse
%{_datadir}/themes/TraditionalOkTest

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-8
- 为 Magic 3.0 重建

* Sat Oct 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-7
- add requires gtk2-engines and mate-icon-theme 

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-6
- fix mistake in scriptlets from last commit

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-5
- Fix scriplets
- add requires gtk-murrine-engine

* Sun Oct 14 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update BR and add test themes

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix missing icon scriptlets

* Sun Sep 30 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Update br and post scriptlets as per package review

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
