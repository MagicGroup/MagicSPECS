Name:  librfm
Summary: Rodent file manager basic library functionality
Version: 5.3.16
Release: 7%{?dist}
Group:   System Environment/Libraries
License: GPLv3+
URL:   http://xffm.org/
Source0: http://sourceforge.net/projects/xffm/files/%{version}.5/librfm5-%{version}.3.tar.bz2

##https://bugzilla.redhat.com/show_bug.cgi?id=1210424
Patch0: %{name}-magic_header.patch

BuildRequires:  gtk3-devel, ghostscript
BuildRequires:  libxml2-devel
BuildRequires:  file-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  libSM-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libzip-devel
BuildRequires:  dbh-devel >= 5.0.13
BuildRequires:  tubo-devel >= 5.0.14
BuildRequires:  procps-ng, automake, autoconf

%description
Basic library functionality for Rodent applications. This includes
two libraries: low level and high level, plus the minimum icon 
emblems and translations.

%package devel
Summary: The %{name} headers and development-related files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Shared links, header files for %{name}.

%prep
%setup -q -n %{name}5-%{version}.3

%patch0 -p0

%build
autoreconf -if
%configure --enable-static=no --enable-shared=yes --disable-silent-rules \
 --disable-gtk-doc-html --with-la-files=no

##Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

## Fix 'unused-direct-shlib-dependency' warnings
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}5 --with-gnome

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/rfm &>/dev/null || :

%postun 
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/rfm &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/rfm &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/rfm &>/dev/null || :

%files -f %{name}5.lang
%doc ChangeLog README NEWS
%if 0%{?fedora}
%license COPYING
%else
%doc COPYING
%endif
%{_libdir}/librfm.so.*
%{_libdir}/librodent.so.*
%{_libdir}/rfm/
%{_datadir}/icons/rfm/
%{_datadir}/rfm/

## The following directory is co-owned with other packages
%dir %{_datadir}/images
%{_datadir}/images/*.jpg

%files devel
%ifarch aarch64
%{_libdir}/pkgconfig/*.pc
%else
%{_datadir}/pkgconfig/*.pc
%endif
%{_includedir}/rfm/
%{_libdir}/librfm.so
%{_libdir}/librodent.so

%changelog
* Sun Jul 05 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.16-7
- pkgconfig files installed in libdir on aarch64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-5
- Update to 5.3.16.3
- pkg-config files moved into /usr/share by upstream

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 5.3.16-4
- rebuild for new libzip

* Mon Apr 13 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-3
- Fixed upstream URL

* Fri Apr 10 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-2
- Disabled mimetype determination by magic (patch0)

* Thu Apr 09 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.16-1
- Update to 5.3.16.0

* Tue Jan 06 2015 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-3
- Update to 5.3.14.6

* Tue Dec 16 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-2
- Libraries generation patched

* Mon Dec 15 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.14-1
- Update to 5.3.14.5

* Sun Sep 28 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.12-2
- librfm now requires gtk3 by default
- ghostscript BR

* Sun Sep 28 2014 Antonio Trande <sagitterATfedoraproject.org> 5.3.12-1
- Update to 5.3.12
- libtubo minimum release changed

* Mon Jul 14 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.10-1
- Release 5.2.10

* Sat Mar 22 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.9-1
- Release 5.2.9

* Sun Mar 09 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.8-1
- Update to a 5.2.8

* Fri Feb 28 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.7-1
- Update to a 5.2.7

* Sat Feb 22 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.6-1
- Update to a 5.2.6

* Wed Feb 19 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.5-1
- Update to a 5.2.5
- Removing rpaths

* Sun Feb 09 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.3-1.20140207git5c2e81
- Update to a 5.2.3 post-release (5c2e81) from git
- Perform autogen.sh to create system specific build files

* Sat Jan 11 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.1-1
- Update to 5.2.1
- Removed runtime libs from -devel package
- Removed %%post/%%postun calls for -devel package
- Added Group tag to the base package

* Tue Jan 07 2014 Antonio Trande <sagitterATfedoraproject.org> 5.2.0-2
- DBH minimum release changed 

* Sun Dec 29 2013 Antonio Trande <sagitterATfedoraproject.org> 5.2.0-1
- Update to 5.2.0
- Removed --enable-libzip option
- Summary/Description changed
- URL tag changed

* Thu Nov 14 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.5-1
- Update to 5.1.5
- This release wants at least version 5.0.12 of 'tubo' package
- Added %%post/%%postun for -devel package

* Tue Nov 05 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.4-1
- Update to 5.1.4
- Removed 'norpath' patch
- Language files renamed 'librfm5'
- Two JPG files now packaged in %%{_datadir}/images
- COPYING file is now included in the source archive
- Added '--with-libzip' option to configure 

* Sat Oct 12 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.3-2
- Requires dependencies removed
- BuildRequires minimum versions removed

* Sat Oct 12 2013 Antonio Trande <sagitterATfedoraproject.org> 5.1.3-1
- First package
