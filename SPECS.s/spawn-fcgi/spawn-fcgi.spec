Summary: Simple program for spawning FastCGI processes
Name: spawn-fcgi
Version: 1.6.3
Release: 3%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://redmine.lighttpd.net/projects/spawn-fcgi/
Source0: http://www.lighttpd.net/download/spawn-fcgi-%{version}.tar.bz2
Source1: spawn-fcgi.init
Source2: spawn-fcgi.sysconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Note that restarting automatically upon update makes no sense at all here
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig

%description
This package contains the spawn-fcgi program used for spawning FastCGI
processes, which can be local or remote.


%prep
%setup -q


%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/init.d/spawn-fcgi
%{__install} -D -p -m 0600 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/spawn-fcgi


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/chkconfig --add spawn-fcgi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service spawn-fcgi stop &>/dev/null || :
    /sbin/chkconfig --del spawn-fcgi
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/init.d/spawn-fcgi
%config(noreplace) %{_sysconfdir}/sysconfig/spawn-fcgi
%{_bindir}/spawn-fcgi
%{_mandir}/man1/spawn-fcgi.1*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6.3-3
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 30 2009 Matthias Saou <http://freshrpms.net/> 1.6.3-1
- Update to 1.6.3.
- Include init script and sysconfig file to make it easy to manage a single
  instance.

* Tue Apr 21 2009 Matthias Saou <http://freshrpms.net/> 1.6.2-1
- Update to 1.6.2.
- Remove leftover -f from %%files section.

* Mon Mar 30 2009 Matthias Saou <http://freshrpms.net/> 1.6.1-1
- Initial RPM release.

