Summary:   Tools for AppData files
Name:      appdata-tools
Version:   0.1.7
Release:   4%{?alphatag}%{?dist}
License:   GPLv2+
URL:       http://people.freedesktop.org/~hughsient/appdata/
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz

Requires: emacs-filesystem

BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: glib2-devel >= 2.25.9-2
BuildRequires: libsoup-devel
BuildRequires: gdk-pixbuf2-devel
#BuildRequires: trang
BuildRequires: python-lxml > 2.3
BuildRequires: emacs

%description
appdata-tools contains a command line program designed to validate AppData
application descriptions for standards compliance and to the style guide.

%prep
%setup -q

%build
%configure --disable-schemas
make %{?_smp_mflags}

%install
%make_install

%find_lang %name

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/appdata-validate
%{_mandir}/man1/appdata-validate.1.gz
%dir %{_datadir}/appdata/schema
%{_datadir}/appdata/schema/appdata.xsd
%{_datadir}/appdata/schema/appdata.rnc
#%{_datadir}/appdata/schema/appdata.rng
#%{_datadir}/appdata/schema/appdata.sch
%{_datadir}/appdata/schema/schema-locating-rules.xml
%{_datadir}/aclocal/appdata-xml.m4
%{_emacs_sitestartdir}/appdata-rng-init.el

%changelog
* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 0.1.7-4
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 0.1.7-3
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 0.1.7-2
- 为 Magic 3.0 重建

* Fri Jan 24 2014 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream release
- Add configure conditional to control validation
- Correct a validation warning when using a translated list
- Output the line and char number when printing problems
- Pass --nonet to appdata-validate in appdata-xml.m4
- Validate APPDATA_XML files during check phase

* Fri Nov 08 2013 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream release
- Fix up several warnings spotted when building with -Wformat
- Fix the schema install logic

* Fri Nov 08 2013 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release
- Add a style rule to require 300 chars of <p> content before <ul>
- Add an --output-format parameter that can optionally output HTML or XML
- Add simple APPDATA_XML m4 macro
- Allow GFDL as an acceptable content licence
- Generate appdata.rng from appdata.rnc at build time
- Host an online version of the AppData validation tool
- Ignore the <compulsory_for_desktop> private key
- Install included RELAX NG schema and make it automatically loadable by Emacs
- Support the 'codec' AppData kind
- Validate AppData files with metadata keys

* Mon Oct 07 2013 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream version
- Add some tests to validate <screenshots>
- Check the screenshots conform to the new size requirements
- Detect AppData files with missing copyright comments
- Detect files with missing XML headers

* Tue Sep 24 2013 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream version
- Add a rule that <li> tags should not end with a full stop
- Allow names and sumaries to end with '.' if there are multiple dots
- Detect if <application> is used more that once
- Support AppData files of other kinds

* Fri Sep 20 2013 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream version
- Add some more restrictions, and have different values for --relax
- Add --version, --verbose and --relax command line switches
- Allow short paragraphs when introducing a list
- Do not count translated paragraphs in the description check
- Do not fail to validate when the translatable tags are duplicated
- Require punctuation in the right places

* Wed Sep 18 2013 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream version
- Add an xsd file to validate the AppStream XML
- Allow <name> and <summary> data in appdata files
- Assign each problem a kind
- Detect starting a description with 'This application'
- Fail validation if tags are duplicated

* Tue Sep 17 2013 Richard Hughes <richard@hughsie.com> 0.1.0-1
- First version for Fedora package review
