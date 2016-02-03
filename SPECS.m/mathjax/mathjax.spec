Name:       mathjax
Version:    2.4.0
Release:    2%{?dist}
Summary:    JavaScript library to render math in the browser
License:    ASL 2.0
URL:        http://mathjax.org
Source0:    https://github.com/mathjax/MathJax/archive/%{version}.tar.gz

BuildArch:  noarch

BuildRequires:   web-assets-devel
BuildRequires:   fontpackages-devel

Requires:        web-assets-filesystem
Requires:        %{name}-ams-fonts
Requires:        %{name}-caligraphic-fonts
Requires:        %{name}-fraktur-fonts %{name}-main-fonts
Requires:        %{name}-math-fonts
Requires:        %{name}-sansserif-fonts
Requires:        %{name}-script-fonts
Requires:        %{name}-typewriter-fonts
Requires:        %{name}-size1-fonts
Requires:        %{name}-size2-fonts
Requires:        %{name}-size3-fonts
Requires:        %{name}-size4-fonts
Requires:        %{name}-size1-fonts
Requires:        %{name}-winie6-fonts
Requires:        %{name}-winchrome-fonts

%description
MathJax is an open-source JavaScript display engine for LaTeX, MathML,
and AsciiMath notation that works in all modern browsers. It requires no
setup on the part of the user (no plugins to download or software to
install), so the page author can write web documents that include
mathematics and be confident that users will be able to view it
naturally and easily. Supports LaTeX, MathML, and AsciiMath notation
in HTML pages.

%global fontsummary Fonts used by MathJax to display math in the browser

%package       ams-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   ams-fonts
%{fontsummary}.

%package       caligraphic-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   caligraphic-fonts
%{fontsummary}.

%package       fraktur-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   fraktur-fonts
%{fontsummary}.

%package       main-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   main-fonts
%{fontsummary}.

%package       math-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   math-fonts
%{fontsummary}.

%package       sansserif-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   sansserif-fonts
%{fontsummary}.

%package       script-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   script-fonts
%{fontsummary}.

%package       typewriter-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   typewriter-fonts
%{fontsummary}.

%package       size1-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   size1-fonts
%{fontsummary}.

%package       size2-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   size2-fonts
%{fontsummary}.

%package       size3-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   size3-fonts
%{fontsummary}.

%package       size4-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   size4-fonts
%{fontsummary}.

%package       winie6-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   winie6-fonts
%{fontsummary}.

%package       winchrome-fonts
Summary:       %{fontsummary}
Requires:      fontpackages-filesystem
License:       OFL
%description   winchrome-fonts
%{fontsummary}.

%prep
%setup -q -n MathJax-%{version}
# Remove bundled fonts
rm -rf MathJax-2.4.0/jax/output
rm -rf MathJax-2.4.0/fonts/HTML-CSS/{Asana-Math,Gyre-Pagella,Gyre-Termes,Latin-Modern,Neo-Euler,STIX-Web}

# Remove minified javascript.
for i in $(find . -type f -path '*unpacked*'); do \
  mv $i ${i//unpacked/}; done
find . -depth -type d -path '*unpacked*' -delete
for i in MathJax.js jax/output/HTML-CSS/jax.js jax/output/HTML-CSS/imageFonts.js; do \
    sed -r 's#(MathJax|BASE)[.]isPacked#1#' <$i >$i.tmp; \
    touch -r $i $i.tmp; \
    mv $i.tmp $i; \
done

%build
# minification should be performed here at some point

%install
mkdir -p %{buildroot}%{_jsdir}/mathjax
cp -pr MathJax.js config/ extensions/ jax/ localization/ images/ test/ \
    %{buildroot}%{_jsdir}/mathjax/

mkdir -p %{buildroot}%{_jsdir}/mathjax/fonts/HTML-CSS/TeX/
cp -pr fonts/HTML-CSS/TeX/png %{buildroot}%{_jsdir}/mathjax/fonts/HTML-CSS/TeX/

mkdir -p %{buildroot}%{_fontdir}
cp -pr fonts/HTML-CSS/TeX/*/MathJax_$i*.{eot,otf,svg} %{buildroot}%{_fontdir}

for t in eot otf svg; do \
    mkdir -p %{buildroot}%{_jsdir}/mathjax/fonts/HTML-CSS/TeX/$t; \
    for i in fonts/HTML-CSS/TeX/$t/MathJax_*.$t; do \
        ln -s %{_fontdir}/$(basename $i) \
            %{buildroot}%{_jsdir}/mathjax/fonts/HTML-CSS/TeX/$t/; \
    done \
done

%files
%{_jsdir}/mathjax
%doc README.md LICENSE

%_font_pkg -n %{name}-AMS MathJax_AMS*.eot MathJax_AMS*.otf MathJax_AMS*.svg
%_font_pkg -n %{name}-Caligraphic MathJax_Caligraphic*.eot MathJax_Caligraphic*.otf MathJax_Caligraphic*.svg
%_font_pkg -n %{name}-Fraktur MathJax_Fraktur*.eot MathJax_Fraktur*.otf MathJax_Fraktur*.svg
%_font_pkg -n %{name}-Main MathJax_Main*.eot MathJax_Main*.otf MathJax_Main*.svg
%_font_pkg -n %{name}-Math MathJax_Math*.eot MathJax_Math*.otf MathJax_Math*.svg
%_font_pkg -n %{name}-SansSerif MathJax_SansSerif*.eot MathJax_SansSerif*.otf MathJax_SansSerif*.svg
%_font_pkg -n %{name}-Script MathJax_Script*.eot MathJax_Script*.otf MathJax_Script*.svg
%_font_pkg -n %{name}-Typewriter MathJax_Typewriter*.eot MathJax_Typewriter*.otf MathJax_Typewriter*.svg
%_font_pkg -n %{name}-Size1 MathJax_Size1*.eot MathJax_Size1*.otf MathJax_Size1*.svg
%_font_pkg -n %{name}-Size2 MathJax_Size2*.eot MathJax_Size2*.otf MathJax_Size2*.svg
%_font_pkg -n %{name}-Size3 MathJax_Size3*.eot MathJax_Size3*.otf MathJax_Size3*.svg
%_font_pkg -n %{name}-Size4 MathJax_Size4*.eot MathJax_Size4*.otf MathJax_Size4*.svg
%_font_pkg -n %{name}-WinIE6 MathJax_WinIE6*.eot MathJax_WinIE6*.otf
%_font_pkg -n %{name}-WinChrome MathJax_WinChrome*.otf MathJax_WinChrome*.svg

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 11 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.0-1
- Update to latest upstream version.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Oct 26 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-3
- Unpackage .woff format.
- Package accepted (#1016677).

* Tue Oct 08 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-2
- Remove some empty directories from the package.

* Mon Oct 07 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-1
- Initial package.
