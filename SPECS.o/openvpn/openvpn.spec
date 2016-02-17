%define _hardened_build 1
#define prerelease rc22

%define plugins down-root auth-pam

Name:              openvpn
Version:           2.3.2
Release:           6%{?prerelease:.%{prerelease}}%{?dist}
Summary:           A full-featured SSL VPN solution
Summary(zh_CN.UTF-8): 全功能的 SSL VPN 解决方案
URL:               http://openvpn.net/
#Source0:           http://openvpn.net/beta/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
#Source0:           https://secure.openvpn.net/beta/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
#Source0:           http://openvpn.net/release/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
Source0:	    http://swupdate.openvpn.org/community/releases/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz
#Source1:           https://secure.openvpn.net/beta/signatures/%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz.asc
Source1:            http://swupdate.openvpn.org/community/releases//%{name}-%{version}%{?prerelease:_%{prerelease}}.tar.gz.asc
# Sample 2.0 config files
Source2:           roadwarrior-server.conf
Source3:           roadwarrior-client.conf
# Systemd service
Source4:           openvpn@.service
# Tmpfile.d config
Source5:           %{name}-tmpfile.conf

# Don't start openvpn by default.
#Patch0:            openvpn-init.patch
#Patch1:            openvpn-script-security.patch
#Patch2:            openvpn-2.1.1-init.patch
#Patch3:            openvpn-2.1.1-initinfo.patch
License:           GPLv2
Group:             Applications/Internet
BuildRequires:     lzo-devel
BuildRequires:     openssl-devel
BuildRequires:     pam-devel
# For the perl_default_filter macro
BuildRequires:     perl-macros
BuildRequires:     pkcs11-helper-devel
BuildRequires:     systemd-units
# For /sbin/ip.
BuildRequires:     iproute
# For /sbin/ip.
Requires:          iproute
Requires(pre):     /usr/sbin/useradd
Requires(post):    systemd-sysv
Requires(post):    systemd-units
Requires(preun):   systemd-units
Requires(postun):  systemd-units

# Filter out the perl(Authen::PAM) dependency.
# No perl dependency is really needed at all.
%{?perl_default_filter}

%description
OpenVPN is a robust and highly flexible tunneling application that uses all
of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP or TCP
port.  It can use the Marcus Franz Xaver Johannes Oberhumer's LZO library
for compression.

%description -l zh_CN.UTF-8
全功能的 SSL VPN 解决方案。

%prep
%setup -q -n %{name}-%{version}%{?prerelease:_%{prerelease}}
#%patch0 -p0
#%patch1 -p1
#%patch2 -p0
#%patch3 -p0

sed -i -e 's,%{_datadir}/openvpn/plugin,%{_libdir}/openvpn/plugin,' doc/openvpn.8

# %%doc items shouldn't be executable.
find contrib sample -type f -perm /100 \
    -exec chmod a-x {} \;

%build
#  --enable-pthread        Enable pthread support (Experimental for OpenVPN 2.0)
#  --enable-password-save  Allow --askpass and --auth-user-pass passwords to be
#                          read from a file
#  --enable-iproute2       Enable support for iproute2
#  --with-ifconfig-path=PATH   Path to ifconfig tool
#  --with-iproute-path=PATH    Path to iproute tool
#  --with-route-path=PATH  Path to route tool
%configure \
    --enable-pthread \
    --enable-password-save \
    --enable-iproute2 \
    --with-iproute-path=/sbin/ip \
    --enable-plugins \
    --enable-plugin-down-root \
    --enable-plugin-auth-pam \
    --enable-pkcs11
%{__make}

## Build plugins
#for plugin in %{plugins} ; do
#    %{__make} -C src/plugins/$plugin
#done

%check
# Test Crypto:
./src/openvpn/openvpn --genkey --secret key
./src/openvpn/openvpn --test-crypto --secret key

# Randomize ports for tests to avoid conflicts on the build servers.
cport=$[ 50000 + ($RANDOM % 15534) ]
sport=$[ $cport + 1 ]
sed -e 's/^\(rport\) .*$/\1 '$sport'/' \
    -e 's/^\(lport\) .*$/\1 '$cport'/' \
    < sample/sample-config-files/loopback-client \
    > %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client
sed -e 's/^\(rport\) .*$/\1 '$cport'/' \
    -e 's/^\(lport\) .*$/\1 '$sport'/' \
    < sample/sample-config-files/loopback-server \
    > %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server

pushd sample
# Test SSL/TLS negotiations (runs for 2 minutes):
../src/openvpn/openvpn --config \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client &
../src/openvpn/openvpn --config \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server
wait
popd

rm -f %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-client \
    %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u})-loopback-server

%install
#install -D -m 0644 doc/%{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
#install -D -m 0755 src/openvpn/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/
rm -rf %{buildroot}%{_initrddir}
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
#cp -pR easy-rsa $RPM_BUILD_ROOT%{_datadir}/%{name}/
#rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/easy-rsa/Windows
cp %{SOURCE2} %{SOURCE3} sample/sample-config-files/

#mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/lib
#for plugin in %{plugins} ; do
#    install -m 0755 src/plugins/$plugin/openvpn-$plugin.so \
#        $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/lib/openvpn-$plugin.so
#    cp src/plugins/$plugin/README plugin/$plugin.txt
#done

%{__make} install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

# tmpfiles.d
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/%{name}/
magic_rpm_clean.sh

%pre
getent group openvpn &>/dev/null || groupadd -r openvpn
getent passwd openvpn &>/dev/null || \
    /usr/sbin/useradd -r -g openvpn -s /sbin/nologin -c OpenVPN \
        -d /etc/openvpn openvpn

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openvpn.service > /dev/null 2>&1 || :
    /bin/systemctl stop openvpn.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
# Normally, we'd try a restart here, but in this case, it could be troublesome.

%triggerun -- openvpn < 2.2.1-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply openvpn
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openvpn >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del openvpn >/dev/null 2>&1 || :
/bin/systemctl try-restart openvpn.service >/dev/null 2>&1 || :


%files
%doc AUTHORS COPYING COPYRIGHT.GPL INSTALL PORTS README
# Add NEWS when it isn't zero-length.
%doc src/plugins/*/README.*
%doc contrib sample
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
#%{_datadir}/%{name}/
%{_includedir}/openvpn-plugin.h
%{_libdir}/%{name}/
%{_unitdir}/%{name}@.service
%attr(0710,root,openvpn) %dir %{_localstatedir}/run/%{name}/
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%config %dir %{_sysconfdir}/%{name}/
%exclude %{_datadir}/doc/%{name}/

%changelog
* Sun Feb 14 2016 Liu Di <liudidi@gmail.com> - 2.3.2-6
- 为 Magic 3.0 重建

* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.3.2-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.3.2-4
- 为 Magic 3.0 重建

* Fri Apr 03 2015 Liu Di <liudidi@gmail.com> - 2.3.2-3
- 为 Magic 3.0 重建

* Fri Apr 03 2015 Liu Di <liudidi@gmail.com> - 2.3.2-2
- 为 Magic 3.0 重建

* Thu May 16 2013 Jon Ciesla <limburgher@gmail.com> 2.3.1-4
- chmod -x .service, BZ 963914.

* Thu May 16 2013 Jon Ciesla <limburgher@gmail.com> 2.3.1-3
- Enable --enable-pkcs11, BZ 963868.

* Mon Apr 08 2013 Kalev Lember <kalevlember@gmail.com> 2.3.1-2
- Update perl requires filtering

* Tue Apr 02 2013 Jon Ciesla <limburgher@gmail.com> 2.3.1-1
- 2.3.1, BZ 929402.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Jon Ciesla <limburgher@gmail.com> 2.3.0-1
- 2.3.0, BZ 893700.

* Wed Sep 26 2012 Jon Ciesla <limburgher@gmail.com> 2.2.2-9
- Dropped net-tools, BZ 785794.

* Wed Sep 05 2012 Jon Ciesla <limburgher@gmail.com> 2.2.2-8
- Dropped config from tmpfiles conf.

* Wed Sep 05 2012 Jon Ciesla <limburgher@gmail.com> 2.2.2-7
- Fix tmpfiles location, BZ 840188.
- Fix run ownership, BZ 854440.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Jon Ciesla <limburgher@gmail.com> 2.2.2-5
- Add hardened build.

* Mon Feb 13 2012 Jon Ciesla <limburgher@gmail.com> 2.2.2-4
- Use PrivateTmp=true, BZ 782522.

* Wed Feb  8 2012 Kay Sievers <kay@redhat.com> - 2.2.2-3
- Drop dependency on 'dev' package; it is gone since many years

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Jon Ciesla <limburgher@gmail.com> 2.2.2-1
- Update to 2.2.2.

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> 2.2.1-2
- convert to systemd

* Fri Jul 08 2011 Jon Ciesla <limb@jcomserv.net> 2.2.1-1
- Update to 2.2.1.

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> 2.2.0-2
- Bump and rebuild for BZ 712251.

* Thu May 19 2011 Jon Ciesla <limb@jcomserv.net> 2.2.0-1
- Update to 2.2.0.

* Thu Mar 17 2011 Jon Ciesla <limb@jcomserv.net> 2.1.4-1
- Update to 2.1.4.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 07 2010 Jon Ciesla <limb@jcomserv.net> 2.1.3-1
- Update to 2.1.3.

* Thu Aug 19 2010 Steven Pritchard <steve@kspei.com> 2.1.2-1
- Update to 2.1.2.

* Mon Jan 04 2010 Jon Ciesla <limb@jcomserv.net> 2.1.1-2
- Fix init script *.sh sourcing, BZ 498348.
- Added init script info block, BZ 392991, BZ 541219.

* Fri Dec 11 2009 Steven Pritchard <steve@kspei.com> 2.1.1-1
- Update to 2.1.1.

* Sat Nov 21 2009 Steven Pritchard <steve@kspei.com> 2.1-0.39.rc22
- Update to 2.1_rc22.

* Thu Nov 12 2009 Steven Pritchard <steve@kspei.com> 2.1-0.38.rc21
- Update to 2.1_rc21.

* Sun Oct 25 2009 Robert Scheck <robert@fedoraproject.org> 2.1-0.37.rc20
- Added script_security initialisation in initscript (#458594 #c20)

* Fri Oct 02 2009 Steven Pritchard <steve@kspei.com> 2.1-0.36.rc20
- Update to 2.1_rc20.

* Sun Sep 06 2009 Kalev Lember <kalev@smartlink.ee> - 2.1-0.35.rc19
- Update to 2.1_rc19
- Build with pkcs11-helper

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1-0.34.rc15
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.33.rc15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.32.rc15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.1-0.31.rc15
- rebuild with new openssl

* Thu Dec 11 2008 Steven Pritchard <steve@kspei.com> 2.1-0.30.rc15
- Attempt to fix BZ#476129.

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 2.1-0.29.rc15
- Update to 2.1_rc15

* Wed Aug 13 2008 Steven Pritchard <steve@kspei.com> 2.1-0.28.rc9
- Add "--script-security 2" by default for backwards compatibility
  (see bug #458594).

* Fri Aug 01 2008 Steven Pritchard <steve@kspei.com> 2.1-0.27.rc9
- Update to 2.1_rc9.

* Sat Jun 14 2008 Steven Pritchard <steve@kspei.com> 2.1-0.26.rc8
- Update to 2.1_rc8.
- Update License tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1-0.25.rc7
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Steven Pritchard <steve@kspei.com> 2.1-0.24.rc7
- Update to 2.1_rc7
- Drop BETA21-userpriv-fixups.patch (upstream)

* Fri Jan 25 2008 Steven Pritchard <steve@kspei.com> 2.1-0.23.rc6
- Apply update to BETA21-userpriv-fixups.patch from Alon Bar-Lev

* Thu Jan 24 2008 Steven Pritchard <steve@kspei.com> 2.1-0.22.rc6
- Update to 2.1_rc6
- Pass paths to ifconfig, ip, and route to configure
- BR iproute and Require iproute and net-tools
- Add BETA21-userpriv-fixups.patch from Alon Bar-Lev

* Wed Jan 23 2008 Steven Pritchard <steve@kspei.com> 2.1-0.21.rc5
- Update to 2.1_rc5

* Wed Dec 05 2007 Steven Pritchard <steve@kspei.com> 2.1-0.20.rc4
- Remove check macro cruft.

* Thu Apr 26 2007 Steven Pritchard <steve@kspei.com> 2.1-0.19.rc4
- Update to 2.1_rc4

* Mon Apr 23 2007 Steven Pritchard <steve@kspei.com> 2.1-0.18.rc3
- Update to 2.1_rc3

* Fri Mar 02 2007 Steven Pritchard <steve@kspei.com> 2.1-0.17.rc2
- Update to 2.1_rc2

* Tue Feb 27 2007 Steven Pritchard <steve@kspei.com> 2.1-0.16.rc1
- Randomize ports for tests to avoid conflicts on the build servers

* Tue Feb 27 2007 Steven Pritchard <steve@kspei.com> 2.1-0.15.rc1
- Update to 2.1_rc1

* Mon Oct 02 2006 Steven Pritchard <steve@kspei.com> 2.1-0.14.beta16
- Update to 2.1_beta16
- Drop Paul's patch (in upstream)

* Tue Sep 12 2006 Steven Pritchard <steve@kspei.com> 2.1-0.13.beta15
- Update to 2.1_beta15
- Add openvpn-2.1_beta15-test-timeout.patch to avoid test hang
  (from Paul Howarth)

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 2.1-0.12.beta14
- Rebuild

* Mon Jul 31 2006 Steven Pritchard <steve@kspei.com> 2.1-0.11.beta14
- Rebuild

* Fri Apr 14 2006 Steven Pritchard <steve@kspei.com> 2.1-0.10.beta14
- Update to 2.1_beta14

* Wed Apr 12 2006 Steven Pritchard <steve@kspei.com> 2.1-0.9.beta13
- Update to 2.1_beta13

* Wed Apr 05 2006 Steven Pritchard <steve@kspei.com> 2.1-0.8.beta12
- Update to 2.1_beta12 (BZ#188050/CVE-2006-1629)

* Tue Feb 21 2006 Steven Pritchard <steve@kspei.com> 2.1-0.7.beta11
- Update to 2.1_beta11

* Tue Feb 14 2006 Steven Pritchard <steve@kspei.com> 2.1-0.6.beta8
- Update to 2.1_beta8

* Wed Jan 04 2006 Steven Pritchard <steve@kspei.com> 2.1-0.5.beta7
- Man page shouldn't be executable (BZ#176953)

* Tue Dec 06 2005 Steven Pritchard <steve@kspei.com> 2.1-0.4.beta7
- Rebuild

* Fri Nov 18 2005 Steven Pritchard <steve@kspei.com> 2.1-0.3.beta7
- Update to 2.1_beta7

* Tue Nov 08 2005 Steven Pritchard <steve@kspei.com> 2.1-0.2.beta6
- Make sample-scripts (etc.) non-executable to avoid some dependencies

* Wed Nov 02 2005 Steven Pritchard <steve@kspei.com> 2.1-0.1.beta6
- Update to 2.1_beta6

* Mon Oct 17 2005 Steven Pritchard <steve@kspei.com> 2.1-0.1.beta4
- Update to 2.1_beta4

* Thu Aug 25 2005 Steven Pritchard <steve@kspei.com> 2.0.2-1
- Update to 2.0.2
- Refine roadwarrior-server.conf a bit

* Mon Aug 22 2005 Steven Pritchard <steve@kspei.com> 2.0.1-1
- Update to 2.0.1

* Mon Jun 27 2005 Steven Pritchard <steve@kspei.com> 2.0-2
- Move the plugin directory to _libdir
- Drop the easy-rsa/Windows directory
- Comment cleanups
- Add "processname" header to init script
- The init script isn't a config file
- Tag contrib, sample-config-files, sample-keys, and sample-scripts as doc
- Create/own pid dir

* Sat Jun 25 2005 Steven Pritchard <steve@kspei.com> 2.0-1
- Update to 2.0 final
- Drop Epoch: 0 and rebuild for Fedora Extras

* Wed Feb 16 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.14.rc13
- Fix/add paths to useradd

* Mon Feb 14 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.13.rc13
- Update to 2.0_rc13
- More spec cleanup (suggestions from Matthias Saou)

* Tue Feb 08 2005 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.12.rc12
- Update to 2.0_rc12
- Small spec cleanups
- Drop perl auto-requirements entirely

* Mon Dec 20 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.11.rc6
- Add down-root and auth-pam plugins
- Add --enable-password-save and --enable-iproute2
- Add crypto and loopback tests (somewhat time-consuming)

* Thu Dec 16 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.10.rc5
- Update to 2.0_rc5
- Change the port to 1194 in the roadwarrior-*.conf samples
- Change openvpn-init.patch to reformat the description in the init script
- Modify the Summary and description (OpenVPN isn't UDP-only)

* Tue Dec 14 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.9.rc1
- Remove the perl(Authen::PAM) dependency

* Thu Dec 09 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.8.rc1
- Update to 2.0_rc1

* Tue Nov 16 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.7.beta17
- Update to 2.0_beta17
- Require dev instead of /dev/net/tun (for udev compatibility)
- Change openvpn-init.patch to match upstream (starts even earlier now)

* Wed Aug 04 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.6.beta10
- Remove unnecessary BuildRequires: kernel-headers

* Tue Aug 03 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.5.beta10
- Update to 2.0_beta10
- Minor fix to configuration example
- Change the init script to start a little earlier and stop much later
  (after netfs) by default
- Remove a lot of unnecessary macro use (install/mkdir/cp)
- Don't create /dev/net/tun, use Requires instead

* Sat Jul 17 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.4.beta7
- Update to 2.0_beta7
- Include gpg signature in source rpm
- Include 2.0-style configuration examples
- Minor spec cleanup

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.3.test23
- Add openvpn-init.patch to leave the init script disabled by default

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.2.test23
- Fix URL and Source0
- Add an openvpn user

* Wed Apr 28 2004 Steven Pritchard <steve@kspei.com> 0:2.0-0.fdr.0.1.test23
- Update to 2.0_test23
- BuildRequires lzo-devel, kernel-headers, openssl-devel
- Lots of spec cleanup

* Sun Feb 23 2003 Matthias Andree <matthias.andree@gmx.de> 1.3.2.14-1
- Have the version number filled in by autoconf.

* Wed Jul 10 2002 James Yonan <jim@yonan.net> 1.3.1-1
- Fixed %%preun to only remove service on final uninstall

* Mon Jun 17 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.2.2-1
- Added condrestart to openvpn.spec & openvpn.init.

* Wed May 22 2002 James Yonan <jim@yonan.net> 1.2.0-1
- Added mknod for Linux 2.4.

* Wed May 15 2002 Doug Keller <dsk@voidstar.dyndns.org> 1.1.1.16-2
- Added init scripts
- Added conf file support

* Mon May 13 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.14-1
- Added new directories for config examples and such

* Sun May 12 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.13-1
- Updated buildroot directive and cleanup command
- added easy-rsa utilities

* Mon Mar 25 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.0-1
- Initial build.
