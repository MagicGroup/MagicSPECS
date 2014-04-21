%define my_subversion b7
Name:           html2ps
Version:        1.0
Release:        0.9.%{my_subversion}%{?dist}
Summary:        HTML to PostScript converter
Summary(zh_CN.UTF-8): HTML 到 PostScript 的转换器

Group:          Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
License:        GPLv2+
URL:            http://user.it.uu.se/~jan/%{name}.html
Source0:        http://user.it.uu.se/~jan/%{name}-1.0%{my_subversion}.tar.gz
Source1:        xhtml2ps.desktop
Patch0:         http://ftp.de.debian.org/debian/pool/main/h/%{name}/%{name}_1.0b5-5.diff.gz
# use xdg-open in xhtml2ps
Patch1:         %{name}-1.0b5-xdg-open.patch
# patch config file from debian to use dvips, avoid using weblint 
# don't set letter as default page type, paperconf will set the default
Patch2:         %{name}-1.0b5-config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  desktop-file-utils
# Depend on paperconf directly (instead of libpaper package) for rpmlint sake
Requires:       tex(tex) tex(dvips) ghostscript /usr/bin/paperconf
# not autodetected since they are called by require not at the beginning of 
# line
Requires:       perl(LWP::UserAgent) perl(HTTP::Cookies) perl(HTTP::Request)

%description
An HTML to PostScript converter written in Perl.
* Many possibilities to control the appearance. 
* Support for processing multiple documents.
* A table of contents can be generated.
* Configurable page headers/footers.
* Automatic hyphenation and text justification can be selected. 

%description -l zh_CN.UTF-8
HTML 到 PostScript 的转换器，使用 Perl 语言编写。

%package -n xhtml2ps
Summary:     GUI front-end for html2ps
Summary(zh_CN.UTF-8): %{name} 图形界面
Group:       User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
Requires:    html2ps = %{version}-%{release}
Requires:    xdg-utils

%description -n xhtml2ps
X-html2ps is freely-available GUI front-end for html2ps, a HTML-to-PostScript
converter.

%description -n xhtml2ps -l zh_CN.UTF-8
%{name} 的图形界面。

%prep
%setup -q -n %{name}-1.0%{my_subversion}
%patch0 -p1
%patch1 -p1 -b .xdg-open
%patch2 -p1 -b .config

# convert README to utf8
iconv -f latin1 -t utf8 < README > README.utf8
touch -c -r README README.utf8
mv README.utf8 README

patch -p1 < debian/patches/01_manpages.dpatch
# 03_html2ps.dpatch is against 1.0b5, adjust it to 1.0b6
< debian/patches/03_html2ps.dpatch sed -e 's|/opt/misc/|/it/sw/share/www/|' | \
    patch -p1

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5}

sed -e 's;/etc/html2psrc;%{_sysconfdir}/html2psrc;' \
    -e 's;/usr/share/doc/html2ps;%{_docdir}/%{name}-%{version};' \
        html2ps > $RPM_BUILD_ROOT%{_bindir}/html2ps
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/html2ps
install -p -m0644 html2ps.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m0644 html2psrc.5 $RPM_BUILD_ROOT%{_mandir}/man5
sed -e 's;/usr/bin;%{_bindir};' \
    -e 's;/usr/share/texmf-texlive;%{_datadir}/texmf;' \
    debian/config/html2psrc > $RPM_BUILD_ROOT%{_sysconfdir}/html2psrc

install -m0755 -p contrib/xhtml2ps/xhtml2ps $RPM_BUILD_ROOT%{_bindir}
desktop-file-install --vendor="magic"               \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
  %{SOURCE1}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README sample html2ps.html
%config(noreplace) %{_sysconfdir}/html2psrc
%{_bindir}/html2ps
%{_mandir}/man1/html2ps.1*
%{_mandir}/man5/html2psrc.5*

%files -n xhtml2ps
%defattr(-,root,root,-)
%doc contrib/xhtml2ps/README contrib/xhtml2ps/LICENSE
%{_bindir}/xhtml2ps
%{_datadir}/applications/*xhtml2ps.desktop

%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.0-0.9.b7
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0-0.8.b7
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.b7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May  7 2010 Petr Pisar <ppisar@redhat.com> - 1.0-0.6.b7
- 1.0b7 bump
- Increase revision to 0.6 to have NVR upper then F-13 package

* Thu Apr 29 2010 Petr Pisar <ppisar@redhat.com> - 1.0-0.1.b6
- 1.0b6 bump (#530403)
- Fix regression from upstream 1.0b5..1.0b6
- Fix spelling
- Default attributes for xhtml2ps %%files
- Replace libpaper dependency with paperconf binary to make rpmlint happy

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.2.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr 18 2008 Patrice Dumas <pertusus@free.fr> 1.0-0.1.b5
- initial release
