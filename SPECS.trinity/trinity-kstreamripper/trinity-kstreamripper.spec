# Default version for this component
%define kdecomp kstreamripper
%define tdeversion 3.5.13.2

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	TDE frontend for streamripper

Version:	0.3.4
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

Patch0:		kstreamripper-3.5.13-missing_include_tqt.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-arts-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	scons


%description
KStreamRipper is a small frontend for the streamripper command
line utility. Streamripper captures internet shoutcast radio streams
on your harddisk and splits them up in mp3 files. KStreamRipper helps
you with managing/ripping your preferred streams.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
%patch0 -p1

%__sed -i kde.py \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|include/kde|include/tde|g"

%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"


scons -Q -j4 \
  qtlibs=${QTLIB:-${QTDIR}/%{_lib}}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}



## File lists
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi


%clean
%__rm -rf %{buildroot}



%files
%defattr(-,root,root,-)
%{tde_bindir}/kstreamripper
%{tde_datadir}/applnk/Utilities/kstreamripper.desktop
%{tde_datadir}/apps/kstreamripper/kstreamripperui.rc
%{tde_tdedocdir}/HTML/en/kstreamripper/



%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 0.3.4-3.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.3.4-2
- Initial build for TDE 3.5.13.1

* Wed Nov 02 2011 Francois Andriot <francois.andriot@free.fr> - 0.3.4-1
- Initial release for TDE 3.5.13 on RHEL 6, RHEL 5 and Fedora 15
