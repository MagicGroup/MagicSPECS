%define name	stardict
%define version	3.0.6
%define enable_gnome 0
%define enable_plugins 0

Name:		%{name}
Summary: 	A powerful dictionary platform written in GTK+2
Summary(zh_CN.UTF-8): GTK2 写成的强大的词典平台
Version:	%{version}
Release:	4%{?dist}
Group: 		Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
License: 	GPL
URL: 		http://stardict.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source2:	stardict.desktop
Source1:        defaultdict.cfg
Patch4:		stardict-3.0.4-gmodule.patch
Patch5:         stardict-default-netdict-off.patch
Patch6:         stardict-3.0.1-gcc46.patch
Patch7:		stardict-3.0.2-glib.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

Requires: libsigc++20 >= 2.0.17
BuildRequires: libsigc++20-devel

%if %enable_gnome
Requires: libgnome >= 2.2.0
Requires: libgnomeui >= 2.2.0
Requires: libbonobo >= 2.2.0
Requires: bonobo-activation >= 2.2.0
BuildRequires: libgnomeui-devel >= 2.2.0, scrollkeeper, gettext, perl-XML-Parser
Requires(post): GConf2
%endif
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%if %enable_plugins
Requires: gucharmap
BuildRequires: gucharmap-devel
Requires: espeak
BuildRequires: espeak-devel
Requires: enchant
BuildRequires: enchant-devel
Requires: festival, speech-tools
BuildRequires: festival-devel, speech-tools-devel
%endif

%description
StarDict is a Cross-Platform and international dictionary written in Gtk2.
It has powerful features such as "Glob-style pattern matching,"
"Scan selection word," "Fuzzy query," etc.

%prep
%setup -q
#%patch5 -p1 -b .orig
#%patch6 -p1 -b .orig
#%patch7 -p1
#patch4 -p1

# Remove unneeded sigc++ header files to make it sure
# that we are using system-wide libsigc++
# (and these does not work on gcc43)
find src/sigc++* -name \*.h -or -name \*.cc | xargs rm -f

%build
CFLAGS="${RPM_OPT_FLAGS} -std=c99"
CXXFLAGS="${RPM_OPT_FLAGS} -std=c++11"

%configure --disable-schemas-install --disable-festival --disable-espeak --disable-gucharmap  \
%if ! %{enable_gnome}
	 --disable-gnome-support
%endif
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# copy config file of locale specific default dictionaries
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%{__rm} -f `find %{buildroot}%{_libdir}/stardict/plugins -name "*.la"`
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/stardict.desktop

magic_rpm_clean.sh
%find_lang %{name}


%post
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update; fi

%postun
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update; fi


%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -f %{name}.lang
%defattr(-, root, root)
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/stardict/plugins/*
%{_sysconfdir}/stardict/defaultdict.cfg
%{_datadir}/gnome/*
%{_datadir}/omf/*
%{_datadir}/stardict/*
%{_datadir}/applications/stardict.desktop
%{_datadir}/pixmaps/stardict.png
%if %enable_gnome
%{_sysconfdir}/gconf/schemas/*.schemas
%endif





%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 3.0.6-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.0.6-3
- 为 Magic 3.0 重建

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 3.0.6-2
- 为 Magic 3.0 重建

* Fri Nov 23 2007 Liu Di <liudidi@gmail.com>  - 3.0.1-1mgc
- update to 3.0.1

* Fri Aug 24 2007 kde <athena_star {at} 163 {dot} com> - 3.0.0.1-1mgc
- init the spec file
- use a modified edition from Gao Changli <xiao_suo {at} hotmail {dot} com> that enable --disable-gnome-support
