%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

# Prevent RPM from stripping the binaries & debuginfo.
#
# NB: Only required because this package uses the obsolete -custom
# parameter and builds a bytecode 'ocamlrpcgen'.  I tried to fix the
# build to make a native code 'ocamlrpcgen' but the build system got
# the better of me.
%global debug_package %{nil}
%global __strip /bin/true

Name:           ocaml-ocamlnet
Version: 4.0.2
Release: 1%{?dist}
Summary:        Network protocols for OCaml
Summary(zh_CN.UTF-8): OCaml 的网络协议库
License:        BSD

URL:            http://projects.camlcity.org/projects/ocamlnet.html
Source0:        http://download.camlcity.org/download/ocamlnet-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.1-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-pcre-devel
BuildRequires:  ocaml-ssl-devel
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  ocaml-labltk-devel
BuildRequires:  ncurses-devel

%global __ocaml_requires_opts -i Asttypes -i Outcometree -i Parsetree


%description
Ocamlnet is an ongoing effort to collect modules, classes and
functions that are useful to implement network protocols. Since
version 2.2, Ocamlnet incorporates the Equeue, RPC, and Netclient
libraries, so it now really a big player.

In detail, the following features are available:

 * netstring is about processing strings that occur in network
   context. Features: MIME encoding/decoding, Date/time parsing,
   Character encoding conversion, HTML parsing and printing, URL
   parsing and printing, OO-representation of channels, and a lot
   more.

 * netcgi2 focuses on portable web applications.

 * rpc implements ONCRPC (alias SunRPC), the remote procedure call
   technology behind NFS and other Unix services.

 * netplex is a generic server framework. It can be used to build
   stand-alone server programs from individual components like those
   from netcgi2, nethttpd, and rpc.

 * netclient implements clients for HTTP (version 1.1, of course), FTP
   (currently partially), and Telnet.

 * equeue is an event queue used for many protocol implementations. It
   makes it possible to run several clients and/or servers in parallel
   without having to use multi-threading or multi-processing.

 * shell is about calling external commands like a Unix shell does.

 * netshm provides shared memory for IPC purposes.

 * netsys contains bindings for system functions missing in core OCaml.

 * smtp and pop are two further client implementations for the SMTP
   and POP3 protocols.

%description -l zh_CN.UTF-8
OCaml 的网络协议库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        nethttpd
Summary:        Ocamlnet HTTP daemon
Summary(zh_CN.UTF-8): OCamlnet 的 HTTP 服务
License:        GPLv2+
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    nethttpd
Nethttpd is a web server component (HTTP server implementation). It
can be used for web applications without using an extra web server, or
for serving web services.

%description nethttpd -l zh_CN.UTF-8
OCamlnet 的 HTTP 服务。

%package        nethttpd-devel
Summary:        Development files for %{name}-nethttpd
Summary(zh_CN.UTF-8): %{name}-nethttpd 的开发包
License:        GPLv2+
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-nethttpd = %{version}-%{release}


%description    nethttpd-devel
The %{name}-nethttpd-devel package contains libraries and signature
files for developing applications that use %{name}-nethttpd.

%description nethttpd-devel -l zh_CN.UTF-8
%{name}-nethttpd 的开发包。

%prep
%setup -q -n ocamlnet-%{version}


%build
# Parallel builds don't work:
unset MAKEFLAGS

./configure \
  -bindir %{_bindir} \
  -datadir %{_datadir}/%{name} \
  -disable-apache \
  -enable-pcre \
  -enable-gtk2 \
  -enable-gnutls \
  -enable-gssapi \
  -enable-nethttpd \
  -enable-tcl \
  -enable-zip


make all
%if %opt
make opt
%endif

%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $OCAMLFIND_DESTDIR/stublibs
make install

# rpc-generator/dummy.mli is empty and according to Gerd Stolpmann can
# be deleted safely.  This avoids an rpmlint warning.
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/rpc-generator/dummy.mli

# NB. Do NOT strip the binaries and prevent prelink from stripping them too.
# See comment at top of spec file.
mkdir -p $RPM_BUILD_ROOT/etc/prelink.conf.d
echo -e '-b /usr/bin/netplex-admin\n-b /usr/bin/ocamlrpcgen' \
  > $RPM_BUILD_ROOT/etc/prelink.conf.d/ocaml-ocamlnet.conf
magic_rpm_clean.sh

%files
%doc ChangeLog RELNOTES
%{_libdir}/ocaml/equeue
%{_libdir}/ocaml/equeue-gtk2
#%{_libdir}/ocaml/equeue-ssl
%{_libdir}/ocaml/equeue-tcl
%{_libdir}/ocaml/netcamlbox
%{_libdir}/ocaml/netcgi2
%{_libdir}/ocaml/netcgi2-plex
%{_libdir}/ocaml/netclient
#%{_libdir}/ocaml/netgssapi
%{_libdir}/ocaml/netmulticore
%{_libdir}/ocaml/netplex
%{_libdir}/ocaml/netshm
%{_libdir}/ocaml/netstring
%{_libdir}/ocaml/netsys
#%{_libdir}/ocaml/pop
%{_libdir}/ocaml/rpc
%{_libdir}/ocaml/rpc-auth-local
%{_libdir}/ocaml/rpc-generator
#%{_libdir}/ocaml/rpc-ssl
%{_libdir}/ocaml/shell
#%{_libdir}/ocaml/smtp
%{_libdir}/ocaml/netgss-system
%{_libdir}/ocaml/netstring-pcre
%{_libdir}/ocaml/nettls-gnutls
%{_libdir}/ocaml/netunidata
%{_libdir}/ocaml/netzip
%if %opt
%exclude %{_libdir}/ocaml/*/*.a
%exclude %{_libdir}/ocaml/*/*.cmxa
%exclude %{_libdir}/ocaml/*/*.cmx
%exclude %{_libdir}/ocaml/*/*.o
%endif
%exclude %{_libdir}/ocaml/*/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_datadir}/%{name}/
%{_bindir}/netplex-admin
%{_bindir}/ocamlrpcgen
%config(noreplace) /etc/prelink.conf.d/ocaml-ocamlnet.conf


%files devel
%defattr(-,root,root,-)
%doc ChangeLog RELNOTES
%if %opt
%{_libdir}/ocaml/*/*.a
%{_libdir}/ocaml/*/*.cmxa
%{_libdir}/ocaml/*/*.cmx
%{_libdir}/ocaml/*/*.o
%endif
%{_libdir}/ocaml/*/*.mli


%files nethttpd
%defattr(-,root,root,-)
%doc ChangeLog RELNOTES
#%{_libdir}/ocaml/nethttpd-for-netcgi2
%{_libdir}/ocaml/nethttpd
%if %opt
%exclude %{_libdir}/ocaml/*/*.a
%exclude %{_libdir}/ocaml/*/*.cmxa
%endif
%exclude %{_libdir}/ocaml/*/*.mli


%files nethttpd-devel
%defattr(-,root,root,-)
%doc ChangeLog RELNOTES
%if %opt
%{_libdir}/ocaml/*/*.a
%{_libdir}/ocaml/*/*.cmxa
%endif
%{_libdir}/ocaml/*/*.mli


%changelog
* Fri Mar 06 2015 Liu Di <liudidi@gmail.com> - 4.0.2-1
- 更新到 4.0.2

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 3.7.3-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 02 2013 Richard W.M. Jones <rjones@redhat.com> - 3.7.3-4
- Rebuild for ocaml-lablgtk 2.18.

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 3.7.3-3
- Unfortunately we have to re-add the anti-stripping code back.  See
  comment at top of spec file.
- Disable debuginfo for the same reason.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 3.7.3-1
- New upstream version 3.7.3.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Do not strip binaries, remove anti-prelink protection.
- Missing BR ncurses-devel.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Richard W.M. Jones <rjones@redhat.com> - 3.5.1-4
- Rebuild for OCaml 4.00.1.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 3.5.1-3
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 3.5.1-1
- New upstream version 3.5.1.
- Rebuild for OCaml 4.00.0, plus small patch.
- Move configure into build (not prep).

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 3.4.1-3
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 3.4.1-2
- Rebuild against PCRE 8.30

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 3.4.1-1
- New upstream version 3.4.1.
- Rebuild for OCaml 3.12.1.

* Mon Sep 19 2011 Richard W.M. Jones <rjones@redhat.com> - 3.4-1
- Move to new upstream 3.4 version.  Note this is not compatible with
  ocamlnet 2.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-23
- Rebuild against rpm-4.9.0-0.beta1.6.fc15.  See discussion:
  http://lists.fedoraproject.org/pipermail/devel/2011-February/148398.html

* Sat Feb  5 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-22
- Bump and rebuild because of broken deps on ocaml-lablgtk.

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-21
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).
- Missing BR ocaml-labltk-devel.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-19
- {gtk2,openssl,pcre,tcl}-devel BRs have now been pushed down to the
  corresponding ocaml-X-devel packages, so we don't need those here
  any more.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-18
- Use new dependency generator in upstream RPM 4.8.
- Add BR gtk2-devel.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-16
- Rebuild for OCaml 3.11.2.

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-15
- Force rebuild against newer lablgtk.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-13
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-11
- Rebuild against updated lablgtk.

* Wed Jan 21 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-10
- Fix prelink configuration file.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-9
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-8
- Rebuild for OCaml 3.11.0

* Tue Sep  2 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-7
- Prevent RPM & prelink from stripping bytecode.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-6
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-5
- New upstream URL.

* Mon Mar  3 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-4
- Do not strip binaries (bz 435559).

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-3
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-2
- Rebuild for OCaml 3.10.1.

* Wed Nov  7 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.9-1
- New upstream release 2.2.9.
- A more bletcherous, but more working, patch to fix the camlp4
  missing path bug.  Hopefully this is very temporary.
- Fixes for mock build under F8:
  + BR tcl-devel

* Thu Sep 13 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.8.1-1
- New upstream version 2.2.8.1.
- License of the base package is in fact BSD.  Clarified also that
  the license of nethttpd is GPLv2+.
- Removed the camlp4 paths patch as it doesn't seem to be necessary.
- Add BRs for camlp4, ocaml-pcre-devel, ocaml-lablgtk-devel,
  openssl-devel
- Removed explicit requires, they're not needed.
- Strip binaries and libraries.
- Ignore Parsetree module in deps.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-6
- ExcludeArch ppc64
- BR ocaml-pcre-devel
- Fix for camlp4 missing path

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-5
- Updated to latest packaging guidelines.

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-4
- Added support for ocaml-lablgtk2

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-3
- Remove empty file rpc-generator/dummy.mli.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-2
- Added support for SSL.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-1
- Initial RPM.
