%define java 0
Summary:		VNC server for the current X11 session
Summary(zh_CN.UTF-8):  当前 X11 会话的 VNC 服务
Name:		x11vnc
Version:		0.9.13
Release:		9%{?dist}
License:		GPLv2
Group:		User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL:			http://www.karlrunge.com/x11vnc/
Source0:		http://downloads.sourceforge.net/libvncserver/%{name}-%{version}.tar.gz

# Actually only /usr/bin/wish needed.
Requires:		tk
BuildRequires:	libjpeg-devel, zlib-devel, openssl-devel
BuildRequires:	xorg-x11-proto-devel, libXext-devel, libXtst-devel
BuildRequires:	libXfixes-devel, libvncserver-devel



# In Fedora 12 /usr/include/X11/extensions/XInput.h in libXi-devel but in
# previous versions in xorg-x11-proto-devel /usr/include/X11/extensions/shmproto.h
# placed in libXext-devel in F12 and in xorg-x11-proto-devel early.
BuildRequires:	libXi-devel libXext-devel
Requires:		Xvfb

# Fedora don't want hardcoded rpaths.
Patch1:		x11vnc-0.9.8-disableRpath.patch

# Package intended to EL-5 too, so we still need define BuildRoot
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
What WinVNC is to Windows x11vnc is to X Window System, i.e. a server
which serves the current X Window System desktop via RFB (VNC)
protocol to the user.

Based on the ideas of x0rfbserver and on LibVNCServer it has evolved into a
versatile and productive while still easy to use program.

%description -l zh_CN.UTF-8
当前 X 会话的 VNC 服务

# Required java not available on EL-5.ppc
%if 0%{?java}
%if ! ( (%{_arch}==ppc && 5 == 0%{?rhel}) || (%{_arch}==ppc64 && 6 == 0%{?rhel}) )
%package		javaviewers
Version:		%{version}
Summary:		VNC clients (browser java applets)
Requires:		%{name} = %{version}-%{release}
License:		GPLv2+
Group:		User Interface/X
# EL-5 does not support noarch subpackages ( https://fedorahosted.org/fedora-infrastructure/ticket/1772#comment:4 )
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
BuildArch: noarch
%endif
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	jpackage-utils

%description	javaviewers
The package contains the corresponding java clients for %{name}. They
can be used with any java-enabled browser and provide an easy access to
the server without the need to install software on the client machine.

%endif # EL.ppc
%endif

%prep
%setup -q
%patch1 -p0 -b .rpath

# fix source perms for the -debuginfo package rpmlint warnings
find -name "*.c" -o -name "*.h" -exec %{__chmod} 0644 {} \;

for file in README AUTHORS; do
	# ISO-8859-1 is my assumption.
	iconv -f ISO-8859-1 -t UTF-8 "$file" > "$file.new"
	touch --reference "$file" "$file.new"
	mv "$file.new" "$file"
done

# Delete prebuilt binaries
find -name '*.jar' -exec rm {} \;

%build
%configure --with-system-libvncserver --without-tightvnc-filetransfer

%if ! ( (%{java}==0) || (%{_arch}==ppc && 5 == 0%{?rhel}) || (%{_arch}==ppc64 && 6 == 0%{?rhel}) )
# First rebuild jars, what have been removed in %%prep.
pushd classes/ssl/src
%{__make} %{?_smp_mflags}
	# Alternative to patch Makefiles.
	for jarfile in *.jar; do
	%{__ln_s} src/$jarfile ../;
	%{__ln_s} ssl/src/$jarfile ../../;
	done
popd
%else
%{__rm} -rf classes
sed -ri 's/(DUST_)?SUBDIRS = x11vnc classes/\1SUBDIRS = x11vnc/' Makefile
%endif

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%if ! ( (%{java}==0) || (%{_arch}==ppc && 5 == 0%{?rhel}) || (%{_arch}==ppc64 && 6 == 0%{?rhel}) )
# And Java viewers
pushd classes/ssl
%{__make} install DESTDIR="%{buildroot}"
popd

# Rename README file to avoid name bump
%{__mv} classes/ssl/src/tight/README classes/ssl/src/tight/README.tight
%{__mv} classes/ssl/src/ultra/README classes/ssl/src/ultra/README.ultra
%endif

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_mandir}/man1/x11vnc.1*
%{_bindir}/x11vnc
%{_datadir}/applications/x11vnc.desktop

%if ! ( (%{java}==0) || (%{_arch}==ppc && 5 == 0%{?rhel}) || (%{_arch}==ppc64 && 6 == 0%{?rhel}) )
%files javaviewers
%defattr(-,root,root,-)
%doc classes/ssl/README classes/ssl/src/tight/README.tight classes/ssl/src/ultra/README.ultra
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/classes/ssl/README
%endif

%changelog
* Tue Oct 20 2015 Liu Di <liudidi@gmail.com> - 0.9.13-9
- 为 Magic 3.0 重建

* Sun Apr 14 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.13-8
- Add requires to tk (bz#920554).

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.9.13-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.9.13-5
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 0.9.13-3
- Resolves rhbz#794475
- Patch from Omair Majid <omajid@redhat.com> to remove explicit Java 6 req.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 11 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.13-1
- Update to 0.9.13 version (asked in bz#669780)
- Drop x11vnc-0.9.8-XShm-explicit-include.patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.12-17
- Update to last version 0.9.12 with hope it fix BZ#646694 and by request BZ#666612
- Change java related exclusion to El6 too.

* Sun Nov 1 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-16
- Noarch subpackage became only on Fedora
	( https://fedorahosted.org/fedora-infrastructure/ticket/1772#comment:4 )
- Also -javaviewers subpackage compleatly disabled on PPC arch on EL-5 because
	there no java-devel >= 1:1.6.0 and java-1.6.0-openjdk-devel.
	( https://fedorahosted.org/fedora-infrastructure/ticket/1772#comment:4 )

* Tue Oct 6 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-14
- Make -javaviewers subpackage noarch.

* Sun Oct 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-13
- Small fis requires release.
- Rename README file to avoid name bump

* Fri Sep 25 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-12
- Own %%{_datadir}/%%{name} instead of %%{_datadir}/%%{name}/classes
- Add Requires: %%{name} = %%{version}-%%{release} in subpackage.
- Change summary and description for javaviewers subpackage.
- Remove %%doc marker from man-page.
- %%defattr(-,root,root,0755) -> %%defattr(-,root,root,-)
- Add classes/ssl/src/tight/README classes/ssl/src/ultra/README files into
	javaviewers subpackage %%doc (thank you Orcan Ogetbil)
- ln -s replaced by %%{__ln_s}
- Set License: GPLv2+ for javaviewers subpackage (Thanks Spot)

* Mon Aug 31 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-11
- Remove all prebuilt *.jar-files in %%prep section and try build it from source.
- Add BR java-1.6.0-openjdk-devel
- Introduce new subpackage x11vnc-javaviewers.
- Add separate build java-viewers.
- Add Russian localized versions of Summary and descrioptions.

* Wed Aug 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-10
- Fix some spelling, change some cosmetic things.
- Delete Patch0 and hacks to link with system lzo package - it is not needed
	anymore as we link it with systel libvncserver instead.
- Delete BR lzo-devel
- Remiove empty directory %%{_datadir}/%%{name}/

* Sun Aug 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-9
- Add Requires: Xvfb

* Fri Aug 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-8
- Link to shared lzo instead of minilzo for all (not only EL-5).
- Add BuildRequires: /usr/include/X11/extensions/XShm.h
- Patch2: x11vnc-0.9.8-XShm-explicit-include.patch
- Step to conditional BR for Fedora 12, add
	Patch2: x11vnc-0.9.8-XShm-explicit-include.patch to build on it.

* Tue Aug 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-7
- Change license to GPLv2 without plus according to x11vnc.c
	source (thanks to Christian Krause).
- For consistency macros usage replace "ln -s" by %%{__ln_s},
	mv by %%{__mv} and similar (chmod, sed).
- Change find call to avoid using xargs in chmod sources command.

* Wed Jul 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-6
- Build with openssl unconditionally.
- Add Patch1: x11vnc-0.9.8-disableRpath.patch
- fix source perms for the -debuginfo package rpmlint warnings

* Tue Jul 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-5
- Try use lzo instead of minilzo in EL-5 (minilzo is not bundled in it).
- Try use system libvncserver library (--with-system-libvncserver
	configure option) instead of bundled one.
- System libvncserver built without tightvnc-filetransfer support.
	Now disable it there (--without-filetransfer)
	And according to it change License to only GPLv2+
	./configure --help misleading, using --without-tightvnc-filetransfer

* Tue Jul 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-4
- All changes inspired by started Fedora Review (thank you to Christian Krause).
- README and AUTHORS files converted into UTF-8.
- Explicit mention previous author in changelog and delet old entries of it.
- Source renamed to Source0.
- Source0 URL changed to long (correct) variant:
	http://downloads.sourceforge.net/libvncserver/%%{name}-%%{version}.tar.gz
	was http://dl.sf.net/libvncserver/x11vnc-%%{version}.tar.gz
- Add BR: /usr/include/X11/extensions/XInput.h; In F12 it is located in
	libXi-devel but in previous versions in xorg-x11-proto-devel
	so, to do not make conditional requires, require explicit file.
- Remove prebuild binaries clients.
- Remove Requires: minilzo it will be automatically propogated.
- Add BR: libvncserver-devel

* Fri Jul 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-3
- Add BR openssl-devel to provide SSL capability (thanks Manuel Wolfshant).
- Requires: minilzo, BR lzo-devel and Patch0: 
	11vnc-0.9.8-use-system-minilzo.patch to use system version of library.
- Add "and GPLv2" to License. See comment above why.
- Add BuildRequires: libXfixes-devel

* Fri Jul 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-2
- Import http://packages.sw.be/x11vnc/x11vnc-0.9.7-1.rf.src.rpm to maintain it in fedora:
	Packager: Dag Wieers <dag@wieers.com>
	Vendor: Dag Apt Repository, http://dag.wieers.com/apt/
- Step to version 0.9.8
- Reformat spec with tabs.
- Comment out (leave for history) Packager and Vendor tags
- Remove defines of several macros like dtag, conditional _without_modxorg
- Remove all stuff around conditional build _without_modxorg
- Add -%%(%%{__id_u} -n) part into buildroot.
- Make setup quiet.
- Remove "rf" Release suffix and replace it by %%{?dist}
- License from GPL changed to GPLv2+
