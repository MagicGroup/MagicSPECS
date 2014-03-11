Name:           xmedcon
Version:        0.10.7
Release:        10%{?dist}
Summary:        A medical image conversion utility and library

# Please refer to http://xmedcon.sourceforge.net/pub/readme/README for details
# None of the libraries are bundled, they are appear to be modified versions of code taken
# from the respective sources
# License needs more looking into to confirm correctness. All licenses are FOSS compatible though
License:        LGPLv2+ and Copyright only and MIT and BSD and libtiff
URL:            http://xmedcon.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.desktop
Patch0:         xmedcon-fix-includes.patch
# Patch for libpng provided by Tom Lane in rhbz#843662
# Thanks Tom!
Patch1:         xmedcon-libpng-1.5.patch

BuildRequires:  gtk2-devel nifticlib-devel
BuildRequires:  libtpcimgio-devel libtpcmisc-devel
BuildRequires:  desktop-file-utils

#Requires:       gtk2

%description
This project stands for Medical Image Conversion and is released under the
GNU's (L)GPL license. It bundles the C source code, a library, a flexible
command-line utility and a graphical front-end based on the amazing Gtk+
toolkit.

Its main purpose is image conversion while preserving valuable medical
study information. The currently supported formats are: Acr/Nema 2.0,
Analyze (SPM), Concorde/uPET, DICOM 3.0, CTI ECAT 6/7, InterFile 3.3
and PNG or Gif87a/89a towards desktop applications.

%package devel
Summary: Libraries and header files for (X)MedCon development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The xmedcon-devel package contains the header files and static libraries
necessary for developing programs that make use of the (X)MedCon library
(libmdc).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Remove the sources of the nifti, since we're using fedora nifti here
rm -rvf ./libs/nifti/ 
rm -rvf ./libs/tpc/ 

%build
# Give it the fedora nifti
# Who hardcodes the lib!?
sed -i \
       -e  "s|tpc_prefix/lib|tpc_prefix/%{_lib}|" \
       -e  "s|nifti_prefix/lib|nifti_prefix/%{_lib}|" configure
%configure --disable-static --disable-rpath --with-nifti-prefix=%{_prefix} --with-tpc-prefix=%{_prefix} --enable-shared --includedir=%{_includedir}/xmedcon

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


# Make it use -fPIC
sed -i "s/\(^CFLAGS =\)/\1 -fPIC/" source/Makefile
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

mv -v $RPM_BUILD_ROOT/%{_includedir}/*.h $RPM_BUILD_ROOT/%{_includedir}/%{name}/

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/
install -m 0644 -p etc/%{name}.png -t $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/

desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
%{SOURCE1}

# remove static libraries
find $RPM_BUILD_ROOT -name "*.a" -execdir rm -fv '{}' \;
find $RPM_BUILD_ROOT -name "*.la" -execdir rm -fv '{}' \;

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
# leave out ChangeLog : zero length
%doc COPYING COPYING.LIB README REMARKS AUTHORS etc/%{name}rc.linux
%config(noreplace) %{_sysconfdir}/xmedconrc
%{_bindir}/medcon
%{_bindir}/%{name}
%{_libdir}/*so.*
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png


%files devel
%doc README COPYING COPYING.LIB
%{_bindir}/%{name}-config
%{_mandir}/man3/*
%{_mandir}/man4/*
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_datadir}/aclocal/*

%changelog
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.7-9
- Use Tom's patch to fix FTBFS because of libpng 1.5
- Details here: rhbz#843662 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.10.7-6
- Rebuild for new libpng

* Sun Nov 13 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-5
- Correct placements of includes and configure command
- RHBZ #753246

* Tue Aug 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-4
- Move xmedcon-config to -devel
- Correct requires for -devel
- Add icon, scriptlets
- Add desktop file, scriptlets
- Add a xmedconrc.linux file in docs
- Remove defattr

* Tue Aug 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-3
- Fix license tag
- remove rpath
- https://bugzilla.redhat.com/show_bug.cgi?id=714328#c3
- Fix sed
 
* Sun Jul 03 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-2
- Make it use fPIC

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-1
- Initial rpm build
- Based on the spec built by Erik Nolf for the srpm available at 
- http://xmedcon.sourceforge.net/Main/Download

