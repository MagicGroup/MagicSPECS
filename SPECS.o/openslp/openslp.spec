
Summary: Open implementation of Service Location Protocol V2
Name:    openslp
Version: 1.2.1
Release: 17%{?dist}

Group:   System Environment/Libraries
License: BSD
URL:     http://sourceforge.net/projects/openslp/
Source:  http://dl.sourceforge.net/sourceforge/openslp/openslp-1.2.1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: slpd.init

Patch1:  openslp-1.2.1-optflags.patch
# slpd crashes if slptool findsrvtypes is run, when message logging is on
# http://bugzilla.redhat.com/523609
Patch2:  openslp-1.2.1-nullauth.patch

BuildRequires: automake libtool
BuildRequires: bison
BuildRequires: flex 
BuildRequires: openssl-devel

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.

%package devel
Summary: OpenSLP headers and libraries
Group:   Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
OpenSLP header files and libraries.

%package server
Summary: OpenSLP server daemon
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires(preun): chkconfig, /sbin/service
Requires(post): chkconfig
Requires(postun): /sbin/service
%description server
OpenSLP server daemon to dynamically register services.


%prep
%setup -q

%patch1 -p1 -b .optflags
%patch2 -p1 -b .nullauth

# tarball goof (?), it wants to re-automake anyway, so let's do it right.
#libtoolize --force
#aclocal
#autoconf
#automake --add-missing
autoreconf -f -i

# remove CVS leftovers...
find . -name "CVS" | xargs rm -rf


%build

# for x86_64
export CFLAGS="-fPIC $RPM_OPT_FLAGS"
# for slpd
export LDFLAGS="-pie"

%configure \
  --disable-dependency-tracking \
  --disable-static \
  --enable-slpv2-security
# --enable-async-api

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -p -D -m755  %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/slpd

# nuke unpackaged/unwanted files
rm -rf $RPM_BUILD_ROOT/usr/doc
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add slpd

%preun server
# on remove
if [ $1 -eq 0 ]; then
  /sbin/service slpd stop >/dev/null 2>&1 ||:
  /sbin/chkconfig --del slpd
fi

%postun server
# on upgrade
if [ $1 -gt 0 ]; then
  /sbin/service slpd condrestart >/dev/null 2>&1 ||:
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING FAQ NEWS README THANKS
%config(noreplace) %{_sysconfdir}/slp.conf
%{_bindir}/slptool
%{_libdir}/libslp.so.1*

%files server
%defattr(-,root,root)
%doc doc/html/IntroductionToSLP
%doc doc/html/UsersGuide
%doc doc/html/faq*
%{_sbindir}/slpd
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) %{_sysconfdir}/slp.spi
%config(noreplace) %{_initrddir}/slpd

%files devel
%defattr(-,root,root)
%doc doc/html/ProgrammersGuide
%doc doc/rfc
%{_includedir}/slp.h
%{_libdir}/libslp.so


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2.1-17
- 为 Magic 3.0 重建

* Fri Jan 20 2012 Liu Di <liudidi@gmail.com> - 1.2.1-16
- 为 Magic 3.0 重建

