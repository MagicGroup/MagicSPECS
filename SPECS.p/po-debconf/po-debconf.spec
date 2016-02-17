
# Handle Debian +nmu<n> version suffixes
# As they are non-numeric we move them to the release part
# Per Fedora policy:
#   https://fedoraproject.org/wiki/Packaging:NamingGuidelines#Post-Release_packages
%global	posttag	nmu2
%global	release_posttag %{?posttag:.%{posttag}}
%global	tarball_posttag %{?posttag:+%{posttag}}
%global	debian_fqn %{name}_%{version}%{tarball_posttag}

# Some self tests are failing. For now make it optional.
# To try it, simply run: mock --with=check
%bcond_with check

Name:		po-debconf
Version:	1.0.16
Release:	5%{release_posttag}%{?dist}
Summary:	Tool for managing templates file translations with gettext
Summary(zh_CN.UTF-8):管理 gettext 使用的模板文件翻译的工具

Group:		Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:	GPLv2+
URL:		http://packages.debian.org/sid/po-debconf
Source0:	http://ftp.de.debian.org/debian/pool/main/p/%{name}/%{name}_%{version}%{tarball_posttag}.tar.gz
Patch0:		po-debconf-1.0.16-fix-prefix.patch

BuildArch:	noarch

BuildRequires:	po4a
BuildRequires:	dpkg-dev

# Needed for check
%if %{with check}
BuildRequires: perl(Test::Harness)
BuildRequires: debconf
BuildRequires: intltool
%endif

Requires:	perl
Requires:	intltool
Requires:	gettext
Requires:	html2text

# Debian optional run-time features
Requires:	perl(Compress::Zlib)
Requires:	perl(Mail::Sendmail)
Requires:	perl(Mail::Box::Manager)


%description
This package is an alternative to debconf-utils, and provides
tools for managing translated debconf templates files with
common gettext utilities.

%description -l zh_CN.UTF-8
管理 gettext 使用的模板文件翻译的工具。

%prep
%setup -q -n %{name}-%{version}%{tarball_posttag}
%patch0 -p1

# Fix upstream
chmod -x COPYING

%build
make %{?_smp_mflags}

%if %{with check}
%check
( cd ./tests && PODEBCONF_LIB=/usr/bin ./run.pl )
%endif

%install
mkdir -p \
	%{buildroot}/%{_bindir} \
	%{buildroot}/%{_datadir}/%{name}/

for prog in debconf-gettextize debconf-updatepo po2debconf podebconf-display-po podebconf-report-po; do
	install -pm 755 $prog %{buildroot}/%{_bindir}
done

# I don't know what to do with these
rm -rf doc/vi

for lang_man in `find doc/ -name "*.1" -exec dirname {} \; | sort -u`; do
	lang_id=$(basename $lang_man | sed -e 's/en//g')
	mkdir -p %{buildroot}/%{_mandir}/man1/
	mkdir -p "%{buildroot}/%{_mandir}/$lang_id/man1"
	for man in $lang_man/*.1; do
		dest_name=$(basename $man | sed -e "s/\.$lang_id\././")
		install -pm 644 "$man" "%{buildroot}/%{_mandir}/$lang_id/man1/$dest_name"
	done
done

install -pm 644 encodings %{buildroot}/%{_datadir}/%{name}
install -pm 644 pot-header %{buildroot}/%{_datadir}/%{name}/
cp -a podebconf-report-po_templates/ %{buildroot}/%{_datadir}/%{name}/templates
magic_rpm_clean.sh
%find_lang po-debconf --without-mo --with-man --all-name || :

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc COPYING README README-trans
%{_mandir}/man1/*.1*
%{_bindir}/debconf-gettextize
%{_bindir}/debconf-updatepo
%{_bindir}/po2debconf
%{_bindir}/podebconf-display-po
%{_bindir}/podebconf-report-po
%{_datadir}/%{name}

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0.16-5.nmu2
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.0.16-4.nmu2
- 为 Magic 3.0 重建

* Wed Aug 07 2013 Oron Peled <oron@actcom.co.il> - 1.0.16-3.nmu2
- Fixed build dependency
- Fix FTBFS in rawhide - bug #992741

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.0.16-2.nmu2
- Perl 5.18 rebuild

* Thu May  9 2013 Oron Peled <oron@actcom.co.il> - 1.0.16-1.nmu2
- Use same upstream version as Debian/wheezy
- Remove patch1 (no-utf8)
- Added more build-requires to enable features detected at build-time
- Preserve timestamps during installation (install -p)
- Prepare for 'check' -- some self-tests still fail

* Mon May 14 2012 Oron Peled <oron@actcom.co.il> - 1.0.16+nmu1-1
- Now debconf is in Fedora (#5913320). It provides the perl classes missing
  to install po-debconf.
- Installed translated man pages to correct names (without $LANG in the
  man-page name, only in the prefixing directory)
- Use find_lang for translated man-pages
- Don't specify exact compression scheme for (non-tranlated) man-pages
- Removed Build-Root (not needed for modern Fedora)

* Tue May 11 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.0.16-3
- Add requirement for html2text
- Add build requirement for debhelper
- First package
