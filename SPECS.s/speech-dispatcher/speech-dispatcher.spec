Name:          speech-dispatcher
Version:	0.8.3
Release:	2%{?dist}
Summary:       To provide a high-level device independent layer for speech synthesis
Summary(zh_CN.UTF-8): 语音合成用的高级设备无关层
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

# Almost all files are under GPLv2+, however 
# src/c/clients/spdsend/spdsend.h is licensed under GPLv2,
# which makes %%_bindir/spdsend GPLv2.
License:       GPLv2+ and GPLv2
URL:           http://devel.freebsoft.org/speechd
Source0:       http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
Source1:       http://www.freebsoft.org/pub/projects/sound-icons/sound-icons-0.1.tar.gz
Source2:       speech-dispatcherd.service
Patch0: 0001-RPM-Cleanups.patch

BuildRequires: alsa-lib-devel
BuildRequires: dotconf-devel
BuildRequires: espeak-devel
BuildRequires: flite-devel
Buildrequires: glib2-devel
Buildrequires: libao-devel
Buildrequires: libtool-ltdl-devel
Buildrequires: pulseaudio-libs-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: texinfo
BuildRequires: systemd
BuildRequires: automake libtool intltool

%ifnarch s390 s390x
BuildRequires: libraw1394
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: festival-freebsoft-utils
Obsoletes: python-speechd
Obsoletes: speech-dispatcher-python


%description
* Common interface to different TTS engines
* Handling concurrent synthesis requests – requests may come
  asynchronously from multiple sources within an application
  and/or from more different applications.
* Subsequent serialization, resolution of conflicts and
  priorities of incoming requests
* Context switching – state is maintained for each client
  connection independently, event for connections from
  within one application.
* High-level client interfaces for popular programming languages
* Common sound output handling – audio playback is handled by
  Speech Dispatcher rather than the TTS engine, since most engines
  have limited sound output capabilities.
%description -l zh_CN.UTF-8
语音合成用的高级设备无关层。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       speech-dispatcher = %{version}-%{release}
License:        GPLv2+

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:        Documentation for speech-dispatcher
Summary(zh_CN.UTF-8): %{name} 的文档
License:        GPLv2+
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       speech-dispatcher = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun):/sbin/install-info
BuildArch: noarch

%description doc
speechd documentation

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package -n python3-speechd
Summary:        Python 3 Client API for speech-dispatcher
Summary(zh_CN.UTF-8): %{name} 的 Python3 客户端 API
License:        GPLv2+
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       speech-dispatcher = %{version}-%{release}

%description -n python3-speechd
Python 3 module for speech-dispatcher
%description -n python3-speechd -l zh_CN.UTF-8
%{name} 的 Python3 客户端 API。

%prep
%setup -q
#%patch0 -p1
#autoreconf -vif

%build
%configure --disable-static --with-alsa --with-pulse \
  --with-flite --without-nas --without-libao \
  --sysconfdir=%{_sysconfdir} --with-default-audio-method=pulse

make %{?_smp_mflags} V=1

%install
for dir in \
 config/ doc/ include/ src/audio/ src/api/ src/modules/ src/tests/ src/server/ src/clients/
 do
  pushd $dir
  make install DESTDIR=%{buildroot} INSTALL="install -p"
 popd
done

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/

#Remove %{_infodir}/dir file
rm -f %{buildroot}%{_infodir}/dir

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Move the config files from /usr/share to /etc
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/modules
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/speechd.conf %{buildroot}%{_sysconfdir}/speech-dispatcher/
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/clients/* %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/modules/* %{buildroot}%{_sysconfdir}/speech-dispatcher/modules

# Create log dir
mkdir -p -m 0700 %{buildroot}%{_localstatedir}/log/speech-dispatcher/

# enable pulseaudio as default with a fallback to alsa
sed 's/# AudioOutputMethod "pulse,alsa"/AudioOutputMethod "pulse,alsa"/' %{buildroot}%{_sysconfdir}/speech-dispatcher/speechd.conf
magic_rpm_clean.sh

%post 
/sbin/ldconfig
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig

/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart speech-dispatcherd.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable speech-dispatcherd.service > /dev/null 2>&1 || :
    /bin/systemctl stop speech-dispatcherd.service > /dev/null 2>&1 || :
fi

%triggerun -- speech-dispatcherd < 0.7.1-6
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save speech-dispatcherd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del speech-dispatcherd >/dev/null 2>&1 || :
/bin/systemctl try-restart speech-dispatcherd.service >/dev/null 2>&1 || :

%files
%doc AUTHORS ChangeLog NEWS README COPYING
%dir %{_sysconfdir}/speech-dispatcher/
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%config(noreplace) %{_sysconfdir}/speech-dispatcher/speechd.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/clients/*.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/*.conf
%{_bindir}/*
%{_libdir}/libspeechd.so.*
%{_libdir}/speech-dispatcher-modules/
%dir %{_libdir}/speech-dispatcher
%{_libdir}/speech-dispatcher/spd*.so
%{_datadir}/sounds/speech-dispatcher
%{_datadir}/speech-dispatcher/conf/desktop/speechd.desktop

%dir %attr(0700, root, root) %{_localstatedir}/log/speech-dispatcher/

%{_unitdir}/speech-dispatcherd.service

%files devel
%{_includedir}/*
%{_libdir}/lib*.so

%files doc
%{_infodir}/*

%post doc
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/spd-say.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/ssip.info %{_infodir}/dir || :

%preun doc
if [ $1 = 0 ]; then
 /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
 /sbin/install-info --delete %{_infodir}/spd-say.info %{_infodir}/dir || :
 /sbin/install-info --delete %{_infodir}/ssip.info %{_infodir}/dir || :
fi

%files -n python3-speechd
%{python3_sitearch}/speechd*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 0.8.3-1
- 更新到 0.8.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 0.8-6
- 为 Magic 3.0 重建

* Tue Aug 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-5
- Install clients as not longer installed by default (fixes RHBZ 996337)

* Sat Aug 10 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8-4
- include/install missing headers

* Wed Aug  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-3
- Drop libao and python2 bindings

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-1
- Update to 0.8 stable release
- Rename python package for consistency
- Add python3 bindings - fixes RHBZ 867958
- Update the systemd scriptlets to the macroized versions

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Bastien Nocera <bnocera@redhat.com> 0.7.1-9
- Move RPM hacks to source patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
