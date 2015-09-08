%global fontname fontawesome
%global fontconf 60-%{fontname}.conf

Name:		%{fontname}-fonts
Version:	4.4.0
Release:	1%{?dist}
Summary:	Iconic font set
Summary(zh_CN.UTF-8): Iconic 字体集
License:	OFL
URL:		http://fontawesome.io/
Source0:	http://fontawesome.io/assets/font-awesome-%{version}.zip
Source1:	%{name}-fontconfig.conf
Source2:	README-Trademarks.txt
BuildArch:	noarch
BuildRequires:	fontpackages-devel
BuildRequires:	ttembed
Requires:	fontpackages-filesystem


%description
Font Awesome gives you scalable vector icons that can instantly be
customized — size, color, drop shadow, and anything that can be done with the
power of CSS.

%description -l zh_CN.UTF-8
Iconic 字体集。

%package web
License:	MIT
Requires:	%{fontname}-fonts = %{version}-%{release}
Summary:	Web files for fontawesome
Summary(zh_CN.UTF-8): %{name} 的网页文件

%description web
Web files for Font Awesome.
%description web -l zh_CN.UTF-8
%{name} 的网页文件。

%prep
%setup -q -n font-awesome-%{version}
cp -p %SOURCE2 .

%build
ttembed fonts/*.ttf fonts/*.otf

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.ttf fonts/*.otf fonts/*.woff fonts/*.svg %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
		%{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
		%{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
		%{buildroot}%{_fontconfig_confdir}/%{fontconf}

mkdir -p %{buildroot}%{_datadir}/font-awesome-web/
cp -a css less scss %{buildroot}%{_datadir}/font-awesome-web/
magic_rpm_clean.sh

# files:
%_font_pkg -f %{fontconf} *.ttf *.otf
%exclude %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg
%exclude %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff

%doc README-Trademarks.txt

%files web
%{_datadir}/font-awesome-web/
%{_datadir}/fonts/fontawesome/fontawesome-webfont.svg
%{_datadir}/fonts/fontawesome/fontawesome-webfont.woff

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 4.4.0-1
- 更新到 4.4.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 04 2014 Matthias Runge <mrunge@redhad.com> - 4.1.0-2
- include .woff and .svg files (rhbz#1110646)

* Tue Jul 08 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.0-1
- update to version 4.1.0
- renamed web packaged dir from font-awesome-$version to font-awesome-web

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 02 2014 Petr Vobornik <pvoborni@redhat.com> - 4.0.3-1
- embeddable flag set to installable by ttembed
- web package license updated to MIT
- README-Trademarks.txt added

* Mon Nov 04 2013 Ryan Lerch <ryanlerch@fedoraproject.org> - 4.0.3-0
- initial package based off spot's package
