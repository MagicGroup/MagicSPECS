%global api_ver 0.24
%global priority 90

Name:           vala
Version:        0.23.2
Release:        1%{?dist}
Summary:        A modern programming language for GNOME

# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License:        LGPLv2+ and BSD
URL:            http://live.gnome.org/Vala
#VCS:           git:git://git.gnome.org/vala
# note: do not use a macro for directory name
# as it breaks Colin Walters' automatic build script
# see https://bugzilla.redhat.com/show_bug.cgi?id=609292
Source0:        http://download.gnome.org/sources/vala/0.23/vala-%{version}.tar.xz
Source1:        vala-mode.el
Source2:        vala-init.el
Source3:        emacs-vala-COPYING

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  glib2-devel
BuildRequires:  libxslt
# only if Vala source files are patched
# BuildRequires:  vala

# for Emacs modes
BuildRequires:  emacs emacs-el

# for tests
# BuildRequires:  dbus-x11

# alternatives
%global vala_binaries vala valac
%global vala_manpages valac
%global vala_tools_binaries vala-gen-introspect vapicheck vapigen
%global vala_tools_manpages vala-gen-introspect vapigen
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives


%description
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

valac, the Vala compiler, is a self-hosting compiler that translates
Vala source code into C source and header files. It uses the GObject
type system to create classes and interfaces declared in the Vala source
code. It's also planned to generate GIDL files when gobject-
introspection is ready.

The syntax of Vala is similar to C#, modified to better fit the GObject
type system.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains development files for %{name}. This is not
necessary for using the %{name} compiler.


%package        tools
Summary:        Tools for creating projects and bindings for %{name}
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gnome-common intltool libtool pkgconfig
Requires:       gobject-introspection-devel

%description    tools
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains tools to generate Vala projects, as well as API
bindings from existing C libraries, allowing access from Vala programs.


%package        doc
Summary:        Documentation for %{name}
License:        LGPLv2+

BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       devhelp

%description    doc
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains documentation in a devhelp HTML book.


%package -n emacs-%{name}
Summary:        Vala mode for Emacs
License:        GPLv2+

BuildArch:      noarch
Requires:       emacs(bin) >= %{_emacs_version}

%description -n emacs-%{name}
An Emacs mode for editing Vala source code.


%package -n emacs-%{name}-el
Summary:        Elisp source files for emacs-%{name}
License:        GPLv2+

BuildArch:      noarch
Requires:       emacs-%{name} = %{version}-%{release}

%description -n emacs-%{name}-el
This package contains the elisp source files for Vala under GNU
Emacs. You do not need to install this package to run Vala. Install
the emacs-%{name} package to use Vala with GNU Emacs.


%prep
%setup -q


%build
%configure
# Don't use rpath!
sed -i 's|/lib /usr/lib|/lib /usr/lib /lib64 /usr/lib64|' libtool
make %{?_smp_mflags}
# Compile emacs module
mkdir emacs-vala && cd emacs-vala && cp -p %{SOURCE1} .
%{_emacs_bytecompile} vala-mode.el
# and copy its licensing file
cp -p %{SOURCE3} COPYING


%install
make install DESTDIR=$RPM_BUILD_ROOT
# remove symlinks, using alternatives
for f in %{vala_binaries} %{vala_tools_binaries};
do
    rm $RPM_BUILD_ROOT%{_bindir}/$f
    touch $RPM_BUILD_ROOT%{_bindir}/$f
done
for f in %{vala_manpages} %{vala_tools_manpages};
do
    rm $RPM_BUILD_ROOT%{_mandir}/man1/$f.1*
    touch $RPM_BUILD_ROOT%{_mandir}/man1/$f.1.gz
done
# own this directory for third-party *.vapi files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vala/vapi
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Emacs mode files
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
cp -p emacs-vala/*.el* $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_emacs_sitestartdir}


%check
# make check


%posttrans
/sbin/ldconfig
for f in %{vala_binaries};
do
    %{_sbindir}/alternatives --install %{_bindir}/$f \
      $f %{_bindir}/$f-%{api_ver} %{priority}
done
for f in %{vala_manpages};
do
    %{_sbindir}/alternatives --install %{_mandir}/man1/$f.1.gz \
      $f.1.gz %{_mandir}/man1/$f-%{api_ver}.1.gz %{priority}
done

%posttrans tools
for f in %{vala_tools_binaries};
do
    %{_sbindir}/alternatives --install %{_bindir}/$f \
      $f %{_bindir}/$f-%{api_ver} %{priority}
done
for f in %{vala_tools_manpages};
do
    %{_sbindir}/alternatives --install %{_mandir}/man1/$f.1.gz \
      $f.1.gz %{_mandir}/man1/$f-%{api_ver}.1.gz %{priority}
done

%preun
/sbin/ldconfig
for f in %{vala_binaries};
do
    %{_sbindir}/alternatives --remove $f \
      %{_bindir}/$f-%{api_ver}
done
for f in %{vala_manpages};
do
    %{_sbindir}/alternatives --remove $f.1.gz \
      %{_mandir}/man1/$f-%{api_ver}.1.gz
done

%preun tools
for f in %{vala_tools_binaries};
do
    %{_sbindir}/alternatives --remove $f \
      %{_bindir}/$f-%{api_ver}
done
for f in %{vala_tools_manpages};
do
    %{_sbindir}/alternatives --remove $f.1.gz \
      %{_mandir}/man1/$f-%{api_ver}.1.gz
done


%files
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README THANKS
%ghost %{_bindir}/vala
%ghost %{_bindir}/valac
%{_bindir}/vala-%{api_ver}
%{_bindir}/valac-%{api_ver}
# owning only the directories, they should be empty
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala-%{api_ver}
%{_libdir}/libvala-%{api_ver}.so.*
%ghost %{_mandir}/man1/valac.1.gz
%{_mandir}/man1/valac-%{api_ver}.1.gz

%files devel
%{_includedir}/vala-%{api_ver}
%{_libdir}/libvala-%{api_ver}.so
%{_libdir}/pkgconfig/libvala-%{api_ver}.pc
# directory owned by filesystem
%{_datadir}/aclocal/vala.m4
%{_datadir}/vala/Makefile.vapigen

%files tools
%ghost %{_bindir}/vala-gen-introspect
%ghost %{_bindir}/vapicheck
%ghost %{_bindir}/vapigen
%{_bindir}/vala-gen-introspect-%{api_ver}
%{_bindir}/vapicheck-%{api_ver}
%{_bindir}/vapigen-%{api_ver}
%{_libdir}/vala-%{api_ver}
%{_datadir}/aclocal/vapigen.m4
%{_datadir}/pkgconfig/vapigen*.pc
%ghost %{_mandir}/man1/vala-gen-introspect.1.gz
%ghost %{_mandir}/man1/vapigen.1.gz
%{_mandir}/man1/vala-gen-introspect-%{api_ver}.1.gz
%{_mandir}/man1/vapigen-%{api_ver}.1.gz

%files doc
%doc %{_datadir}/devhelp/books/vala-%{api_ver}

%files -n emacs-%{name}
%doc emacs-vala/COPYING
%dir %{_emacs_sitelispdir}/%{name}
%{_emacs_sitelispdir}/%{name}/*.elc
%{_emacs_sitestartdir}/*.el

%files -n emacs-%{name}-el
%{_emacs_sitelispdir}/%{name}/*.el


%changelog
* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 0.23.2-1
- Update to 0.23.2

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.23.1-2
- Fix FTBFS

* Wed Jan 08 2014 Richard Hughes <rhughes@redhat.com> - 0.23.1-1
- Update to 0.23.1

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 0.22.1-1
- Update to 0.22.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 0.22.0-1
- Update to 0.22.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.21.2-1
- Update to 0.21.2

* Mon Aug 19 2013 Kalev Lember <kalevlember@gmail.com> - 0.21.1-1
- Update to 0.21.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Michel Salim <salimma@fedoraproject.org> - 0.20.1-1
- Update to 0.20.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 0.20.0-1
- Update to 0.20.0

* Thu Feb 28 2013 Colin Walters <walters@verbum.org> - 0.19.0-2
- Ensure tools pull in gobject-introspection-devel, since vapigen
  needs .gir files.

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 0.19.0-1
- Update to 0.19.0

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.18.1-4
- Temporarily BR vala itself to build with the patch applied

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.18.1-3
- Ignore the "instance-parameter" tag emitted by new g-ir-scanner

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 0.18.1-1
- Update to 0.18.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 0.18.0-1
- Update to 0.18.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 0.17.7-1
- Update to 0.17.7

* Sat Sep  8 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.6-1
- Update to 0.17.6

* Sun Sep  2 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.5-1
- Update to 0.17.5

* Mon Aug 20 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.4-1
- Update to 0.17.4

* Fri Aug  3 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.3-1
- Update to 0.17.3

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.2-1
- Update to 0.17.2

* Mon Jun  4 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.1-1
- Update to 0.17.1
- Remove "Group" field
- Make subpackages' dependencies on main package arch-specific

* Sat May 12 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.0-2
- Spec clean-ups

* Thu May  3 2012 Michel Salim <salimma@fedoraproject.org> - 0.17.0-1
- Update to 0.17.0

* Fri Apr  6 2012 Michel Salim <salimma@fedoraproject.org> - 0.16.0-3
- Disable coverage analysis, build-time paths get hard-coded

* Thu Apr  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.16.0-2
- Update vala-mode.el to April 2011 release
- Fix registration of Vala alternatives

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Tue Mar 27 2012 Ray Strode <rstrode@redhat.com> 0.15.2-2
- Add back Makefile.vapigen.  It's needed by various projects
  build systems to enable vala support.

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> - 0.15.2-1
- Update to 0.15.2

* Mon Feb  6 2012 Michel Salim <salimma@fedoraproject.org> - 0.15.1-3
- Enable coverage analysis
- Drop redundant --enable-vapigen, it's now the default

* Fri Feb  3 2012 Michel Salim <salimma@fedoraproject.org> - 0.15.1-2
- Support parallel installation with other Vala versions

* Mon Jan 30 2012 Michel Salim <salimma@fedoraproject.org> - 0.15.1-1
- Update to 0.15.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Matthias Clasen <mclasen@redhat.com> - 0.15.0-1
- Update to 0.15.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 0.13.3-1
- Update to 0.13.3

* Thu Jul  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.13.1-1
- Update to 0.13.1

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.12.1-1
- Update to 0.12.1

* Tue Apr  5 2011 Michel Salim <salimma@fedoraproject.org> - 0.12.0-2
- Allow access to length of constant array in constant initializer lists

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Thu Mar 17 2011 Michel Salim <salimma@fedoraproject.org> - 0.11.7-1
- Update to 0.11.7

* Mon Feb 21 2011 Peter Robinson <pbrobinson@gmail.com> - 0.11.6-1
- Update to 0.11.6

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.11.5-2
- Own %%{_datadir}/vala directory (# 661603)

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 0.11.5-1
- Update to 0.11.5

* Mon Jan 17 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.4-1
- Update to 0.11.4

* Fri Jan  7 2011 Peter Robinson <pbrobinson@gmail.com> - 0.11.3-1
- Update to 0.11.3
- disable make check as its currently broken

* Tue Nov  9 2010 Peter Robinson <pbrobinson@gmail.com> - 0.11.2-1
- Update to 0.11.2

* Sun Nov  7 2010 Michel Salim <salimma@fedoraproject.org> - 0.11.1-2
- Improved rpath handling, allowing test suite to run

* Sat Nov  6 2010 Michel Salim <salimma@fedoraproject.org> - 0.11.1-1
- Update to 0.11.1
- Drop unneeded build requirements

* Tue Oct 19 2010 Michel Salim <salimma@fedoraproject.org> - 0.11.0-1
- Update to 0.11.0

* Wed Sep 29 2010 jkeating - 0.10.0-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.10.0-1
- Update to 0.10.0
- Work with gobject-introspection >= 0.9.5

* Sun Sep 12 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.8-1
- Update to 0.9.8
- Make -doc subpackage noarch
- Mark -doc files as %%doc

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7.
- Remove clean section & buildroot. No longer needed.

* Mon Aug  9 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5

* Mon Aug  2 2010 Peter Robinson <pbrobinson@gmail.com> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 15 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3

* Mon Jul 12 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.2-2
- Add COPYING file to emacs-vala

* Sat Jul  3 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2

* Sun Jun 13 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1
- Make emacs-vala subpackage noarch; split off source file to -el subpackage
  according to Emacs packaging guidelines

* Tue Apr 27 2010 Michel Salim <salimma@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Fri Apr  9 2010 Peter Robinson <pbrobinson@gmail.com> - 0.8.0-1
- Update to new major release 0.8.0

* Tue Mar  2 2010 Peter Robinson <pbrobinson@gmail.com> - 0.7.10-1
- Update to 0.7.10

* Tue Jan  5 2010 Peter Robinson <pbrobinson@gmail.com> - 0.7.9-1
- Update to 0.7.9

* Tue Nov 17 2009 Peter Robinson <pbrobinson@gmail.com> - 0.7.8-1
- Update to 0.7.8

* Sat Oct  3 2009 Michel Salim <salimma@fedoraproject.org> - 0.7.7-1
- Update to 0.7.7

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 0.7.5-1
- Update to 0.7.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Michel Salim <salimma@fedoraproject.org> - 0.7.4-2
- Patch broken ModuleInit attribute (upstream bug 587444)

* Tue Jul  7 2009 Michel Salim <salimma@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4

* Wed Jun  3 2009 Peter Robinson <pbrobinson@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Sat Apr 18 2009 Michel Salim <salimma@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1

* Mon Feb 23 2009 Michel Salim <salimma@fedoraproject.org> - 0.5.7-1
- Update to 0.5.7

* Tue Jan 27 2009 Michel Salim <salimma@fedoraproject.org> - 0.5.6-1
- Update to 0.5.6

* Tue Dec 16 2008 Michel Salim <salimma@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3

* Mon Dec 15 2008 Michel Salim <salimma@fedoraproject.org> - 0.5.2-3
- Fix bug in Emacs version detection

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.5.2-2
- Use buildsystem variables to determine available Emacs version
- BR on gecko-devel >= 1.9, since older version is also in RHEL repo

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Sun Nov 23 2008 Michel Salim <salimma@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Fri Aug 22 2008 Michel Salim <salimma@fedoraproject.org> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 15 2008 Michel Salim <salimma@fedoraproject.org> - 0.3.4-2
- Add vala-mode for editing Vala code in Emacs

* Tue Jul  1 2008 Lennart Poettering <lpoetter@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Wed Jun  4 2008 Michel Salim <salimma@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3

* Fri May 16 2008 Michel Salim <salimma@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Thu Apr 10 2008 Michel Salim <salimma@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Wed Mar  5 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7
- -tool subpackage now requires gnome-common, intltool and libtoolize
  for out-of-the-box vala-gen-project support

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.6-2
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6
- Revert vapi addition, needed declarations have been inlined (r846)
- Rename -docs subpackage to -doc, to comply with guidelines

* Tue Jan 15 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.5-5
- Manually add Gee vapi file to package (bz #428692)

* Tue Dec  4 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.5-4
- Backport patch to autodetect location of automake shared files

* Tue Dec  4 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.5-3
- Add build dependency on gtk2-devel

* Tue Dec  4 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.5-2
- Enable project generator tool

* Tue Nov 27 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Sun Nov 11 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.4-2
- Add build dependency on devhelp

* Fri Oct 19 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4
- Put newly-added documentation in its own subpackage (depends on devhelp)

* Mon Sep 17 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.3-5
- vapigen subpackage: add missing Require: on perl-XML-Twig

* Sat Sep  8 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.3-4
- Split -vapigen subpackage. It is functionally self-contained and the license
  is more restricted
- Updated license declarations

* Wed Sep  5 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.3-3
- Licensing and URL updates

* Tue Sep  4 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.3-2
- Enable binding generation tools

* Sun Sep  2 2007 Michel Salim <salimma@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Sun Mar 25 2007 Michel Salim <salimma@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8

* Wed Mar  7 2007 Michel Salim <salimma@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7

* Wed Feb 28 2007 Michel Salim <salimma@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6

* Mon Nov  6 2006 Michel Salim <salimma@fedoraproject.org> - 0.0.5-1
- Initial package
