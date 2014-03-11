Name:           debconf
Version:        1.5.52
Release:        1%{?dist}
Summary:        Debian configuration management system

Group:          Development/Tools
License:        BSD
URL:            http://packages.debian.org/sid/debconf
Source0:        http://ftp.de.debian.org/debian/pool/main/d/%{name}/%{name}_%{version}.tar.gz
Patch1:         debconf-1.5.49-python_version_support.patch
BuildArch:      noarch

BuildRequires:  python
BuildRequires:  po4a >= 0.23
BuildRequires:  gettext >= 0.13
BuildRequires:  perlqt-devel
# Not actual requirements, although listed at
# http://ftp.de.debian.org/debian/pool/main/d/debconf/debconf_1.5.32.dsc
#BuildRequires:  debhelper >= 7.0.50
#BuildRequires:  perl-libintl
#BuildRequires:  po-debconf

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Debconf is a configuration management system for Debian
packages. Packages use Debconf to ask questions when
they are installed.

%package gnome
Summary:       GNOME frontend for debconf
Requires:      %{name} = %{version}-%{release}

%description gnome
This package contains the GNOME frontend for debconf.

%package kde
Summary:       KDE frontend for debconf
Requires:      %{name} = %{version}-%{release}

%description kde
This package contains the KDE frontend for debconf.

%package doc
Summary:        Debconf documentation
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains lots of additional documentation for Debconf,
including the debconf user's guide, documentation about using
different backend databases via the /etc/debconf.conf file, and a
developer's guide to debconf.

%package i18n
Summary:        Full internationalization support for debconf
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description i18n
This package provides full internationalization for debconf,
including translations into all available languages, support
for using translated debconf templates, and support for
proper display of multibyte character sets.

%package utils
Summary:        This package contains some small utilities for debconf developers
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description utils
This package contains some small utilities for debconf developers.

%prep
%setup -q -n debconf
%patch1 -p1


%build
make %{?_smp_mflags}

%install
make install-utils prefix=%{buildroot}
make install-rest prefix=%{buildroot}
make install-i18n prefix=%{buildroot}

# Add /var/cache/debconf and initial contents
mkdir -p %{buildroot}/%{_var}/cache/%{name}
touch %{buildroot}/%{_var}/cache/%{name}/config.dat
touch %{buildroot}/%{_var}/cache/%{name}/passwords.dat
touch %{buildroot}/%{_var}/cache/%{name}/templates.dat

mkdir -p \
        %{buildroot}/%{perl_vendorlib} \
        %{buildroot}/%{_mandir}/man{1,3,5,7,8} \
        %{buildroot}/%{_mandir}/de/man{1,3,5,7,8} \
        %{buildroot}/%{_mandir}/fr/man{1,3,5,7,8} \
        %{buildroot}/%{_mandir}/ru/man{1,3,5,7,8} \
        %{buildroot}/%{_mandir}/pt_BR/man{1,3,8}

%if "%{_datadir}/perl5" != "%{perl_vendorlib}"
mv %{buildroot}/%{_datadir}/perl5/Debconf %{buildroot}/%{perl_vendorlib}/.
mv %{buildroot}/%{_datadir}/perl5/Debian %{buildroot}/%{perl_vendorlib}/.
%endif

chmod 755 %{buildroot}/%{_datadir}/%{name}/confmodule*

# Base and i18n man pages
for man in \
        "debconf-apt-progress" \
        "debconf-communicate" \
        "debconf-copydb" \
        "debconf-escape" \
        "debconf-set-selections" \
        "debconf-show" \
        "debconf" \
        "dpkg-preconfigure" \
        "dpkg-reconfigure"; do

    for level in 1 8; do
        for lang in de fr pt_BR ru; do
            if test -f doc/man/gen/$man.$lang.$level; then
                short_lang=`echo "$lang" | sed 's/_.*//'`
                install -m 644 doc/man/gen/$man.$lang.$level %{buildroot}/%{_mandir}/$lang/man$level/$man.$level
                echo "%lang($short_lang) %{_mandir}/$lang/man$level/$man.$level*" >> "man-i18n.lang"
            fi
        done
        test -f doc/man/gen/$man.$level && \
            install -m 644 doc/man/gen/$man.$level %{buildroot}/%{_mandir}/man$level/$man.$level
    done
done

# Doc foo
for man in \
        "Debconf::Client::ConfModule" \
        "confmodule" \
        "debconf.conf" \
        "debconf-devel" \
        "debconf"; do

    for level in 3 5 7; do
        for lang in de fr pt_BR ru; do
            if test -f doc/man/$man.$lang.$level*; then
                short_lang=`echo "$lang" | sed 's/_.*//'`
                install -m 644 doc/man/$man.$lang.$level* %{buildroot}/%{_mandir}/$lang/man$level/$man.$level
                echo "%lang($short_lang) %{_mandir}/$lang/man$level/$man.$level*" >> "man-doc.lang"
            fi
        done
        test -f doc/man/$man.$level && \
            install -m 644 doc/man/$man.$level %{buildroot}/%{_mandir}/man$level/$man.$level
    done
done

# Utils man pages
for man in get-selections \
            getlang \
            loadtemplate \
            mergetemplate; do
    for lang in de fr pt_BR ru; do
        short_lang=`echo "$lang" | sed 's/_.*//'`
        if test -f doc/man/gen/debconf-$man.$lang.1; then
            install -m 644 doc/man/gen/debconf-$man.$lang.1 %{buildroot}/%{_mandir}/$lang/man1/debconf-$man.1
            echo "%lang($short_lang) %{_mandir}/$lang/man1/debconf-$man.1*" >> "man-utils.lang"
        fi
    done
    test -f doc/man/gen/debconf-$man.1 && \
        install -m 644 doc/man/gen/debconf-$man.1 %{buildroot}/%{_mandir}/man1/debconf-$man.1
done

%find_lang debconf

%files
%doc doc/README doc/EXAMPLES doc/CREDITS doc/README.translators doc/README.LDAP doc/TODO
%doc debian/changelog debian/copyright debian/README.Debian
%config(noreplace) %{_sysconfdir}/debconf.conf
%{_bindir}/debconf
%{_bindir}/debconf-apt-progress
%{_bindir}/debconf-communicate
%{_bindir}/debconf-copydb
%{_bindir}/debconf-escape
%{_bindir}/debconf-set-selections
%{_bindir}/debconf-show
%{_sbindir}/dpkg-preconfigure
%{_sbindir}/dpkg-reconfigure
%{python_sitelib}/debconf.*
%exclude /usr/lib/python3
%{perl_vendorlib}/Debconf
%{perl_vendorlib}/Debian
%{_datadir}/%{name}
%{_mandir}/man1/debconf-apt-progress.1*
%{_mandir}/man1/debconf-communicate.1*
%{_mandir}/man1/debconf-copydb.1*
%{_mandir}/man1/debconf-escape.1*
%{_mandir}/man1/debconf-set-selections.1*
%{_mandir}/man1/debconf-show.1*
%{_mandir}/man1/debconf.1*
%{_mandir}/man8/dpkg-preconfigure.8*
%{_mandir}/man8/dpkg-reconfigure.8*
%{_datadir}/pixmaps/debian-logo.png
%{_var}/cache/%{name}
%exclude %{perl_vendorlib}/Debconf/Element/Gnome*
%exclude %{perl_vendorlib}/Debconf/Element/Kde*
%exclude %{perl_vendorlib}/Debconf/FrontEnd/Gnome*
%exclude %{perl_vendorlib}/Debconf/FrontEnd/Kde*


%files gnome
%{perl_vendorlib}/Debconf/Element/Gnome*
%{perl_vendorlib}/Debconf/FrontEnd/Gnome*


%files kde
%{perl_vendorlib}/Debconf/Element/Kde*
%{perl_vendorlib}/Debconf/FrontEnd/Kde*


%files doc -f man-doc.lang
%doc samples/
%doc doc/CREDITS doc/README doc/README.LDAP doc/TODO
%doc debian/changelog
%doc debian/copyright
%doc doc/debconf.schema
%doc doc/hierarchy.txt
%doc doc/namespace.txt
%doc doc/passthrough.txt
%{_mandir}/man3/confmodule.3*
%{_mandir}/man5/debconf.conf.5*
%{_mandir}/man7/debconf-devel.7*
%{_mandir}/man7/debconf.7*


%files i18n -f man-i18n.lang -f debconf.lang
%doc debian/changelog debian/copyright debian/README.Debian


%files utils -f man-utils.lang
%doc debian/changelog debian/copyright debian/README.Debian
%{_bindir}/debconf-get-selections
%{_bindir}/debconf-getlang
%{_bindir}/debconf-loadtemplate
%{_bindir}/debconf-mergetemplate
%{_mandir}/man1/debconf-get-selections.1*
%{_mandir}/man1/debconf-getlang.1*
%{_mandir}/man1/debconf-loadtemplate.1*
%{_mandir}/man1/debconf-mergetemplate.1*


%changelog
* Thu Oct 10 2013 Sandro Mani <manisandro@gmail.com> - 1.5.51-1
- Update to 1.5.51
- Drop upstreamed patches
- Split off gnome and kde frontends to subpackages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5.49-4
- Perl 5.18 rebuild

* Sun Jun 09 2013 Oron Peled <oron@actcom.co.il> - 1.5.49-3
- Added missing /var/cache/debconf and initial contents

* Mon Jun 03 2013 Sérgio Basto <sergio@serjux.com> - 1.5.49-2
- Source rpms will have last 2 commits, which document better our patches.

* Wed Apr  3 2013 Oron Peled <oron@actcom.co.il> - 1.5.49-1
- Bump to version used by Debian/wheezy
- Fix 'find ... -perm' in Makefile to modern format. The deprecated
  format (+100) caused problems with find version >= 4.5.11
- Split 'make install' as is done in debian/rules for consistency

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.42-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.42-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1.5.42-6
- Perl 5.16 rebuild

* Sun May 13 2012 Oron Peled <oron@actcom.co.il> - 1.5.42-5
- Bump release to match f17, f16 builds

* Sat May 12 2012 Oron Peled <oron@actcom.co.il> - 1.5.42-4
- Fix find_lang for man-pages. It is not smart enough to do
  it all in one swoop. So we generate the expected results
  manually (during installation)
- Fix exclude of python3 (picked wrong directory on x86-64

* Tue May  1 2012 Oron Peled <oron@actcom.co.il> - 1.5.42-3
- Added --with-man and --all-name to find_lang
- Use wild-cards for language directories of man-pages 

* Thu Apr 12 2012 Oron Peled <oron@actcom.co.il> - 1.5.42-2
- Added find_lang stuff
- Don't specify man-pages compression
- Added BR python
- Added BR perl-Qt (for KDE frontend)

* Mon Mar 26 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.5.42-1
- New upstream version

* Tue Sep  7 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.5.32-4
- Fix available python interpreters (4)
- Fix %%install (4)
- Fix build requirements (3)
- Include doc, i18n and utils packages (2)
- First package (1)
