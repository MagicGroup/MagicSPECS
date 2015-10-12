# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".

%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_confdir %{_sysconfdir}/trinity
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}

Name:           trinity-knoda
Version:        0.8.3
Release:        1%{?dist}%{?_variant}
Summary:        A database frontend for TDE.

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://sourceforge.net/projects/knoda/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        http://downloads.sourceforge.net/project/knoda/knoda/0.8.3/knoda-0.8.3.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdelibs-devel
BuildRequires:	hk_classes-devel
Requires:		hk_classes


%description


%package devel
Summary:  	Development files for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}


%description devel
%{summary}


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n knoda-%{version}

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"


%configure \
	--prefix=%{tde_prefix} \
	--exec-prefix=%{tde_prefix} \
	--disable-dependency-tracking \
	--enable-rpath \
	--bindir=%{tde_bindir} \
	--libdir=%{tde_libdir} \
	--datadir=%{tde_datadir} \
	--includedir=%{tde_tdeincludedir} 

 
%__make %{?_smp_mflags} || %__make


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT


# Useless files ..
%__rm -f %{?buildroot}%{tde_libdir}/*.a
%__rm -f %{?buildroot}%{tde_tdelibdir}/*.a

%find_lang knoda

%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for i in hicolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%postun
for i in hicolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%files -f knoda.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{tde_bindir}/knoda
%{tde_bindir}/knoda-rt
%{tde_libdir}/libhk_kdeclasses.la
%{tde_libdir}/libhk_kdeclasses.so
%{tde_tdelibdir}/libhk_kdedbdesignerpart.la
%{tde_tdelibdir}/libhk_kdedbdesignerpart.so
%{tde_tdelibdir}/libhk_kdeformpart.la
%{tde_tdelibdir}/libhk_kdeformpart.so
%{tde_tdelibdir}/libhk_kdegridpart.la
%{tde_tdelibdir}/libhk_kdegridpart.so
%{tde_tdelibdir}/libhk_kdemodulepart.la
%{tde_tdelibdir}/libhk_kdemodulepart.so
%{tde_tdelibdir}/libhk_kdeqbepart.la
%{tde_tdelibdir}/libhk_kdeqbepart.so
%{tde_tdelibdir}/libhk_kdequerypart.la
%{tde_tdelibdir}/libhk_kdequerypart.so
%{tde_tdelibdir}/libhk_kdereportpart.la
%{tde_tdelibdir}/libhk_kdereportpart.so
%{tde_tdelibdir}/libhk_kdetablepart.la
%{tde_tdelibdir}/libhk_kdetablepart.so
%{tde_datadir}/applnk/Office/knoda.desktop
%{tde_datadir}/apps/hk_kdeclasses/
%{tde_datadir}/apps/knoda/
%{tde_confdir}/magic/hk_classes.magic
%{tde_tdedocdir}/HTML/en/knoda/
%{tde_datadir}/icons/hicolor/*/apps/knoda.png
%{tde_datadir}/icons/locolor/*/apps/knoda.png
%{tde_datadir}/mimelnk/application/x-hk_classes-sqlite2.desktop
%{tde_datadir}/mimelnk/application/x-hk_classes-sqlite3.desktop
%{tde_datadir}/mimelnk/application/x-hk_connection.desktop
%{tde_datadir}/mimelnk/application/x-paradox.desktop
%{tde_datadir}/mimelnk/application/x-xbase.desktop
%{tde_datadir}/services/hk_kdedbdesignerpart.desktop
%{tde_datadir}/services/hk_kdeformpart.desktop
%{tde_datadir}/services/hk_kdegridpart.desktop
%{tde_datadir}/services/hk_kdemodulepart.desktop
%{tde_datadir}/services/hk_kdeqbepart.desktop
%{tde_datadir}/services/hk_kdequerypart.desktop
%{tde_datadir}/services/hk_kdereportpart.desktop
%{tde_datadir}/services/hk_kdetablepart.desktop


%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/hk_kdeboolean.h
%{tde_tdeincludedir}/hk_kdebutton.h
%{tde_tdeincludedir}/hk_kdecolumn.h
%{tde_tdeincludedir}/hk_kdecombobox.h
%{tde_tdeincludedir}/hk_kdecsvexportdialog.h
%{tde_tdeincludedir}/hk_kdecsvimportdialog.h
%{tde_tdeincludedir}/hk_kdecsvimportdialogbase.h
%{tde_tdeincludedir}/hk_kdedatasource.h
%{tde_tdeincludedir}/hk_kdedate.h
%{tde_tdeincludedir}/hk_kdedbdesignerpart.h
%{tde_tdeincludedir}/hk_kdedbdesignerpartfactory.h
%{tde_tdeincludedir}/hk_kdedblistview.h
%{tde_tdeincludedir}/hk_kdedriverdialog.h
%{tde_tdeincludedir}/hk_kdefilterdialog.h
%{tde_tdeincludedir}/hk_kdefilterdialogbase.h
%{tde_tdeincludedir}/hk_kdefinddialog.h
%{tde_tdeincludedir}/hk_kdefinddialogbase.h
%{tde_tdeincludedir}/hk_kdeform.h
%{tde_tdeincludedir}/hk_kdeformdatasourcedialog.h
%{tde_tdeincludedir}/hk_kdeformdatasourcedialogbase.h
%{tde_tdeincludedir}/hk_kdeformfocus.h
%{tde_tdeincludedir}/hk_kdeformpart.h
%{tde_tdeincludedir}/hk_kdeformpartfactory.h
%{tde_tdeincludedir}/hk_kdeformpartwidget.h
%{tde_tdeincludedir}/hk_kdegrid.h
%{tde_tdeincludedir}/hk_kdegridcolumndialog.h
%{tde_tdeincludedir}/hk_kdegridcolumndialogbase.h
%{tde_tdeincludedir}/hk_kdegridpart.h
%{tde_tdeincludedir}/hk_kdegridpartfactory.h
%{tde_tdeincludedir}/hk_kdeimage.h
%{tde_tdeincludedir}/hk_kdeindexeditwindow.h
%{tde_tdeincludedir}/hk_kdeinterpreterdialog.h
%{tde_tdeincludedir}/hk_kdelabel.h
%{tde_tdeincludedir}/hk_kdelineedit.h
%{tde_tdeincludedir}/hk_kdememo.h
%{tde_tdeincludedir}/hk_kdemessages.h
%{tde_tdeincludedir}/hk_kdemodule.h
%{tde_tdeincludedir}/hk_kdemodulepart.h
%{tde_tdeincludedir}/hk_kdemodulepartfactory.h
%{tde_tdeincludedir}/hk_kdenewpassworddialog.h
%{tde_tdeincludedir}/hk_kdenewpassworddialogbase.h
%{tde_tdeincludedir}/hk_kdepassworddialog.h
%{tde_tdeincludedir}/hk_kdeproperty.h
%{tde_tdeincludedir}/hk_kdepropertybase.h
%{tde_tdeincludedir}/hk_kdeqbe.h
%{tde_tdeincludedir}/hk_kdeqbepart.h
%{tde_tdeincludedir}/hk_kdeqbepartfactory.h
%{tde_tdeincludedir}/hk_kdequery.h
%{tde_tdeincludedir}/hk_kdequerypart.h
%{tde_tdeincludedir}/hk_kdequerypartfactory.h
%{tde_tdeincludedir}/hk_kdequerypartwidget.h
%{tde_tdeincludedir}/hk_kdereport.h
%{tde_tdeincludedir}/hk_kdereportdata.h
%{tde_tdeincludedir}/hk_kdereportpart.h
%{tde_tdeincludedir}/hk_kdereportpartfactory.h
%{tde_tdeincludedir}/hk_kdereportpartwidget.h
%{tde_tdeincludedir}/hk_kdereportproperty.h
%{tde_tdeincludedir}/hk_kdereportpropertybase.h
%{tde_tdeincludedir}/hk_kdereportsection.h
%{tde_tdeincludedir}/hk_kdereportsectiondialog.h
%{tde_tdeincludedir}/hk_kdereportsectiondialogbase.h
%{tde_tdeincludedir}/hk_kderowselector.h
%{tde_tdeincludedir}/hk_kdesimpleform.h
%{tde_tdeincludedir}/hk_kdesimplegrid.h
%{tde_tdeincludedir}/hk_kdesimplereport.h
%{tde_tdeincludedir}/hk_kdesubform.h
%{tde_tdeincludedir}/hk_kdesubreportdialog.h
%{tde_tdeincludedir}/hk_kdesubreportdialogbase.h
%{tde_tdeincludedir}/hk_kdetable.h
%{tde_tdeincludedir}/hk_kdetabledesign.h
%{tde_tdeincludedir}/hk_kdetablepart.h
%{tde_tdeincludedir}/hk_kdetablepartfactory.h
%{tde_tdeincludedir}/hk_kdetablepartwidget.h
%{tde_tdeincludedir}/hk_kdetoolbar.h
%{tde_tdeincludedir}/hk_kdexmlexportdialog.h
%{tde_tdeincludedir}/hk_kdexmlexportdialogbase.h


%changelog
* Mon Apr 08 2013 Francois Andriot <francois.andriot@free.fr> - 0.5b-1
- Initial release for TDE 3.5.13.2
