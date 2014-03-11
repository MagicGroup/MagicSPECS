Name:           munge
Version:        0.5.10
Release:        5%{?dist}
Summary:        Enables uid & gid authentication across a host cluster

Group:          Applications/System
License:        GPLv2+
URL:            http://munge.googlecode.com/
Source0:        http://munge.googlecode.com/files/munge-%{version}.tar.bz2
Source1:        create-munge-key
Source2:        munge.logrotate
Source3:        munged.service
Source4:        munged-tmpfiles.conf

BuildRequires:  systemd-units
BuildRequires:  zlib-devel%{?_isa} bzip2-devel%{?_isa} openssl-devel%{?_isa}
Requires:       munge-libs%{?_isa} = %{version}-%{release}

Requires(pre):    shadow-utils

Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description
MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating 
and validating credentials. It is designed to be highly scalable for use 
in an HPC cluster environment. 
It allows a process to authenticate the UID and GID of another local or 
remote process within a group of hosts having common users and groups. 
These hosts form a security realm that is defined by a shared cryptographic 
key. Clients within this security realm can create and validate credentials 
without the use of root privileges, reserved ports, or platform-specific 
methods.

%package devel
Summary:        Development files for uid * gid authentication acrosss a host cluster
Group:          Applications/System
Requires:       munge-libs%{?_isa} = %{version}-%{release}

%description devel
Header files for developing using MUNGE.

%package libs
Summary:        Runtime libs for uid * gid authentication acrosss a host cluster
Group:          Applications/System

%description libs
Runtime libraries for using MUNGE.


%prep
%setup -q
cp -p %{SOURCE1} create-munge-key
cp -p %{SOURCE2} munge.logrotate
cp -p %{SOURCE3} munged.service
cp -p %{SOURCE4} munged-tmpfiles.conf

%build
%configure  --disable-static
# Get rid of some rpaths for /usr/sbin
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} 


%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install extra files.
install -p -D -m 644 munged.service $RPM_BUILD_ROOT/%{_unitdir}/munged.service
install -p -D -m 644 munged-tmpfiles.conf $RPM_BUILD_ROOT/%{_sysconfdir}/tmpfiles.d/munged.conf
install -p -m 755 create-munge-key $RPM_BUILD_ROOT/%{_sbindir}/create-munge-key
install -p -D -m 644 munge.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/munge

# rm unneeded files.
rm $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/munge
rm $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/munge

# Exclude .la files 
rm $RPM_BUILD_ROOT/%{_libdir}/libmunge.la


# Fix a few permissions
chmod 700 $RPM_BUILD_ROOT%{_var}/lib/munge $RPM_BUILD_ROOT%{_var}/log/munge
chmod 700 $RPM_BUILD_ROOT%{_sysconfdir}/munge

# Create and empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record 
# of it is.
touch $RPM_BUILD_ROOT%{_var}/run/munge/munged.pid
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%postun 
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
   # Package upgrade, not uninstall
   /usr/bin/systemctl try-restart munged.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
   # Package removal, not upgrade
   /usr/bin/systemctl --no-reload disable munged.service > /dev/null 2>&1 || :
   /usr/bin/systemctl stop munged.service > /dev/null 2>&1 || :
fi

%pre
getent group munge >/dev/null || groupadd -r munge
getent passwd munge >/dev/null || \
useradd -r -g munge -d %{_var}/run/munge -s /sbin/nologin \
  -c "Runs Uid 'N' Gid Emporium" munge
exit 0


%post
if [ $1 -eq 1 ] ; then 
   # Initial installation 
   /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%triggerun -- munge < 0.5.10-3
# Save the current service runlevel info
/usr/bin/systemd-sysv-convert --save munge >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/usr/sbin/chkconfig --del munge >/dev/null 2>&1 || :
/usr/bin/systemctl try-restart munged.service >/dev/null 2>&1 || :

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/munge
%{_bindir}/remunge
%{_bindir}/unmunge
%{_sbindir}/munged
%{_sbindir}/create-munge-key
%{_mandir}/man1/munge.1.gz
%{_mandir}/man1/remunge.1.gz
%{_mandir}/man1/unmunge.1.gz
%{_mandir}/man7/munge.7.gz
%{_mandir}/man8/munged.8.gz
%{_unitdir}/munged.service

%attr(0700,munge,munge) %dir  %{_var}/log/munge
%attr(0700,munge,munge) %dir %{_sysconfdir}/munge
%attr(0755,munge,munge) %ghost %dir  %{_var}/run/munge
%attr(0644,munge,munge)    %ghost %{_var}/run/munge/munged.pid
%attr(0700,munge,munge) %dir  %{_var}/lib/munge

%config(noreplace) %{_sysconfdir}/tmpfiles.d/munged.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/munge

%doc AUTHORS BUGS ChangeLog    
%doc JARGON META NEWS QUICKSTART README 
%doc doc

%files libs
%{_libdir}/libmunge.so.2
%{_libdir}/libmunge.so.2.0.0
%doc COPYING

%files devel
%{_includedir}/munge.h
%{_libdir}/libmunge.so
%{_mandir}/man3/munge.3.gz
%{_mandir}/man3/munge_ctx.3.gz
%{_mandir}/man3/munge_ctx_copy.3.gz
%{_mandir}/man3/munge_ctx_create.3.gz
%{_mandir}/man3/munge_ctx_destroy.3.gz
%{_mandir}/man3/munge_ctx_get.3.gz
%{_mandir}/man3/munge_ctx_set.3.gz
%{_mandir}/man3/munge_ctx_strerror.3.gz
%{_mandir}/man3/munge_decode.3.gz
%{_mandir}/man3/munge_encode.3.gz
%{_mandir}/man3/munge_enum.3.gz
%{_mandir}/man3/munge_enum_int_to_str.3.gz
%{_mandir}/man3/munge_enum_is_valid.3.gz
%{_mandir}/man3/munge_enum_str_to_int.3.gz
%{_mandir}/man3/munge_strerror.3.gz


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.5.10-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 5 2012 Steve Traylen <steve.traylen@cern.ch> - 0.5.10-3
- Remove EPEL4 support since EOL.
- Change to systemd.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 27 2011 Steve Traylen <steve.traylen@cern.ch> - 0.5.10-1
- Upstream to 0.5.10
- Add _isa tags to all build requires.
- Remove unused patch munge-correct-service-name.patch, upstream fixed.
- Update and add check-key-exists.patch back.
- Revert back to default CFLAGS. _GNU_SOURCE not needed any more.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-4
- Upsteam is now hosted on google.
- Mark /var/run/munge as a %ghost file. #656631

* Sat Mar 27 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-3
- Release Bump
* Fri Mar 26 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-2
- Remove initd-pass-rpmlint.patch, has been applied upstream.
- Remove remove-GPL_LICENSED-cpp.patch, has been applied upstream.
* Fri Mar 26 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-1
- New upstream 0.5.9
* Wed Oct 21 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-8
- Requirment on munge removed from munge-libs.
- Explicit exact requirment on munge-libs for munge and munge-devel
  added.
* Wed Oct 21 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-7
- rhbz#530128 Move runtime libs to a new -libs package.
  ldconfig moved to new -libs package as a result.
* Sat Sep 26 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-6
- Patch for rhbz #525732 - Loads /etc/sysconfig/munge 
  correctly.
- Mark pid file as ghost file on oses that support that.
- Permisions on pid directory to 755

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.8-5
- rebuilt with new openssl

* Thu Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-4
- Expand defattr with 4th argument for default directory perms.
- Explict attr for non 0644 files and 0755 directories.

* Thu Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-3
- Append -DGNU_SOURCE to default CFLAGS.

* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-2
- Correct License to GPLv2+
- Move man3 pages to the devel package.
- Remove +x bit from create-munge-key source.
- Preserve timestamps when installing files.
- ldconfig not needed on -devel package.
- Do a condrestart when upgrading.
- Remove redundant files from docs.
- chmod /var/lib/munge /var/log/munge and /etc/munge to 700.
- Apply patch to not error when GPL_LICENSED is not set.
- Patch service script to print error on if munge.key not present
  on start only and with a better error. 
- Remove dont-exit-form-lib.patch. munge is expecting munge to
  do this.
- Remove libgcrypt-devel from BuildRequires, uses openssl by
  default anyway.
- Mark the munge.key as a ghost file.


* Fri Jun 12 2009 Steve Traylen <steve@traylen.net> - 0.5.8-1
- First Build


