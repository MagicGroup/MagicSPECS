%define goldcgidir	%{_datadir}/%{name}-%{version}
%define golddatadir	%{_localstatedir}/lib/%{name}

Name:		gold
Version:	2.1.12.2
Release:	12%{?dist}
Summary:	Tracks and manages resource usage on High Performance Computers
Vendor:		Cluster Resources
Group:		Applications/Internet
License:	BSD
URL:		http://www.clusterresources.com/products/%{name}
Source0:	http://www.clusterresources.com/downloads/%{name}/%{name}-%{version}.tar.gz
# These patches are to make it build happily under rpm and mock - they have
# been submitted upstream (see the thread at
# http://www.supercluster.org/pipermail/gold-users/2010-July/000343.html for
# more info).
Patch0:		gold-makefile.patch
Patch1:		gold-configure-ac.patch

BuildArch:	noarch 
Requires(pre):	shadow-utils
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	sqlite

# For some reason, these requires are missed:
Requires:	perl(Data::Properties)
Requires:	perl(Crypt::DES_EDE3)

BuildRequires:	autoconf
BuildRequires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Gold Allocation Manager is an open source accounting system developed by
Pacific Northwest National Laboratory (PNNL) as part of the Department of
Energy (DOE) Scalable Systems Software Project (SSS). It tracks resource usage
on High Performance Computers and acts much like a bank, establishing accounts
in order to pre-allocate user and project resource usage over specific nodes and
time-frame. Gold provides balance and usage feedback to users, managers, and
system administrators.  SQLite is used by default, but Gold can be configured
to use either MySQL or PostgreSQL instead.

%package web
Summary:			Gold Allocation Manager Web Frontend
Group:				Applications/Internet
Requires:			%{name} = %{version}-%{release}
Requires:			webserver
Requires:			perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description web
CGI Perl web front-end for the Gold Allocation Manager.

%package doc
Summary:			Gold Allocation Manager Documentation
Group:				Documentation

%description doc
Documentation for the Gold Allocation Manager.

%prep 
%setup -q
%patch0
%patch1
# Regenerate configure script
autoconf -f -o configure

%build
%configure \
	--with-user=gold --with-db=SQLite \
	--with-doc-dir=%{_docdir}/%{name}-%{version} \
	--with-perl-libs=vendor --with-gold-libs=vendor --with-cgi-bin=%{goldcgidir} \
	--datadir=%{golddatadir}
make %{?_smp_mflags}
make %{?_smp_mflags} gui

# Prevent spurious requirement on Postgres DBD class
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(DBD::Pg)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%install
## Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}

## Install binaries
mkdir -p %{buildroot}%{golddatadir}
mkdir -p %{buildroot}%{perl_vendorlib}
make install DESTDIR=%{buildroot}

## Install web gui
make install-gui DESTDIR=%{buildroot}

# TODO
#make auth_key DESTDIR=%{buildroot}

# Clean up things that shouldn't have been installed
rm %{buildroot}%{perl_vendorlib}/Gold/*.pm.in

# Fix non UTF-8 files(preserving timestamps)
for i in README LICENSE;
do
	iconv -f iso8859-1 -t utf8 $i >$i.utf8
	touch -r $i $i.utf8
	mv $i.utf8 $i
done

# TODO Separate out the gold server and client packages

# TODO Work out why init script isn't installing - in src/etc/gold.d.in
# TODO chkconfig --add gold
# TODO Patch Perl in /usr/sbin/goldd to use the passed in pid file and not the
# hard coded one!!
# TODO Patch Perl in /usr/sbin/goldd to use the correct path for the /etc/
# files!
# TODO Patch Perl in Gold.pm and others too as paths to the config files are
# incorrect.
# TODO Correct init script to use the correct path for the pid file -
# /var/run/gold/gold.pid or /var/run/gold.pid

# TODO Correct goldsh so that the gold_history file isn't in a hard-coded
# location in /usr/log/.gold_history or similar

# TODO Sort out the authkey: ${GOLD_HOME}/etc/auth_key (line 220 of
# /usr/sbin/goldd)

# TODO On the client end, make sure the default logging is to use syslog, and
# that this is honoured in all the places it is currently hard-coded!

# TODO The gold*.conf config files need to have their permissions changed so
# that they belong to the gold user and group and are chmod 600 or similar as
# they will contain database usernames and passwords.

# TODO Change the server name set in the config files
# TODO Change the log location set in the config files
# TODO Change the logging level set in the config files

# The server configuration file is goldd.conf
# The client is 
# The web interface configuration file is 
magic_rpm_clean.sh

%check
# This target, although it exists, does nothing at present
make test

%pre
## Add the "gold" group
getent group gold >/dev/null || groupadd -r gold
## Add the "gold" user
getent passwd gold >/dev/null || \
/usr/sbin/useradd -c "Gold Allocation Manager" -g gold \
	-s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} gold 
exit 0

%preun
if [ "$1" = 0 ]
then
	/sbin/service gold stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del gold
fi

%files
%defattr(-,root,root,-)
%doc LICENSE
%dir %{golddatadir}
%dir %{perl_vendorlib}/Gold
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_sbindir}/*
%{perl_vendorlib}/Gold.pm
%{perl_vendorlib}/Gold/*.pm

%files doc
%defattr(-,root,root,-)
%doc README INSTALL LICENSE DATABASE CHANGES doc/
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*

%files web
%defattr(-,root,root,-)
%doc LICENSE
%dir %{goldcgidir}
%{goldcgidir}/*

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 2.1.12.2-12
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.1.12.2-11
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.1.12.2-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1.12.2-7
- Rebuild for new perl, cleanup spec file

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.1.12.2-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 12 2010 Jessica Jones <fedora@zaniyah.org> 2.1.12.2-4
- Changed summary to something more comprehensible
- Updated description to include full package name

* Tue Aug  3 2010 Jessica Jones <fedora@zaniyah.org> 2.1.12.2-3
- Attempt to fix Perl dependencies

* Wed Jul 28 2010 Jessica Jones <fedora@zaniyah.org> 2.1.12.2-2
- Convert README and LICENSE to UTF-8
- Change file list to include %conf directive for config files
- Remove duplicate files from file list
- Remove unnecessary documentation from web and main packages
- Add test step
- Remove unnecessary Perl tests

* Thu Jul 01 2010 Jessica Jones <fedora@zaniyah.org> 2.1.12.2-1
- Initial build for EPEL 5
