%{!?python_site: %define python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.1.4
Release: 5%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Source1: autogen.sh

# Remove with 2.1.5
Patch1:  0001-reporter-bugzilla-support-new-format-keyword-reporte.patch
Patch2:  0002-reporter-bugzilla-remove-recently-added-aux.-files-f.patch
Patch3:  0003-do-not-build-or-install-any-piece-of-BZ-when-without.patch
Patch4:  0004-do-not-build-or-install-BZ-dependencies-when-without.patch
Patch6:  0006-updated-translation.patch
Patch8:  0008-create-last_occurrence-at-the-time-of-the-first-cras.patch

BuildRequires: dbus-devel
BuildRequires: gtk3-devel
BuildRequires: curl-devel
BuildRequires: desktop-file-utils
BuildRequires: xmlrpc-c-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: libtar-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: nss-devel
BuildRequires: texinfo
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: newt-devel
BuildRequires: libproxy-devel
BuildRequires: btparser-devel
BuildRequires: doxygen
Requires: libreport-filesystem = %{version}-%{release}
# required for update from old report library, otherwise we obsolete report-gtk
# and all it's plugins, but don't provide the python bindings and the sealert
# end-up with: can't import report.GtkIO
# FIXME: can be removed when F15 will EOLed, needs to stay in rhel6!
Requires: libreport-python = %{version}-%{release}
Conflicts: abrt < 2.1.0

# for rhel6
%if 0%{?rhel} == 6
BuildRequires: gnome-keyring-devel
%else
BuildRequires: libgnome-keyring-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libraries providing API for reporting different problems in applications
to different bug targets like Bugzilla, ftp, trac, etc...

%package filesystem
Summary: Filesystem layout for libreport
Group: Applications/File

%description filesystem
Filesystem layout for libreport

%package devel
Summary: Development libraries and headers for libreport
Group: Development/Libraries
Requires: libreport = %{version}-%{release}

%description devel
Development libraries and headers for libreport

%package web
Summary: Library providing network API for libreport
Group: Libraries
Requires: libreport = %{version}-%{release}

%description web
Library providing network API for libreport

%package web-devel
Summary: Development headers for libreport-web
Group: Development/Libraries
Requires: libreport-web = %{version}-%{release}

%description web-devel
Development headers for libreport-web

%package python
Summary: Python bindings for report-libs
# Is group correct here? -
Group: System Environment/Libraries
Requires: libreport = %{version}-%{release}
Provides: report = 0:0.23-1
Obsoletes: report < 0:0.23-1
# in report the rhtsupport is in the main package, so we need to install it too
%if 0%{?rhel} >= 6
Requires: libreport-plugin-rhtsupport
%endif

%description python
Python bindings for report-libs.

%package cli
Summary: %{name}'s command line interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package newt
Summary: %{name}'s newt interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Provides: report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary: GTK front-end for libreport
Group: User Interface/Desktops
Requires: libreport = %{version}-%{release}
Requires: libreport-plugin-reportuploader = %{version}-%{release}
%if 0%{?rhel} >= 6
%else
Requires: pygobject3
%endif
Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary: Development libraries and headers for libreport
Group: Development/Libraries
Requires: libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%package plugin-kerneloops
Summary: %{name}'s kerneloops reporter plugin
Group: System Environment/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-kerneloops
This package contains plugin which sends kernel crash information to specified
server, usually to kerneloops.org.

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-logger < 2.0.4
Provides: report-plugin-localsave = 0:0.23-1
Obsoletes: report-plugin-localsave < 0:0.23-1
Provides: report-config-localsave = 0:0.23-1
Obsoletes: report-config-localsave < 0:0.23-1

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-mailx
Summary: %{name}'s mailx reporter plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: mailx
Obsoletes: abrt-plugin-mailx < 2.0.4

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%package plugin-bugzilla
Summary: %{name}'s bugzilla plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}
Obsoletes: abrt-plugin-bugzilla < 2.0.4
Provides: report-plugin-bugzilla = 0:0.23-1
Obsoletes: report-plugin-bugzilla < 0:0.23-1
Provides: report-config-bugzilla-redhat-com = 0:0.23-1
Obsoletes: report-config-bugzilla-redhat-com < 0:0.23-1

%package plugin-ureport
Summary: %{name}'s micro report plugin
BuildRequires: json-c-devel
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-ureport
Uploads micro-report to abrt server

%description plugin-bugzilla
Plugin to report bugs into the bugzilla.

%package plugin-rhtsupport
Summary: %{name}'s RHTSupport plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}
Obsoletes: abrt-plugin-rhtsupport < 2.0.4

%description plugin-rhtsupport
Plugin to report bugs into RH support system.

%package compat
Summary: %{name}'s compat layer for obsoleted 'report' package
Group: System Environment/Libraries
Requires: libreport = %{version}-%{release}
Requires: %{name}-plugin-bugzilla = %{version}-%{release}
Requires: %{name}-plugin-rhtsupport = %{version}-%{release}

%description compat
Provides 'report' command-line tool.

%package plugin-reportuploader
Summary: %{name}'s reportuploader plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}
Obsoletes: abrt-plugin-reportuploader < 2.0.4
Provides: report-plugin-ftp = 0:0.23-1
Obsoletes: report-plugin-ftp < 0:0.23-1
Provides: report-config-ftp = 0:0.23-1
Obsoletes: report-config-ftp < 0:0.23-1
Provides: report-plugin-scp = 0:0.23-1
Obsoletes: report-plugin-scp < 0:0.23-1
Provides: report-config-scp = 0:0.23-1
Obsoletes: report-config-scp < 0:0.23-1

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%package fedora
Summary: Default configuration for reporting bugs via Fedora infrastructure
Group: Applications/File

%description fedora
Default configuration for reporting bugs via Fedora infrastructure
used to easy configure the reporting process for Fedora sytems. Just
install this package and you're done.

%package rhel
Summary: Default configuration for reporting bugs via Red Hat infrastructure
Group: Applications/File

%description rhel
Default configuration for reporting bugs via Red Hat infrastructure
used to easy configure the reporting process for Red Hat sytems. Just
install this package and you're done.

%package anaconda
Summary: Default configuration for reporting anaconda bugs
Group: Applications/File
Requires: libreport-plugin-reportuploader
Requires: libreport-plugin-bugzilla

%description anaconda
Default configuration for reporting Anaconda problems using Fedora
infrastructure or uploading the gathered data over ftp/scp...

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch8 -p1
# koji in f19 has new autotools, so we need to regenerate everything
cp %SOURCE1 %_builddir/%{name}-%{version}
./autogen.sh

%build
# Commented because of deprecated GTK API
#CFLAGS="%{optflags} -Werror" %configure --disable-silent-rules
CFLAGS="%{optflags}" %configure --enable-doxygen-docs --disable-silent-rules
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
%find_lang %{name}

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/events.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/events/

# After everything is installed, remove info dir
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%post gtk
/sbin/ldconfig
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun gtk
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/forbidden_words.conf
%{_libdir}/libreport.so.*
%{_libdir}/libabrt_dbus.so.*
%{_mandir}/man5/report_event.conf.5*

%files filesystem
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%dir %{_sysconfdir}/%{name}/plugins/

%files devel
%defattr(-,root,root,-)
# Public api headers:
%doc apidoc/html/*
%{_includedir}/libreport/libreport_types.h
%{_includedir}/libreport/client.h
%{_includedir}/libreport/dump_dir.h
%{_includedir}/libreport/event_config.h
%{_includedir}/libreport/problem_data.h
%{_includedir}/libreport/report.h
%{_includedir}/libreport/run_event.h
%{_includedir}/libreport/file_obj.h
%{_includedir}/libreport/config_item_info.h
%{_includedir}/libreport/workflow.h
# Private api headers:
%{_includedir}/libreport/internal_abrt_dbus.h
%{_includedir}/libreport/internal_libreport.h
%{_includedir}/libreport/xml_parser.h
%{_libdir}/libreport.so
%{_libdir}/libabrt_dbus.so
%{_libdir}/pkgconfig/libreport.pc
%dir %{_includedir}/libreport

%files web
%defattr(-,root,root,-)
%{_libdir}/libreport-web.so*

%files web-devel
%defattr(-,root,root,-)
%{_includedir}/libreport/libreport_curl.h
%{_libdir}/pkgconfig/libreport-web.pc

%files python
%defattr(-,root,root,-)
%{python_sitearch}/report/*
%{python_sitearch}/reportclient/*

%files cli
%defattr(-,root,root,-)
%{_bindir}/report-cli
%{_mandir}/man1/report-cli.1.gz

%files newt
%defattr(-,root,root,-)
%{_bindir}/report-newt

%files gtk
%defattr(-,root,root,-)
%{_bindir}/report-gtk
%{_libexecdir}/abrt-screencast
%{_libdir}/libreport-gtk.so.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/emergencyanalysis_event.conf
%{_sysconfdir}/libreport/events/report_EmergencyAnalysis.xml


%files gtk-devel
%defattr(-,root,root,-)
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%files plugin-kerneloops
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/events/report_Kerneloops.xml
%{_mandir}/man*/reporter-kerneloops.*
%{_bindir}/reporter-kerneloops

%files plugin-logger
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/events/report_Logger.conf
%{_sysconfdir}/libreport/events/report_Logger.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%{_bindir}/reporter-print
%{_mandir}/man*/reporter-print.*

%files plugin-mailx
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/mailx.conf
%{_sysconfdir}/libreport/events/report_Mailx.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/mailx_event.conf
%{_mandir}/man*/reporter-mailx.*
%{_bindir}/reporter-mailx

%files plugin-ureport
%defattr(-,root,root,-)
%{_bindir}/reporter-ureport
#%{_mandir}/man1/reporter-ureport.1.gz
%{_sysconfdir}/libreport/events/report_uReport.xml

%files plugin-bugzilla
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_kernel.conf
%{_sysconfdir}/libreport/events/report_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
# FIXME: remove with the old gui
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_bindir}/reporter-bugzilla

%files plugin-rhtsupport
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/rhtsupport.conf
%{_sysconfdir}/libreport/events/report_RHTSupport.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/rhtsupport_event.conf
%{_mandir}/man1/reporter-rhtsupport.1.gz
%{_bindir}/reporter-rhtsupport

%files compat
%defattr(-,root,root,-)
%{_bindir}/report
%{_mandir}/man1/report.1.gz

%files plugin-reportuploader
%defattr(-,root,root,-)
%{_mandir}/man*/reporter-upload.*
%{_bindir}/reporter-upload
%{_sysconfdir}/libreport/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf
%{_sysconfdir}/libreport/workflows/workflow_Upload.xml

%files fedora
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/workflows/workflow_Fedora.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_fedora.conf

%files rhel
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/workflows/workflow_RHELCCpp.xml
%{_sysconfdir}/libreport/workflows/workflow_RHELKerneloops.xml
%{_sysconfdir}/libreport/workflows/workflow_RHELPython.xml
%{_sysconfdir}/libreport/workflows/workflow_RHELvmcore.xml
%{_sysconfdir}/libreport/workflows/workflow_RHELxorg.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_rhel.conf

%files anaconda
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/workflows/workflow_AnacondaFedora.xml
%{_sysconfdir}/libreport/workflows/workflow_AnacondaUpload.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_anaconda_event.conf


%changelog
* Fri May 10 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.1.4-5
- removed dependency on recordmydesktop rhbz#959475

* Mon May 06 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-4
- create last_occurrence at the time of the first crash

* Fri May 03 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-2
- update translation
- reporter-bugzilla: provide version of libreport

* Mon Apr 29 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-1
- support /etc/os-release
- added flag to not retry locking the incomplete problem dir
- ureport: save solutions in not-reportable item
- wizard: make value column click-sortable too
- wizard: fix clickability of the item list column header
- wizard: eliminate evd->error_msg member
- wizard: remove a bunch of evd->foo members
- debuginfo downloader should enable repos matching *debug* closes #138
- Replace "THANKYOU" with EXIT_STOP_EVENT_RUN exit code (70)
- debuginfo downloader: fix DebugInfoDownload::download() error paths.
- report-gtk: handle user cancellation gracefully
- logging: refine errors reporting
- emit a message when searching bugzilla for duplicates closes #151
- reporter-upload: create tarball with the name based on directory's name
- reporter-rhtsupport: generate archive name from problem dir name
- added report-cli event for anaconda should help with rhbz#950544
- ss: skip option holding NULL values
- spec: added new event for anaconda reporting rhbz#926916
- distinguish the event configuration by problem type in the UI closes #149
- report-gtk: show Next Step btn at workflow start
- curl upload helper: upload data with "application/octet-stream" content type
- reporter-rhtsupport: fix hint query to use correct URL

* Thu Apr  4 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.1.3-2
- fixed reporting from anaconda
- Resolves: #926916

* Wed Mar 27 2013 Jakub Filak <jfilak@redhat.com> 2.1.3-1
- rhbz: get id of duplicate from correct field
- change the "exited with" message with something less technical closes #143
- Integration with satyr
- dump_dir_accessible_by_uid(): clear errno if error didn't occur
- reporter-rhtsupport: improve logging
- reporter-rhtsupport: upload file to BigFileURL if it is large
- dd: document used errno values in dump_dir_accessible_by_uid()
- add rhel package with appropriate workflow definitions
- add workflow definitions for RHEL
- improve is_text_file() to not treat valid Unicode as bad_chars
- reporter-rhtsupport: fix double-free error
- reporter-upload: move file upload function to lib/
- reporter-upload: factor out HTTP PUT upload
- reporter-rhtsupport: skip hints check if uploaded data is really large
- reporter-rhtsupport: make -t[CASE_ID] work without FILEs. Closes #140
- reporter-rhtsupport: factor out tarball creation
- RHTS support: regularize order of functions and comments
- fread_with_reporting: make progress indicator less noisy
- report-gtk: update excluded elements check boxes before emergency analysis event
- Resolves: #921941

* Fri Mar 22 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-2
- add a patch which fixes a problem with empty archives in emergency analysis

* Tue Mar 19 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-1
- always treat os-release as textual related to rhbz#922433
- is_text_file(): bump allowable non-ASCII chars from 2% to 10%. Closes rhbz#922433
- report-gtk: don't clear warnings after reporting is finished
- report-gtk: show tabs only in verbose expert mode
- report-gtk: prettify the workflow buttons rhbz#917694
- report-gtk: add a button to report reporting failures
- uReport: do not show URL twice in error output
- uReport: detect missing type field at client side
- uReport: add more explanatory message when upload fails
- uReport: improve messages. Closes #579
- workflows: a less confusing event name for reporting to Fedora infrastructure
- workflows: correct an event name for reporting to Fedora in anaconda config
- fixed workflow localization closes #137
- run_event_state: expose children_count in python wrapper
- add the proxy options to the addvanced section of event configurations
- don't suid before running yum related to rhbz#759443
- update translation
- ss: stop reconnecting to the session bus
- ss: destroy all timeout GSources attached to the main context
- ss: add a timeout to the waiting for the Completed signal
- dd: convert time at lock time
- spawn_next_command: make process group creation optional
- fork_execv_on_steroids: fix close/move order of fds, move getpwuid out of fork
- problem API: generate UUID if is missing instead of DUPHASH
- fix logic of 'Dont ask me again' dialogues (stop returning true for all options)
- make [p]error_msg[_and_die] more fork-in-multithreaded-app safe
- Make forking code paths more robust.
- curl_debug: fix use of "%.*s" (need to pass an int, not size_t)
- curl_debug: prettify debug output
- Resolves: #871126, #885055, #890778, #901467, #916389, #917684, #917694, #919536, #922433, #923117

* Thu Feb 07 2013 Jakub Filak <jfilak@redhat.com> 2.1.1-1
- move 'reporter-mailx' from post-create event to notify(-dup) event
- reporter-bugzilla: use base64 XMLRPC type for encoded data instead of string type
- ureport: fix extra quoting when reporting error messages
- Resolves: #908210

* Tue Feb 05 2013 Jakub Filak <jfilak@redhat.com> 2.1.0-2
- configure libreport to be in conflict with abrt < 2.1.0

* Mon Feb 04 2013 Jakub Filak <jfilak@redhat.com> 2.1.0-1
- dd: unify error handling in save_binary_file()
- dd_sanitize: don't sanitize symlinks
- rpm: preserve old configuration for <F17 and <REHL7
- configure: change defaults to be compliant with /var/tmp/abrt
- configure: fix dump dir mode help string
- dd: always sanitize mode of saved file
- rhbz: replace obsolete methods by their substitutes
- reporter-rhtsupport: improve error detection and logging
- mailx: remove extra trailing newline in help text
- spec: add requires section for pygobject3
- reporter-rhtsupport: retain " Beta" suffix in version. Closes rhbz#896090
- Fix bugs discoverent by Coverity
- bz: swap 'bug id' arg with 'item name' arg in attach fn call
- dd: move dir accessibility check from abrt to libreport
- don't overwrite "type" rhbz#902828
- move chown functionality from ABRT DBus to libreport
- expose configure cmd options for dump dir mode and ownership
- cli: guard against user ^Z-ing editor and being stuck
- report-cli: don't close tty fd too early
- report-cli: switch terminal's fg process group to editor's one; and back
- dd: open symlinks on request
- minor fix to the pkg-config file
- reporter-rhtsupport: extract error message from Strata-Message: header
- add build time condition for dump dir ownership schema
- reporter-bz: post a comment to dup bug, if we found a dup. version 2.
- report-cli: use Client API
- report-cli: add event name prefix before question
- run_event: default callbacks for logging and errors
- make default dump dir mode configurable at build time
- Stop reading text files one byte at a time
- make dd_delete_item check that dd is locked
- never follow symlinks rhbz#887866
- Revert "reporter-bz: post a comment to dup bug, if we found a dup."
- wizard: make radio-button text wrap
- reporter-bz: post a comment to dup bug, if we found a dup.
- added missing article
- make the dependency on recordmydesktop soft - related to rhbz#891512
- cli: use !ec_skip_review as indicator that the event is a reporter
- Add and use "report-cli" event instead of removed "report-cli -r" option
- cli: remove superfluous problem_data_free() call
- uReport: add more explanatory message when upload fails
- report-cli rework
- don't require recordmydesktop on RHEL rhbz#891512
- fixed the relro flags rhbz#812283
- bugzilla_format_kernel.conf: Attach dmesg element. Closes rhbz#826058
- bugzilla_format_kernel.conf: fix %summary
- Make get_dirsize_find_largest_dir less talkative.
- Minor fixes: robustify start_command(), fix style, fix English in msgs
- Fix typo, remove c-format from a not c-formatted message
- Resolves: #826058, #902828

* Tue Jan  1 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.20-2
- don't require recordmydesktop on rhel

* Wed Dec 19 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.20-1
- New version 2.0.20
- updated po files
- add abrt-screencast to POTFILES.in
- added screen casting support to the wizard
- fix memory leaks in workflow code
- report_problem_in_dir(): make LIBREPORT_DEL_DIR work
- add Yes/No dialog saving answer
- refactor: move ask_yes_no_save_result from wizard to libreport-gtk
- added anaconda workflows rhbz#885690
- report-python: export dd_delete_item too
- report-python: export DD_OPEN_READONLY too
- strtrimch: optimize it a bit
- show only workflows applicable to actual problem directory
- report-gtk: destroy global text cache only once
- change rules for FILENAME_NOT_REPORTABLE to always include trailing period.
- ask for BZ login/BZ pwd if Login attempt failed
- ask for BZ login/BZ password if not provided by conf
- remove new line from ask/ask_password responses
- add ask_yes_no_yesforever() to Python client API
- make client API independent on translation
- run_event: use client functions for the communication callbacks
- clean the workflow buttons when refreshing the event page
- Fix a bug - inverted check for failed rename() call
- wrap the not_reportable label .trac#908
- don't show events without configuration in preferences .trac#881
- - implemented saving/loading configuratio for workflows - related to trac#822
- reporter-bz: add AVC's description added to BZ comment
- add microseconds to dump dir name (problem ID)
- teach reporter-bugzilla to read BZ ID from reported_to element
- teach reporter-bugzilla to add reporter to CC
- introduce a function deleting dd's element
- introduce a function getting no. of Bytes of dd's element
- make event config name immutable
- fixed segv in the last commit
- made struct workflow private related to trac#822
- don't show the spinner if the problem is not reportable trac#852
- made the config_item_info structure private
- added workflows trac#822
- added x,--expert cmdline option to enable expert mode
- switch comment and event selector page
- use get_ and set_ functions to access event_config_t
- reporter-bz: don't return NULL on %non_existing_item% - use "" instead
- refactoring the xml and conf loader code related to trac#822
- reporter-bugzilla: add a --debug option
- reporter-bz: fix a summary line formatting bug
- let logging_callback and post_run_callback members be None
- expose make_run_event_state_forwarding() in Python API
- reporter-bz: change syntax of bugzilla_format_*.conf to require "text::", not "text:"
- reporter-bz: add support for line continuation and simple text in bugzilla_format*.conf

* Mon Dec 03 2012 Jakub Filak <jfilak@redhat.com> 2.0.19-3
- add a description of AVC to bugzilla comment 0

* Mon Nov 26 2012 Jakub Filak <jfilak@redhat.com> 2.0.19-2
- fix bugzilla summary formatting
- Resolves: #879846

* Wed Nov 14 2012 Jakub Filak <jfilak@redhat.com> 2.0.19-1
- introduce a new formating feature for Bugzilla plugin
- use gtk_show_uri() instead of own launcher
- update kerneloops urls
- don't force the minimal rating trac#854
- add support for forwarding of report client requests
- fix i18n in event client communication protocol
- add event name to the error message - can't get secret item
- switch all load_conf_file() calls to use skipKeysWithoutValue=false
- hide the spinner when the event processing is finishes trac#852
- add a method for loading of configuration of a single event
- unlock secret collection only on meaningful demand
- fix secret item look up for gnome-keyring

* Thu Nov 01 2012 Jakub Filak <jfilak@redhat.com> 2.0.18-1
- reporter-bz: tighten up checking that BZ server gave us its version; fix recently broken settings parsing
- reporter-bz: make selinux-policy special case controllable from config file
- reporter-bz: if we create a new bug but cross-version dup exists, add a note
- reporter-bz: make rhbz_search_duphash static, use it more widely

* Wed Oct 24 2012 Jakub Filak <jfilak@redhat.com> 2.0.17-1
- update CWD after stealing of a dump directory
- get product/version from system configuration
- shorten bz summary if its length exceeds 255 chars
- add full kerneloops to the uReport
- reporter-bz: require bz version match when searching for dups. Closes rhbz#849833
- reporter-bz: eliminate bugzilla_struct::b_product - use auto var instead
- Move struct bugzilla_struct to its only user, reporter-bugzilla.c
- reporter-bz: do not needlessly open dd if -f; assorted small fixes
- added relro to reportclient.so and _pyreport.so rhbz#812283
- bz reporter: include ROOTDIR, OS_RELEASE_IN_ROOTDIR, EXECUTABLE elements
- Fix report-newt segfault
- Resolves: #741647, #812283, #849833, #867118, #869032

* Thu Oct 11 2012 Jakub Filak <jfilak@redhat.com> 2.0.16-1
- expand events from a chain and process expanded events separately
- report-gtk: move selection of event to a right place
- fix a crash while report-gtk startup (use the correct variable)
- wizard: allow "non-reportable" reporting for experts; disallow it for non-experts
- fix typo in function name, remove unnecessary forward declaratioins
- wizard: fix a thinko in last commit (thanks Jakub)
- wizard: check for NON_REPORTABLE file, stop if it exists.FILE
- wizard: remove unnecessary if (1) {...} block. No code changes
- don't update the selected event while processing it
- check D-Bus err name without leaking nor crashing
- ureport: always include offset
- add Makefile target release-fix
- Resolves: #864803, #864803, #863595

* Fri Oct 05 2012 Jakub Filak <jfilak@redhat.com> 2.0.15-1
- remove unnecessary flag from words highlighting functions
- report-gtk: rework forbidden words highlighting
- add xmalloc_fopen_fgetline_fclose helper for reading one-line files
- update GUI before highlighting of forbidden words
- clear warnings after switching to a next page
- tweak conditions in show next forbidden word functions
- reporter-ureport: respect chrooted os_release
- Fix typos.
- rhbz#861679: report-gtk: immediately release dump directory lock
- add a few helpers for reading files as one malloced block

* Fri Sep 21 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.14-1
- added error callback to get notification about download failure rhbz#786640
- rhbz#767186: show a link to a page describing the ABRT configuration
- spec: silence rpmdiff rhbz#857425
- don't show the credential in logs rhbz#856960
- rhbz#852165: warn if adding commands without any rule condition
- rhbz#851855: process ureport server errors correctly
- reporter-bugzilla: fix adding users to CC. (Partially?) closes rhbz#841338
- Resolves: #786640, #767186, #857425, #856960, #852165, #851855, #841338

* Wed Aug 29 2012 Jakub Filak <jfilak@redhat.com> 2.0.13-2
- increment the release number due to rebuild for F17 package

* Tue Aug 21 2012 Jakub Filak <jfilak@redhat.com> 2.0.13-1
- rhbz#741255: don't autodetect executable for sealert reports
- reporter-ureport: save backtrace hash to reported_to
- trac#683: show the description file in bugzilla comment 0
- trac#684: report-gtk saves only loaded files
- reporter-ureport: allow sending attachments
- event_config_dialog: make it resizable; tweak Uploader hint
- add python binding for problem_data_send_to_abrt
- reporter-ureport: attach bug ID from reported_to
- reporter-ureport: make configurable only URL to a server
- Resolves: #741255

* Wed Aug 15 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-5
- rhbz#741255: don't autodetect executable for sealert reports
- show message from the server for known uReports
- trac#678: reporter-bugzilla: do not attach empty files
- Resolves: #741255

* Tue Aug 14 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-4
- rhbz#846389: generate koops description according to rhbz std template
- trac#556: skip not provided bz bug description template fields
- report-gtk: don't log THANKYOU message
- added internal_libreport.h into POTFILES.in rhbz#801255
- updated po files
- Resolves: #801255, #846389

* Fri Aug 10 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-3
- wizard: small changes to message texts and one function name
- trac#623: dd_opendir() fails if time file doesn't contain valid time stamp
- trac#660: report-cli asks for premission to send sensitive data
- trac#660: report-gtk asks for permission to send sensitive data
- trac#660: report-gtk: introduce generic ask_yes_no() function for options
- trac#660: add support for sendining-sensitive-data event option
- Do not check for analyzer == "Kerneloops" when appending "TAINTED" msg
- fix leaks in list_possible_events()

* Tue Aug 7 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-2
- report-gtk: fixed bug in automatic running of next event
- don't try to delete dump dir which doesn't exist rhbz#799909
- Resolves: #799909

* Fri Aug 3 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-1
- new upstream release
- trac#642: run the next event if the current one finished without errors
- trac#641: don't allow event chain to continue, if user don't want to steal a directory
- trac#640: report-gtk replaces 'Forward' button with 'Close' button on finished reporting
- Fix bugs uncovered by Coverity. Closes rhbz#809416
- Resolves: #809416

* Tue Jul 31 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.11-1
- new upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-4
- fixed build on rhel7

* Mon May 14 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-3
- fixed compatibility with bugzilla 4.2
- Resolved: #820985, #795548

* Mon Apr 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-2
- added cgroups filename define

* Mon Mar 26 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-1
- updated to latest upstream

* Mon Jan 23 2012 Dan Horák <dan@danny.cz> - 2.0.8-6
- rebuilt for json-c-0.9-4.fc17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Nikola Pajkovsky <npajkovs@redhat.com> 2.0.8-4
- 768647 - [abrt] libreport-plugin-bugzilla-2.0.8-3.fc16: libreport_xatou:
           Process /usr/bin/reporter-bugzilla was killed by signal 11 (SIGSEGV)

* Fri Dec 09 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-3
- fixed few crashes in bodhi plugin

* Thu Dec 08 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-2
- fixed crash in bodhi plugin
- re-upload better backtrace if available
- fixed dupe finding for selinux
- don't duplicate comments in bugzilla
- fixed problem with empty release

* Tue Dec 06 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-1
- new version
- added bodhi plugin rhbz#655783
- one tab per file on details page rhbz#751833
- search box search thru all data (should help with privacy) rhbz#748457
- fixed close button position rhbz#741230
- rise the attachment limit to 4kb rhbz#712602
- fixed make check (rpath problem)
- save chnages in editable lines rhbz#710100
- ignore backup files rhbz#707959
- added support for proxies rhbz#533652
- Resolves: 753183 748457 737991 723219 712602 711986 692274 636000 631856 655783 741257 748457 741230 712602 753183 748457 741230 712602 710100 707959 533652

* Sat Nov 05 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-2
- bumped release

* Fri Nov 04 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-1
- new version
- added support for bodhi (preview)
- dropped unused patches
- reporter-bugzilla/rhts: add code to prevent duplicate reporting. Closes rhbz#727494 (dvlasenk@redhat.com)
- wizard: search thru all items + tabbed details rhbz#748457 (jmoskovc@redhat.com)
- wizard: add "I don't know what caused this problem" checkbox. Closes rhbz#712508 (dvlasenk@redhat.com)
- reporter-bugzilla: add optional 'Product' parameter. Closes rhbz#665210 (dvlasenk@redhat.com)
- rhbz#728190 - man pages contain suspicious version string (npajkovs@redhat.com)
- reporter-print: expand leading ~/ if present. Closes rhbz#737991 (dvlasenk@redhat.com)
- reporter-rhtsupport: ask rs/problems endpoint before creating new case. (working on rhbz#677052) (dvlasenk@redhat.com)
- reporter-mailx: use Bugzilla's output format. Closes rhbz#717321. (dvlasenk@redhat.com)
- report-newt: add option to display version (rhbz#741590) (mlichvar@redhat.com)
- Resolves: #727494 #748457 #712508 #665210 rhbz#728190 #737991 #677052 #717321 #741590

* Fri Oct 07 2011 Nikola Pajkovsky <npajkovs@redhat.com> 2.0.6-2
- refuse reporting when not reportable file exist

* Mon Oct 03 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.6-1
- updated to the latest upstrem
- just a bug fixing release

* Mon Sep 26 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5.982-1
- re-fix rhbz#730887
- re-fixed prgname (nice icons in gnome3) rhbz#741231
- Resolves: #741231 #730887

* Thu Sep 22 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-9
- don't allow sending reports with bad rating rhbz#672023
- don't allow reporting without duphash rhbz#739182
- tell users to fill out reports in English rhbz#734037
- fixed config for kerneloops reporter rhbz#731189
- Resolves: #672023 #739182 #734037 #731189

* Fri Sep 09 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-8
- allow bugzilla to send binary files
- Related: #733448

* Tue Aug 30 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-7
- added glob support to event xml files
- changed handling of long text files
- added a simple editor as a fallback when no editor is installed (i.e in anaconda) rhbz#728479
- Resolves: #733448 #728479

* Tue Aug 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-6
- improved release parsing rhbz#730887
- Resolves: #730887

* Fri Aug 12 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-5
- more anaconda fixes
- Resolves: #729537

* Tue Aug 02 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-4
- silent keyring warning rhbz#692433
- further improvements to Anaconda compatibility

* Fri Jul 29 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-3
- enable bugzilla reporter for analyzer=libreport rhbz#725970
- improved compatibility with anaconda

* Thu Jul 21 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-2
- obsolete report in rawhide properly rhbz#723320
- added button to add attachments
- ignore backup files
- improved support for interactive plugins
- added description text for logger
- added python bindings for interactive plugins
- Resolves: #723320

* Mon Jul 18 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-1
- move reporter plugins from abrt to libreport
- fixed provides/obsolete to properly obsolete report package
- wizard: make more fields editable

* Mon Jul 11 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-3
- bump release

* Mon Jun 27 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-2
- removed Provides/Obsoletes: report-gtk

* Mon Jun 20 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-1
- new upstream release
- cleaned some header files

* Thu Jun 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.3-1
- added report-cli
- updated translation

* Wed Jun 01 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-1
- initial packaging
